package com.nitron.bubble.chat

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject
import java.io.File

object ChatHistoryStore {

    private val messages = mutableListOf<Message>()
    private var initialized = false
    private lateinit var storageFile: File

    fun init(context: Context) {
        if (initialized) return
        storageFile = File(context.filesDir, "chat_history.json")
        load()
        initialized = true
    }

    fun add(message: Message) {
        messages.add(message)
        save()
    }

    fun getAll(): List<Message> {
        return messages.toList()
    }

    fun clear() {
        messages.clear()
        save()
    }

    fun replaceAll(newMessages: List<Message>) {
        messages.clear()
        messages.addAll(newMessages)
        save()
    }

    private fun load() {
        try {
            if (!storageFile.exists()) return
            val text = storageFile.readText()
            if (text.isBlank()) return
            val array = JSONArray(text)
            messages.clear()
            for (i in 0 until array.length()) {
                val obj = array.getJSONObject(i)
                messages.add(
                    Message(
                        text = obj.optString("text", ""),
                        fromUser = obj.optBoolean("fromUser", false),
                        imageUri = if (obj.has("imageUri") && !obj.isNull("imageUri"))
                            obj.optString("imageUri") else null,
                        timestamp = obj.optLong("timestamp", System.currentTimeMillis())
                    )
                )
            }
        } catch (_: Exception) {
            // corrupted or missing file, start fresh
        }
    }

    private fun save() {
        try {
            val array = JSONArray()
            for (m in messages) {
                val obj = JSONObject()
                obj.put("text", m.text)
                obj.put("fromUser", m.fromUser)
                obj.put("imageUri", m.imageUri)
                obj.put("timestamp", m.timestamp)
                array.put(obj)
            }
            storageFile.writeText(array.toString())
        } catch (_: Exception) {
            // ignore write errors
        }
    }
}
