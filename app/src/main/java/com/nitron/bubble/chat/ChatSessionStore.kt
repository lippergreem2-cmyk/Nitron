package com.nitron.bubble.chat

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject
import java.io.File

data class ChatSession(
    val id: String,
    val title: String,
    val timestamp: Long,
    val messages: List<Message>
)

object ChatSessionStore {

    private val sessions = mutableListOf<ChatSession>()
    private var initialized = false
    private lateinit var storageFile: File

    fun init(context: Context) {
        if (initialized) return
        storageFile = File(context.filesDir, "chat_sessions.json")
        load()
        initialized = true
    }

    fun getSessions(): List<ChatSession> {
        return sessions.sortedByDescending { it.timestamp }
    }

    fun archiveCurrentChat(context: Context) {
        val current = ChatHistoryStore.getAll()
        if (current.isEmpty()) return

        val firstUserMessage = current.firstOrNull { it.fromUser }?.text ?: current.first().text

        val title = firstUserMessage
            .trim()
            .split(Regex("\\s+"))
            .take(6)
            .joinToString(" ")
            .take(40)
            .ifBlank { "New chat" }

        val session = ChatSession(
            id = System.currentTimeMillis().toString(),
            title = title,
            timestamp = System.currentTimeMillis(),
            messages = current
        )

        sessions.add(0, session)
        save()
    }

    fun loadSession(context: Context, id: String): List<Message>? {
        val session = sessions.find { it.id == id } ?: return null
        sessions.remove(session)
        save()
        ChatHistoryStore.replaceAll(session.messages)
        return session.messages
    }

    fun deleteSession(id: String) {
        sessions.removeAll { it.id == id }
        save()
    }

    private fun load() {
        try {
            if (!storageFile.exists()) return
            val text = storageFile.readText()
            if (text.isBlank()) return
            val array = JSONArray(text)
            sessions.clear()
            for (i in 0 until array.length()) {
                val obj = array.getJSONObject(i)
                val msgsArray = obj.getJSONArray("messages")
                val msgs = mutableListOf<Message>()
                for (j in 0 until msgsArray.length()) {
                    val m = msgsArray.getJSONObject(j)
                    msgs.add(
                        Message(
                            text = m.optString("text", ""),
                            fromUser = m.optBoolean("fromUser", false),
                            imageUri = if (m.has("imageUri") && !m.isNull("imageUri")) m.optString("imageUri") else null,
                            timestamp = m.optLong("timestamp", System.currentTimeMillis())
                        )
                    )
                }
                sessions.add(
                    ChatSession(
                        id = obj.optString("id", System.currentTimeMillis().toString()),
                        title = obj.optString("title", "Chat"),
                        timestamp = obj.optLong("timestamp", System.currentTimeMillis()),
                        messages = msgs
                    )
                )
            }
        } catch (_: Exception) {
        }
    }

    private fun save() {
        try {
            val array = JSONArray()
            for (s in sessions) {
                val obj = JSONObject()
                obj.put("id", s.id)
                obj.put("title", s.title)
                obj.put("timestamp", s.timestamp)
                val msgsArray = JSONArray()
                for (m in s.messages) {
                    val mo = JSONObject()
                    mo.put("text", m.text)
                    mo.put("fromUser", m.fromUser)
                    mo.put("imageUri", m.imageUri)
                    mo.put("timestamp", m.timestamp)
                    msgsArray.put(mo)
                }
                obj.put("messages", msgsArray)
                array.put(obj)
            }
            storageFile.writeText(array.toString())
        } catch (_: Exception) {
        }
    }
}
