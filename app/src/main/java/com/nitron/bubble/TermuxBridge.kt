package com.nitron.bubble

import android.content.Context

import org.json.JSONObject
import com.google.firebase.auth.FirebaseAuth
import com.google.android.gms.tasks.Tasks
import java.io.BufferedReader
import java.io.InputStreamReader
import java.io.OutputStreamWriter
import java.net.HttpURLConnection
import java.net.URL
import kotlin.concurrent.thread

object TermuxBridge {

    private lateinit var appContext: Context

    fun initialize(context: Context) {
        appContext = context.applicationContext
    }


    /*
     * ============================================================
     * IMAGE MARKER PARSING
     * ============================================================
     */
    fun extractImage(reply: String): Pair<String, String?> {

        val startTag = "[NITRON_IMG]"
        val endTag = "[/NITRON_IMG]"

        if (!reply.startsWith(startTag)) {
            return Pair(reply, null)
        }

        val endIdx = reply.indexOf(endTag)

        if (endIdx == -1) {
            return Pair(reply, null)
        }

        val url = reply.substring(startTag.length, endIdx)
        val text = reply.substring(endIdx + endTag.length)

        return Pair(text, url)
    }


    /*
     * ============================================================
     * NITRON SERVER
     * ============================================================
     *
     * Change this one address when Nitron is deployed online.
     *
     * Local development:
     * http://127.0.0.1:8000
     *
     * Production example:
     * https://api.your-nitron-domain.com
     */
    private const val DEFAULT_SERVER_BASE_URL =
        "https://bowl-kate-engaged-armor.trycloudflare.com"

    private fun serverBaseUrl(): String {
        return appContext
            .getSharedPreferences(
                "nitron_server",
                Context.MODE_PRIVATE
            )
            .getString(
                "server_url",
                DEFAULT_SERVER_BASE_URL
            )
            ?.trim()
            ?.trimEnd('/')
            ?.ifEmpty { DEFAULT_SERVER_BASE_URL }
            ?: DEFAULT_SERVER_BASE_URL
    }

    private fun serverUrl(path: String): String {
        return serverBaseUrl() + "/" + path.trimStart('/')
    }

    private fun commandUrl() =
        serverUrl("command")

    private fun learnImageUrl() =
        serverUrl("learn-image")

    private fun analyzeImageUrl() =
        serverUrl("analyze-image")

    /*
     * ============================================================
     * RESPONSE FORMATTER
     * ============================================================
     *
     * Important:
     * Generated source code must NOT be reformatted.
     *
     * We preserve:
     * - indentation
     * - multiple spaces
     * - blank lines
     * - braces
     * - HTML/CSS/JS/Python formatting
     */
    private fun formatReply(raw: String): String {

        val text = raw.trim()

        if (text.isEmpty()) {
            return ""
        }

        /*
         * --------------------------------------------------------
         * JSON RESPONSE
         * --------------------------------------------------------
         */
        try {

            val json = JSONObject(text)

            if (json.has("message")) {

                val message =
                    json.optString("message", "").trim()

                val topic =
                    json.optString("topic", "").trim()

                val learned =
                    json.optBoolean("learned", false)

                val imageLearned =
                    json.optBoolean("image_learned", false)

                val detectedTopics =
                    json.optJSONArray("detected_topics")

                val imageMetadata =
                    json.optJSONObject("image_metadata")

                val generated =
                    json.optBoolean("generated", false)

                val project =
                    json.optJSONObject("project")

                val output =
                    StringBuilder()

                /*
                 * ------------------------------------------------
                 * Main response
                 * ------------------------------------------------
                 */
                if (message.isNotEmpty()) {

                    /*
                     * Do NOT run generated-project messages
                     * through cleanSentence().
                     *
                     * The backend message contains source code.
                     */
                    output.append(message)
                    output.append("\n")
                }

                /*
                 * ------------------------------------------------
                 * Learned topic
                 * ------------------------------------------------
                 */
                if (learned && topic.isNotEmpty()) {

                    output.append("\n")
                    output.append("Topic\n")
                    output.append(prettyTopic(topic))
                    output.append("\n")
                }

                /*
                 * ------------------------------------------------
                 * Generated project
                 *
                 * This is retained for structured JSON responses
                 * where project information is supplied separately.
                 * ------------------------------------------------
                 */
                if (generated && project != null) {

                    output.append("\n")

                    val projectName =
                        project.optString("name", "").trim()

                    val projectType =
                        project.optString("project_type", "").trim()

                    val language =
                        project.optString("language", "").trim()

                    val directory =
                        project.optString("directory", "").trim()

                    val files =
                        project.optJSONArray("files")

                    if (projectName.isNotEmpty()) {

                        output.append("Name\n")
                        output.append(projectName)
                        output.append("\n")
                    }

                    if (projectType.isNotEmpty()) {

                        output.append("\n")
                        output.append("Type\n")
                        output.append(
                            prettyTopic(projectType)
                        )
                        output.append("\n")
                    }

                    if (language.isNotEmpty()) {

                        output.append("\n")
                        output.append("Language\n")
                        output.append(
                            language.uppercase()
                        )
                        output.append("\n")
                    }

                    if (files != null && files.length() > 0) {

                        output.append("\n")
                        output.append("Files\n")

                        for (i in 0 until files.length()) {

                            val file =
                                files.optJSONObject(i)

                            if (file != null) {

                                val path =
                                    file.optString(
                                        "path",
                                        ""
                                    ).trim()

                                if (path.isNotEmpty()) {

                                    output.append("• ")
                                    output.append(path)
                                    output.append("\n")
                                }
                            }
                        }
                    }

                    if (directory.isNotEmpty()) {

                        output.append("\n")
                        output.append("Location\n")
                        output.append(directory)
                        output.append("\n")
                    }
                }

                /*
                 * ------------------------------------------------
                 * Image learning
                 * ------------------------------------------------
                 */
                if (imageLearned) {

                    output.append("\n")
                    output.append("What I detected\n")

                    if (detectedTopics != null) {

                        for (i in 0 until detectedTopics.length()) {

                            val item =
                                detectedTopics.optString(i)

                            if (item.isNotBlank()) {

                                output.append("• ")
                                output.append(
                                    prettyTopic(item)
                                )
                                output.append("\n")
                            }
                        }
                    }

                    if (imageMetadata != null) {

                        val width =
                            imageMetadata.optInt(
                                "width",
                                0
                            )

                        val height =
                            imageMetadata.optInt(
                                "height",
                                0
                            )

                        val format =
                            imageMetadata.optString(
                                "format",
                                ""
                            )

                        if (width > 0 && height > 0) {

                            output.append("\n")
                            output.append("Image size\n")
                            output.append(
                                "${width} × ${height}"
                            )
                            output.append("\n")
                        }

                        if (format.isNotBlank()) {

                            output.append("Format\n")
                            output.append(format)
                            output.append("\n")
                        }
                    }
                }

                /*
                 * Preserve source formatting.
                 */
                return cleanFinalText(
                    output.toString()
                )
            }

        } catch (_: Exception) {

            /*
             * Not JSON.
             * Treat it as ordinary backend text.
             */
        }

        return cleanFinalText(text)
    }

    /*
     * ============================================================
     * SENTENCE CLEANER
     * ============================================================
     *
     * Used only for normal conversational text.
     *
     * Never use this on generated source code.
     */
    private fun cleanSentence(value: String): String {

        var text = value.trim()

        text = text
            .replace("True", "")
            .replace("False", "")
            .replace("None", "")

        text = text.replace(
            Regex("[ \\t]+"),
            " "
        )

        text = text.replace(
            Regex(",\\s*,+"),
            ","
        )

        text = text.replace(
            Regex("\\.{2,}"),
            "."
        )

        text = text.replace(
            Regex("\\s+([,.!?])"),
            "$1"
        )

        return text.trim()
    }

    /*
     * ============================================================
     * TOPIC FORMATTER
     * ============================================================
     */
    private fun prettyTopic(topic: String): String {

        if (topic.isBlank()) {
            return ""
        }

        return topic
            .trim()
            .replace("_", " ")
            .split(" ")
            .joinToString(" ") { word ->

                if (word.isEmpty()) {
                    ""
                } else {

                    word.substring(
                        0,
                        1
                    ).uppercase() +
                            word.substring(
                                1
                            ).lowercase()
                }
            }
    }

    /*
     * ============================================================
     * FINAL CLEANUP
     * ============================================================
     *
     * IMPORTANT:
     *
     * We do NOT:
     * - collapse spaces
     * - remove braces
     * - modify indentation
     *
     * This allows source code to remain readable.
     */
    private fun cleanFinalText(value: String): String {

        var text = value.trim()

        /*
         * Only remove excessive blank lines.
         *
         * Do not alter spaces inside lines.
         */
        text = text.replace(
            Regex("\\n{4,}"),
            "\n\n\n"
        )

        /*
         * Remove trailing whitespace only.
         *
         * Leading indentation remains untouched.
         */
        text = text.lines()
            .joinToString("\n") {
                it.trimEnd()
            }

        return text.trim()
    }

    /*
     * ============================================================
     * TEXT MESSAGE
     * ============================================================
     */
    fun send(
        message: String,
        callback: (String) -> Unit
    ) {

        thread {

            try {

                val url =
                    URL(commandUrl())

                val connection =
                    url.openConnection()
                            as HttpURLConnection

                connection.requestMethod =
                    "POST"

                connection.doOutput =
                    true

                connection.connectTimeout =
                    5000

                connection.readTimeout =
                    100000

                connection.setRequestProperty(
                    "Content-Type",
                    "application/json; charset=UTF-8"
                )

                // Use the signed-in Firebase account when available.
                // The backend can verify this token instead of trusting
                // the locally stored user_id.
                try {
                    val firebaseUser =
                        FirebaseAuth.getInstance().currentUser

                    if (firebaseUser != null) {
                        val tokenResult =
                            Tasks.await(
                                firebaseUser.getIdToken(false)
                            )

                        val token = tokenResult.token

                        if (!token.isNullOrBlank()) {
                            connection.setRequestProperty(
                                "Authorization",
                                "Bearer $token"
                            )
                        }
                    }
                } catch (e: Exception) {
                    println(
                        "[AUTH] Firebase token unavailable: ${e.message}"
                    )
                }

                val prefs =
                    appContext.getSharedPreferences(
                        "nitron_user",
                        Context.MODE_PRIVATE
                    )

                val savedUserId =
                    prefs.getString("user_id", null)

                val json =
                    JSONObject()
                        .put(
                            "message",
                            message
                        )

                if (!savedUserId.isNullOrBlank()) {
                    json.put("user_id", savedUserId)
                }

                OutputStreamWriter(
                    connection.outputStream,
                    Charsets.UTF_8
                ).use { writer ->

                    writer.write(
                        json.toString()
                    )

                    writer.flush()
                }

                val inputStream =
                    if (
                        connection.responseCode
                        in 200..299
                    ) {
                        connection.inputStream
                    } else {
                        connection.errorStream
                    }

                val reply =
                    BufferedReader(
                        InputStreamReader(
                            inputStream,
                            Charsets.UTF_8
                        )
                    ).use {
                        it.readText()
                    }

                var cleanReply = reply
                var imageUrl: String? = null

                try {

                    val responseJson =
                        JSONObject(reply)

                    if (responseJson.has("user_id")) {

                        val userId =
                            responseJson.optString(
                                "user_id",
                                ""
                            )

                        if (userId.isNotBlank()) {

                            prefs.edit()
                                .putString(
                                    "user_id",
                                    userId
                                )
                                .apply()

                            println(
                                "[USER] Saved user ID: $userId"
                            )
                        }
                    }

                    if (responseJson.has("response")) {
                        cleanReply =
                            responseJson.getString("response")
                    }

                    if (responseJson.has("image_url")) {

                        val u =
                            responseJson.optString(
                                "image_url",
                                ""
                            )

                        if (u.isNotBlank()) {
                            imageUrl = u
                        }
                    }

                } catch (_: Exception) {

                    cleanReply = reply
                }

                val finalReply =
                    if (imageUrl != null) {

                        "[NITRON_IMG]$imageUrl[/NITRON_IMG]" +
                                formatReply(cleanReply)

                    } else {

                        formatReply(cleanReply)
                    }

                callback(finalReply)

                connection.disconnect()

            } catch (e: Exception) {

                callback(
                    "Nitron is offline\n\n${e.message}"
                )
            }
        }
    }

    /*
     * ============================================================
     * IMAGE MESSAGE
     * ============================================================
     */
    fun sendImage(
        base64Image: String,
        filename: String,
        question: String = "",
        callback: (String) -> Unit
    ) {

        thread {

            try {

                val url =
                    URL(analyzeImageUrl())

                val connection =
                    url.openConnection()
                            as HttpURLConnection

                connection.requestMethod =
                    "POST"

                connection.doOutput =
                    true

                connection.connectTimeout =
                    10000

                connection.readTimeout =
                    30000

                connection.setRequestProperty(
                    "Content-Type",
                    "application/json; charset=UTF-8"
                )

                val json =
                    JSONObject()
                        .put(
                            "image",
                            base64Image
                        )
                        .put(
                            "filename",
                            filename
                        )
                        .put(
                            "question",
                            question
                        )

                OutputStreamWriter(
                    connection.outputStream,
                    Charsets.UTF_8
                ).use { writer ->

                    writer.write(
                        json.toString()
                    )

                    writer.flush()
                }

                val inputStream =
                    if (
                        connection.responseCode
                        in 200..299
                    ) {
                        connection.inputStream
                    } else {
                        connection.errorStream
                    }

                val reply =
                    BufferedReader(
                        InputStreamReader(
                            inputStream,
                            Charsets.UTF_8
                        )
                    ).use {
                        it.readText()
                    }

                val response =
                    try {

                        val responseJson =
                            JSONObject(reply)

                        if (
                            responseJson.has(
                                "response"
                            )
                        ) {

                            responseJson.getString(
                                "response"
                            )

                        } else {

                            reply
                        }

                    } catch (_: Exception) {

                        reply
                    }

                callback(
                    formatReply(response)
                )

                connection.disconnect()

            } catch (e: Exception) {

                callback(
                    "Could not send picture to Nitron\n\n${e.message}"
                )
            }
        }
    }
}
