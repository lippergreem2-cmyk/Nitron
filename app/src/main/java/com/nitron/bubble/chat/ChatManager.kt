package com.nitron.bubble.chat

import com.nitron.bubble.TermuxBridge

class ChatManager {

    interface ChatListener {
        fun onReply(reply: String)
    }

    private var listener: ChatListener? = null

    fun setListener(chatListener: ChatListener) {
        listener = chatListener
    }

    fun sendMessage(message: String) {

        if (message.isBlank()) return

        TermuxBridge.send(message) { reply ->
            listener?.onReply(reply)
        }
    }
}
