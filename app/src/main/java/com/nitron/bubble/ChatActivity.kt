package com.nitron.bubble

import android.os.Bundle
import android.Manifest
import android.content.pm.PackageManager
import android.view.inputmethod.InputMethodManager
import android.content.Context
import android.widget.Button
import android.widget.EditText
import android.content.Intent
import androidx.activity.OnBackPressedCallback
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.nitron.bubble.chat.Message
import com.nitron.bubble.chat.MessageAdapter
import com.nitron.bubble.chat.ChatHistoryStore

class ChatActivity : AppCompatActivity() {

    private lateinit var recyclerView: RecyclerView
    private lateinit var messageBox: EditText
    private lateinit var sendButton: Button
    private lateinit var imageButton: Button

    private val adapter = MessageAdapter()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContentView(R.layout.chat_window)

        recyclerView = findViewById(R.id.recyclerView)
        messageBox = findViewById(R.id.messageBox)
        sendButton = findViewById(R.id.sendButton)
        imageButton = findViewById(R.id.imageButton)

        imageButton.setOnClickListener {
            startActivity(
                Intent(this, ImagePickerActivity::class.java)
            )
        }

        recyclerView.layoutManager =
            LinearLayoutManager(this)

        recyclerView.adapter = adapter

        // Load the existing Nitron conversation
        ChatHistoryStore.init(this)
        ChatHistoryStore.getAll().forEach { message ->
            adapter.addMessage(message)
        }

        if (adapter.itemCount > 0) {
            recyclerView.scrollToPosition(
                adapter.itemCount - 1
            )
        }

        sendButton.setOnClickListener {

            val text = messageBox.text
                .toString()
                .trim()

            if (text.isEmpty()) {
                return@setOnClickListener
            }

            adapter.addMessage(
                Message(text, true)
            )

            recyclerView.scrollToPosition(
                adapter.itemCount - 1
            )

            messageBox.setText("")

            if (
                text.equals("scan", ignoreCase = true) ||
                text.equals("scan wifi", ignoreCase = true) ||
                text.equals("wifi scan", ignoreCase = true)
            ) {

                runWifiScan()

            } else {

                TermuxBridge.send(text) { reply ->

                    runOnUiThread {

                        val (cleanText, imageUrl) =
                            TermuxBridge.extractImage(reply)

                        adapter.addMessage(
                            Message(cleanText, false, imageUri = imageUrl)
                        )

                        recyclerView.scrollToPosition(
                            adapter.itemCount - 1
                        )
                    }
                }
            }
        }
    }

    private fun runWifiScan() {

        if (
            ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_FINE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED
        ) {

            ActivityCompat.requestPermissions(
                this,
                arrayOf(
                    Manifest.permission.ACCESS_FINE_LOCATION
                ),
                1001
            )

            adapter.addMessage(
                Message(
                    "Nitron needs Location permission to scan nearby Wi-Fi networks.",
                    false
                )
            )

            return
        }

        WifiScanner.scan(this) { result ->

            runOnUiThread {

                adapter.addMessage(
                    Message(result, false)
                )

                recyclerView.scrollToPosition(
                    adapter.itemCount - 1
                )
            }
        }

    // Android Back button:
        // close ONLY the chat page.
        // The Nitron bubble/service stays running.
        onBackPressedDispatcher.addCallback(
            this,
            object : OnBackPressedCallback(true) {

                override fun handleOnBackPressed() {

                    hideKeyboard()

                    finish()
                }
            }
        )
    }

    private fun hideKeyboard() {

        try {

            val imm =
                getSystemService(
                    Context.INPUT_METHOD_SERVICE
                ) as InputMethodManager

            imm.hideSoftInputFromWindow(
                messageBox.windowToken,
                0
            )

        } catch (_: Exception) {
        }
    }
}
