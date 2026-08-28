package com.nitron.bubble

import android.content.Intent
import android.os.Bundle
import android.widget.EditText
import android.widget.ImageButton
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.nitron.bubble.chat.ChatManager
import com.nitron.bubble.chat.Message
import com.nitron.bubble.chat.MessageAdapter
import org.json.JSONArray
import org.json.JSONObject

class ProjectChatActivity : AppCompatActivity() {

    private lateinit var projectName: String
    private lateinit var messageAdapter: MessageAdapter
    private lateinit var messageList: RecyclerView
    private lateinit var input: EditText
    private lateinit var chatManager: ChatManager

    companion object {
        private const val IMAGE_REQUEST_CODE = 1001
        private const val PREFS_PREFIX = "nitron_project_"
        private const val MESSAGES_KEY = "messages"
        private const val LAST_ACTIVITY_KEY = "last_activity"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContentView(R.layout.project_chat)

        projectName =
            intent.getStringExtra("project_name") ?: "Project"

        findViewById<TextView>(R.id.projectTitle).text =
            projectName

        messageList =
            findViewById(R.id.projectMessageList)

        input =
            findViewById(R.id.projectMessageInput)

        messageAdapter = MessageAdapter()

        messageList.layoutManager =
            LinearLayoutManager(this)

        messageList.adapter =
            messageAdapter

        chatManager = ChatManager()

        chatManager.setListener(
            object : ChatManager.ChatListener {

                override fun onReply(reply: String) {

                    runOnUiThread {

                        messageAdapter.addMessage(
                            Message(
                                text = reply,
                                fromUser = false
                            )
                        )

                        saveMessages()
                        scrollToLatest()
                    }
                }
            }
        )

        loadMessages()

        findViewById<ImageButton>(R.id.backButton)
            .setOnClickListener {
                finish()
            }

        findViewById<ImageButton>(R.id.imageButton)
            .setOnClickListener {

                val intent =
                    Intent(Intent.ACTION_OPEN_DOCUMENT)

                intent.type = "image/*"

                intent.addCategory(
                    Intent.CATEGORY_OPENABLE
                )

                startActivityForResult(
                    intent,
                    IMAGE_REQUEST_CODE
                )
            }

        findViewById<ImageButton>(R.id.projectSendButton)
            .setOnClickListener {
                sendTextMessage()
            }
    }

    private fun sendTextMessage() {

        val text =
            input.text.toString().trim()

        if (text.isEmpty()) {
            return
        }

        messageAdapter.addMessage(
            Message(
                text = text,
                fromUser = true
            )
        )

        input.setText("")

        saveMessages()
        scrollToLatest()

        chatManager.sendMessage(text)
    }

    @Suppress("DEPRECATION")
    override fun onActivityResult(
        requestCode: Int,
        resultCode: Int,
        data: Intent?
    ) {
        super.onActivityResult(
            requestCode,
            resultCode,
            data
        )

        if (
            requestCode == IMAGE_REQUEST_CODE &&
            resultCode == RESULT_OK &&
            data?.data != null
        ) {

            val imageUri = data.data!!

            try {
                contentResolver.takePersistableUriPermission(
                    imageUri,
                    Intent.FLAG_GRANT_READ_URI_PERMISSION
                )
            } catch (_: Exception) {
            }

            messageAdapter.addMessage(
                Message(
                    text = "",
                    fromUser = true,
                    imageUri = imageUri.toString()
                )
            )

            saveMessages()
            scrollToLatest()
        }
    }

    private fun saveMessages() {

        val messages =
            messageAdapter.getMessages()

        val jsonArray = JSONArray()

        for (message in messages) {

            val json =
                JSONObject()

            json.put(
                "text",
                message.text
            )

            json.put(
                "fromUser",
                message.fromUser
            )

            json.put(
                "imageUri",
                message.imageUri ?: JSONObject.NULL
            )

            json.put(
                "timestamp",
                message.timestamp
            )

            jsonArray.put(json)
        }

        getSharedPreferences(
            PREFS_PREFIX + projectName,
            MODE_PRIVATE
        )
            .edit()
            .putString(
                MESSAGES_KEY,
                jsonArray.toString()
            )
            .putLong(
                LAST_ACTIVITY_KEY,
                System.currentTimeMillis()
            )
            .apply()
    }

    private fun loadMessages() {

        val prefs =
            getSharedPreferences(
                PREFS_PREFIX + projectName,
                MODE_PRIVATE
            )

        val saved =
            prefs.getString(
                MESSAGES_KEY,
                null
            ) ?: return

        try {

            val jsonArray =
                JSONArray(saved)

            for (i in 0 until jsonArray.length()) {

                val json =
                    jsonArray.getJSONObject(i)

                val text =
                    json.optString("text", "")

                val fromUser =
                    json.optBoolean(
                        "fromUser",
                        false
                    )

                val imageUri =
                    if (
                        json.isNull("imageUri")
                    ) {
                        null
                    } else {
                        json.optString(
                            "imageUri",
                            null
                        )
                    }

                val timestamp =
                    json.optLong(
                        "timestamp",
                        System.currentTimeMillis()
                    )

                messageAdapter.addMessage(
                    Message(
                        text = text,
                        fromUser = fromUser,
                        imageUri = imageUri,
                        timestamp = timestamp
                    )
                )
            }

            scrollToLatest()

        } catch (_: Exception) {
            // Ignore corrupted old project data.
        }
    }

    private fun scrollToLatest() {

        if (messageAdapter.itemCount == 0) {
            return
        }

        messageList.post {
            messageList.smoothScrollToPosition(
                messageAdapter.itemCount - 1
            )
        }
    }
}
