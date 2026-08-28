package com.nitron.bubble

import android.content.Context
import android.content.Intent
import android.view.View
import android.widget.PopupMenu

class BubbleMenu(
    private val context: Context
) {

    fun show(anchor: View) {

        val menu = PopupMenu(context, anchor)

        menu.menu.add("💬 Open Chat")
        menu.menu.add("🎤 Voice Mode")
        menu.menu.add("⚙ Settings")
        menu.menu.add("❌ Close Nitron")

        menu.setOnMenuItemClickListener {

            when (it.title.toString()) {

                "💬 Open Chat" -> {
                    val chat = ChatWindow(context)
                    chat.toggle()
                    true
                }

                "🎤 Voice Mode" -> {
                    TermuxBridge.send("voice") { }
                    true
                }

                "⚙ Settings" -> {

                    val intent = Intent(
                        context,
                        SettingsActivity::class.java
                    )

                    intent.addFlags(
                        Intent.FLAG_ACTIVITY_NEW_TASK
                    )

                    context.startActivity(intent)

                    true
                }

                "❌ Close Nitron" -> {

                    context.stopService(
                        Intent(
                            context,
                            BubbleService::class.java
                        )
                    )

                    true
                }

                else -> false
            }
        }

        menu.show()
    }
}
