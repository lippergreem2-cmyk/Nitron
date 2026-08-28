package com.nitron.bubble

import android.content.Context
import android.graphics.PixelFormat
import android.view.Gravity
import android.view.KeyEvent
import android.view.LayoutInflater
import android.view.View
import android.view.WindowManager
import android.view.inputmethod.InputMethodManager
import android.widget.Button
import android.widget.EditText
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.nitron.bubble.chat.Message
import com.nitron.bubble.chat.MessageAdapter

class ChatWindow(private val context: Context) {

    private val windowManager =
        context.getSystemService(Context.WINDOW_SERVICE) as WindowManager

    private var chatView: View? = null

    private lateinit var recyclerView: RecyclerView
    private lateinit var messageBox: EditText
    private lateinit var sendButton: Button

    private val adapter = MessageAdapter()

    fun toggle() {
        if (chatView == null) {
            show()
        } else {
            hide()
        }
    }

    private fun show() {

        if (chatView != null) return

        chatView = LayoutInflater.from(context)
            .inflate(R.layout.chat_window, null)

        recyclerView =
            chatView!!.findViewById(R.id.recyclerView)

        messageBox =
            chatView!!.findViewById(R.id.messageBox)

        sendButton =
            chatView!!.findViewById(R.id.sendButton)

        recyclerView.layoutManager =
            LinearLayoutManager(context)

        recyclerView.adapter = adapter

        val params = WindowManager.LayoutParams(
            WindowManager.LayoutParams.MATCH_PARENT,
            WindowManager.LayoutParams.MATCH_PARENT,
            WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY,

            WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN or
                    WindowManager.LayoutParams.FLAG_ALT_FOCUSABLE_IM,

            PixelFormat.TRANSLUCENT
        )

        params.gravity = Gravity.CENTER

        windowManager.addView(chatView, params)

        // Back button closes ONLY the chat window.
        chatView!!.isFocusableInTouchMode = true
        chatView!!.requestFocus()

        chatView!!.setOnKeyListener { _, keyCode, event ->

            if (keyCode == KeyEvent.KEYCODE_BACK &&
                event.action == KeyEvent.ACTION_UP
            ) {

                hide()
                true

            } else {
                false
            }
        }

        sendButton.setOnClickListener {

            val text = messageBox.text
                .toString()
                .trim()

            if (text.isEmpty()) return@setOnClickListener

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

                WifiScanner.scan(context) { result ->

                    chatView?.post {

                        adapter.addMessage(
                            Message(result, false)
                        )

                        recyclerView.scrollToPosition(
                            adapter.itemCount - 1
                        )
                    }
                }

            } else {

                TermuxBridge.send(text) { reply ->

                    chatView?.post {

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

    fun hide() {

        chatView?.let {

            try {
                val imm = context.getSystemService(
                    Context.INPUT_METHOD_SERVICE
                ) as InputMethodManager

                imm.hideSoftInputFromWindow(
                    it.windowToken,
                    0
                )
            } catch (_: Exception) {
            }

            try {
                windowManager.removeView(it)
            } catch (_: Exception) {
            }
        }

        chatView = null
    }
}
