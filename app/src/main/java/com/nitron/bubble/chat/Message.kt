package com.nitron.bubble.chat

data class Message(
    val text: String = "",
    val fromUser: Boolean,
    val imageUri: String? = null,
    val timestamp: Long = System.currentTimeMillis()
)
