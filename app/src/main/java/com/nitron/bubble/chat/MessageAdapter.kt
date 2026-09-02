package com.nitron.bubble.chat

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Intent
import android.graphics.Color
import android.graphics.Typeface
import android.net.Uri
import android.text.Spannable
import android.text.SpannableString
import android.text.style.ForegroundColorSpan
import android.view.Gravity
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ImageButton
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import androidx.recyclerview.widget.RecyclerView
import com.nitron.bubble.FullTextActivity
import com.nitron.bubble.R
import java.net.HttpURLConnection
import java.net.URL
import kotlin.concurrent.thread

class MessageAdapter :
    RecyclerView.Adapter<MessageAdapter.MessageViewHolder>() {

    private val messages = mutableListOf<Message>()

    class MessageViewHolder(view: View) :
        RecyclerView.ViewHolder(view) {

        val messageText: TextView =
            view.findViewById(R.id.messageText)

        val messageImage: ImageView =
            view.findViewById(R.id.messageImage)

        val copyButton: Button =
            view.findViewById(R.id.copyButton)

        val expandButton: ImageButton =
            view.findViewById(R.id.expandButton)

        val container: View =
            view.findViewById(R.id.messageContainer)
    }

    // ============================================================
    // CODE DETECTION
    // ============================================================

    private fun isLikelyCode(text: String): Boolean {

        if (text.contains("```")) {
            return true
        }

        val indicators = listOf(
            "def ",
            "class ",
            "import ",
            "from ",
            "return ",
            "if ",
            "elif ",
            "else:",
            "for ",
            "while ",
            "try:",
            "except ",
            "public ",
            "private ",
            "protected ",
            "static ",
            "void ",
            "function ",
            "console.log",
            "fun ",
            "val ",
            "var ",
            "#include",
            "package ",
            "SELECT ",
            "INSERT ",
            "UPDATE ",
            "DELETE ",
            "print(",
            "println(",
            "System.out",
            "=>",
            "->",
            "</",
            "/>"
        )

        val lower = text.lowercase()

        val hasIndicator =
            indicators.any {
                lower.contains(it.lowercase())
            }

        val symbolCount =
            text.count {
                it == '{' ||
                it == '}' ||
                it == ';' ||
                it == '(' ||
                it == ')'
            }

        val codeLinePrefixes = listOf(
            "def ",
            "class ",
            "import ",
            "from ",
            "return ",
            "if ",
            "elif ",
            "else:",
            "for ",
            "while ",
            "try:",
            "except ",
            "fun ",
            "val ",
            "var ",
            "const ",
            "let "
        )

        val multipleCodeLines =
            text.lines().count { line ->
                codeLinePrefixes.any { prefix ->
                    line.trim().startsWith(prefix)
                }
            } >= 2

        return hasIndicator ||
               symbolCount >= 4 ||
               multipleCodeLines
    }

    // ============================================================
    // CODE BLOCK DETECTION
    // ============================================================

    private fun hasFencedCode(text: String): Boolean {
        return text.contains("```")
    }

    private fun extractCodeLanguage(text: String): String {

        val regex = Regex(
            """```([A-Za-z0-9_+#.-]*)"""
        )

        val match = regex.find(text)

        return match?.groupValues?.getOrNull(1)
            ?.lowercase()
            ?: ""
    }

    // ============================================================
    // SIMPLE SYNTAX COLORING
    // ============================================================

    private fun colorCode(text: String): SpannableString {

        val result = SpannableString(text)

        // Generated code is displayed entirely in green.
        result.setSpan(
            ForegroundColorSpan(Color.rgb(80, 220, 120)),
            0,
            text.length,
            Spannable.SPAN_EXCLUSIVE_EXCLUSIVE
        )

        val keywordColor =
            Color.rgb(80, 220, 120)

        val stringColor =
            Color.rgb(80, 220, 120)

        val commentColor =
            Color.rgb(80, 220, 120)

        val numberColor =
            Color.rgb(80, 220, 120)

        val keywords = listOf(
            "def",
            "class",
            "return",
            "if",
            "else",
            "elif",
            "for",
            "while",
            "in",
            "is",
            "not",
            "and",
            "or",
            "try",
            "except",
            "finally",
            "raise",
            "import",
            "from",
            "as",
            "with",
            "lambda",
            "yield",
            "async",
            "await",
            "public",
            "private",
            "protected",
            "static",
            "void",
            "new",
            "fun",
            "val",
            "var",
            "const",
            "let",
            "function",
            "package",
            "interface",
            "extends",
            "implements"
        )

        // Keywords
        for (keyword in keywords) {

            val regex =
                Regex("""\b${Regex.escape(keyword)}\b""")

            for (match in regex.findAll(text)) {

                result.setSpan(
                    ForegroundColorSpan(keywordColor),
                    match.range.first,
                    match.range.last + 1,
                    Spannable.SPAN_EXCLUSIVE_EXCLUSIVE
                )
            }
        }

        // Strings
        val stringRegex =
            Regex("""(["'])(?:\\.|(?!\1).)*\1""")

        for (match in stringRegex.findAll(text)) {

            result.setSpan(
                ForegroundColorSpan(stringColor),
                match.range.first,
                match.range.last + 1,
                Spannable.SPAN_EXCLUSIVE_EXCLUSIVE
            )
        }

        // Numbers
        val numberRegex =
            Regex("""\b\d+(?:\.\d+)?\b""")

        for (match in numberRegex.findAll(text)) {

            result.setSpan(
                ForegroundColorSpan(numberColor),
                match.range.first,
                match.range.last + 1,
                Spannable.SPAN_EXCLUSIVE_EXCLUSIVE
            )
        }

        // Python / shell style comments
        val commentRegex =
            Regex("""(?m)^\s*#.*$""")

        for (match in commentRegex.findAll(text)) {

            result.setSpan(
                ForegroundColorSpan(commentColor),
                match.range.first,
                match.range.last + 1,
                Spannable.SPAN_EXCLUSIVE_EXCLUSIVE
            )
        }

        return result
    }

    // ============================================================
    // VIEW CREATION
    // ============================================================

    override fun onCreateViewHolder(
        parent: ViewGroup,
        viewType: Int
    ): MessageViewHolder {

        val view =
            LayoutInflater.from(parent.context)
                .inflate(
                    R.layout.message_item,
                    parent,
                    false
                )

        return MessageViewHolder(view)
    }

    // ============================================================
    // BIND MESSAGE
    // ============================================================

    override fun onBindViewHolder(
        holder: MessageViewHolder,
        position: Int
    ) {

        val message = messages[position]

        val isCode =
            !message.fromUser &&
            isLikelyCode(message.text)

        // --------------------------------------------------------
        // TEXT
        // --------------------------------------------------------

        if (message.text.isBlank()) {

            holder.messageText.visibility =
                View.GONE

        } else {

            holder.messageText.visibility =
                View.VISIBLE

            if (message.fromUser) {

                holder.messageText.text =
                    message.text

                holder.messageText.setBackgroundResource(
                    R.drawable.user_message_bg
                )

                holder.messageText.setTextColor(
                    holder.itemView.context.getColor(
                        R.color.user_text
                    )
                )

                holder.messageText.typeface =
                    Typeface.DEFAULT

            } else if (isCode) {

                // ------------------------------------------------
                // CODE MESSAGE
                // ------------------------------------------------

                holder.messageText.setBackgroundResource(
                    R.drawable.nitron_code_bg
                )

                holder.messageText.typeface =
                    Typeface.MONOSPACE

                holder.messageText.setTextColor(
                    Color.rgb(230, 230, 230)
                )

                holder.messageText.setPadding(
                    14,
                    10,
                    14,
                    10
                )

                val language =
                    extractCodeLanguage(message.text)

                val cleanedCode =
                    message.text
                        .replace(
                            Regex("""```[A-Za-z0-9_+#.-]*"""),
                            ""
                        )
                        .replace(
                            "```",
                            ""
                        )
                        .trim()

                val colored =
                    colorCode(cleanedCode)

                holder.messageText.text =
                    colored

            } else {

                // ------------------------------------------------
                // NORMAL NITRON MESSAGE
                // ------------------------------------------------

                holder.messageText.text =
                    message.text

                holder.messageText.setBackgroundResource(
                    R.drawable.nitron_message_bg
                )

                holder.messageText.setTextColor(
                    holder.itemView.context.getColor(
                        R.color.nitron_blue
                    )
                )

                holder.messageText.typeface =
                    Typeface.DEFAULT

                holder.messageText.setPadding(
                    10,
                    5,
                    10,
                    5
                )
            }
        }

        // --------------------------------------------------------
        // COPY
        // --------------------------------------------------------

        if (
            message.text.isNotBlank() &&
            !message.fromUser
        ) {

            holder.copyButton.visibility =
                View.VISIBLE

            holder.copyButton.text =
                if (isCode) {
                    "Copy Code"
                } else {
                    "Copy"
                }

            holder.copyButton.setOnClickListener {

                val clipboard =
                    holder.itemView.context
                        .getSystemService(
                            ClipboardManager::class.java
                        )

                clipboard.setPrimaryClip(
                    ClipData.newPlainText(
                        "Nitron message",
                        message.text
                    )
                )

                Toast.makeText(
                    holder.itemView.context,
                    if (isCode)
                        "Code copied"
                    else
                        "Copied",
                    Toast.LENGTH_SHORT
                ).show()
            }

        } else {

            holder.copyButton.visibility =
                View.GONE
        }

        // --------------------------------------------------------
        // EXPAND
        // --------------------------------------------------------

        if (
            !message.fromUser &&
            message.text.isNotBlank() &&
            (
                isCode ||
                message.text.length > 300
            )
        ) {

            holder.expandButton.visibility =
                View.VISIBLE

            holder.expandButton.setOnClickListener {

                val intent =
                    Intent(
                        holder.itemView.context,
                        FullTextActivity::class.java
                    )

                intent.putExtra(
                    "full_text",
                    message.text
                )

                intent.putExtra(
                    "is_code",
                    isCode
                )

                holder.itemView.context
                    .startActivity(intent)
            }

        } else {

            holder.expandButton.visibility =
                View.GONE
        }

        // --------------------------------------------------------
        // IMAGE
        // --------------------------------------------------------

        if (message.imageUri != null) {

            holder.messageImage.visibility =
                View.VISIBLE

            holder.messageImage
                .setImageDrawable(null)

            holder.messageImage.tag =
                message.imageUri

            if (
                message.imageUri.startsWith(
                    "http://"
                ) ||
                message.imageUri.startsWith(
                    "https://"
                )
            ) {

                val targetUrl =
                    message.imageUri

                thread {

                    try {

                        val connection =
                            URL(targetUrl)
                                .openConnection()
                                as HttpURLConnection

                        connection.connectTimeout =
                            10000

                        connection.readTimeout =
                            15000

                        val bytes =
                            connection.inputStream
                                .use {
                                    it.readBytes()
                                }

                        val bitmap =
                            android.graphics
                                .BitmapFactory
                                .decodeByteArray(
                                    bytes,
                                    0,
                                    bytes.size
                                )

                        connection.disconnect()

                        holder.messageImage.post {

                            if (
                                holder.messageImage.tag ==
                                targetUrl &&
                                bitmap != null
                            ) {

                                holder.messageImage
                                    .setImageBitmap(
                                        bitmap
                                    )
                            }
                        }

                    } catch (_: Exception) {
                        // Keep image blank if loading fails.
                    }
                }

            } else {

                holder.messageImage.setImageURI(
                    Uri.parse(
                        message.imageUri
                    )
                )
            }

        } else {

            holder.messageImage.visibility =
                View.GONE
        }

        // --------------------------------------------------------
        // MESSAGE POSITION
        // --------------------------------------------------------

        val params =
            holder.container.layoutParams
                as ViewGroup.MarginLayoutParams

        params.marginStart = 0
        params.marginEnd = 0

        holder.container.layoutParams =
            params

        if (message.fromUser) {

            (holder.container as android.widget.LinearLayout)
                .gravity = Gravity.END

        } else {

            (holder.container as android.widget.LinearLayout)
                .gravity = Gravity.START
        }
    }

    // ============================================================
    // DATA
    // ============================================================

    override fun getItemCount(): Int {
        return messages.size
    }

    fun addMessage(message: Message) {

        messages.add(message)

        notifyItemInserted(
            messages.size - 1
        )
    }

    fun getMessages(): List<Message> {
        return messages.toList()
    }

    fun clearMessages() {

        messages.clear()

        notifyDataSetChanged()
    }
}
