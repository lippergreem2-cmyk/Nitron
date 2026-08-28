package com.nitron.bubble.chat

import android.net.Uri
import android.content.ClipboardManager
import android.content.ClipData
import android.content.Intent
import android.graphics.Color
import android.graphics.Typeface
import android.widget.Toast
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.view.Gravity
import android.widget.ImageView
import android.widget.ImageButton
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.nitron.bubble.R
import com.nitron.bubble.FullTextActivity
import android.graphics.BitmapFactory
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
        val copyButton: android.widget.Button =
            view.findViewById(R.id.copyButton)

        val expandButton: ImageButton =
            view.findViewById(R.id.expandButton)

        val container: View =
            view.findViewById(R.id.messageContainer)
    }

    private fun isLikelyCode(text: String): Boolean {
        if (text.contains("```")) return true

        val indicators = listOf(
            "def ", "class ", "import ", "function ", "return ",
            "public ", "private ", "void ", "console.log", "fun ",
            "val ", "var ", "#include", "SELECT ", "print(", "=>",
            "</", "/>"
        )

        val symbolCount = text.count { it == '{' || it == '}' || it == ';' }
        val hasIndicator = indicators.any { text.contains(it) }

        return hasIndicator || symbolCount > 3
    }

    override fun onCreateViewHolder(
        parent: ViewGroup,
        viewType: Int
    ): MessageViewHolder {

        val view = LayoutInflater.from(parent.context)
            .inflate(
                R.layout.message_item,
                parent,
                false
            )

        return MessageViewHolder(view)
    }

    override fun onBindViewHolder(
        holder: MessageViewHolder,
        position: Int
    ) {

        val message = messages[position]
        val isCode = !message.fromUser && isLikelyCode(message.text)

        // TEXT
        if (message.text.isBlank()) {

            holder.messageText.visibility = View.GONE

        } else {

            holder.messageText.visibility = View.VISIBLE
            holder.messageText.text = message.text

            if (message.fromUser) {

                holder.messageText.setBackgroundResource(
                    R.drawable.user_message_bg
                )

                holder.messageText.setTextColor(
                    holder.itemView.context.getColor(
                        R.color.user_text
                    )
                )

                holder.messageText.typeface = Typeface.DEFAULT

            } else if (isCode) {

                holder.messageText.setBackgroundResource(
                    R.drawable.nitron_code_bg
                )

                holder.messageText.setTextColor(
                    Color.parseColor("#E0E0E0")
                )

                holder.messageText.typeface = Typeface.MONOSPACE

            } else {

                holder.messageText.setBackgroundResource(
                    R.drawable.nitron_message_bg
                )

                holder.messageText.setTextColor(
                    holder.itemView.context.getColor(
                        R.color.nitron_blue
                    )
                )

                holder.messageText.typeface = Typeface.DEFAULT
            }
        }

        // COPY
        if (message.text.isNotBlank() && !message.fromUser) {
            holder.copyButton.visibility = View.VISIBLE
            holder.copyButton.text = if (isCode) "Copy Code" else "Copy"

            holder.copyButton.setOnClickListener {
                val clipboard =
                    holder.itemView.context.getSystemService(
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
                    if (isCode) "Code copied" else "Copied",
                    Toast.LENGTH_SHORT
                ).show()
            }
        } else {
            holder.copyButton.visibility = View.GONE
        }

        // EXPAND (long or code messages, Nitron only)
        if (!message.fromUser && message.text.isNotBlank() &&
            (isCode || message.text.length > 300)) {

            holder.expandButton.visibility = View.VISIBLE

            holder.expandButton.setOnClickListener {
                val intent = Intent(
                    holder.itemView.context,
                    FullTextActivity::class.java
                )
                intent.putExtra("full_text", message.text)
                intent.putExtra("is_code", isCode)
                holder.itemView.context.startActivity(intent)
            }
        } else {
            holder.expandButton.visibility = View.GONE
        }

        // IMAGE
        if (message.imageUri != null) {

            holder.messageImage.visibility = View.VISIBLE
            holder.messageImage.setImageDrawable(null)
            holder.messageImage.tag = message.imageUri

            if (message.imageUri.startsWith("http://") ||
                message.imageUri.startsWith("https://")) {

                val targetUrl = message.imageUri

                thread {
                    try {
                        val connection =
                            URL(targetUrl).openConnection()
                                as HttpURLConnection

                        connection.connectTimeout = 10000
                        connection.readTimeout = 15000

                        val bytes =
                            connection.inputStream.use {
                                it.readBytes()
                            }

                        val bitmap =
                            BitmapFactory.decodeByteArray(
                                bytes, 0, bytes.size
                            )

                        connection.disconnect()

                        holder.messageImage.post {
                            if (holder.messageImage.tag == targetUrl && bitmap != null) {
                                holder.messageImage.setImageBitmap(bitmap)
                            }
                        }

                    } catch (_: Exception) {
                        // silently fail; image stays blank
                    }
                }

            } else {

                holder.messageImage.setImageURI(
                    Uri.parse(message.imageUri)
                )
            }

        } else {

            holder.messageImage.visibility = View.GONE
        }

        // USER / NITRON POSITION
        val params =
            holder.container.layoutParams
                as ViewGroup.MarginLayoutParams

        params.marginStart = 0
        params.marginEnd = 0

        holder.container.layoutParams = params

        if (message.fromUser) {
            (holder.container as android.widget.LinearLayout).gravity = Gravity.END
        } else {
            (holder.container as android.widget.LinearLayout).gravity = Gravity.START
        }
    }

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
