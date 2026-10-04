package com.nitron.bubble

import android.content.Context
import android.widget.Toast

object NitronPhoneController {

    fun execute(context: Context, command: String): Boolean {

        val service = NitronAccessibilityService.instance
            ?: return false

        val q = command.trim().lowercase()

        return when {

            q == "go home" ||
            q == "home" ||
            q == "go to home" -> {
                service.goHome()
            }

            q == "go back" ||
            q == "back" ||
            q == "press back" -> {
                service.pressBack()
            }

            q.contains("recent apps") ||
            q.contains("open recents") -> {
                service.openRecents()
            }

            q == "scroll down" ||
            q == "scroll down please" -> {
                service.scrollForward()
            }

            q == "scroll up" ||
            q == "scroll up please" -> {
                service.scrollBackward()
            }

            q.startsWith("tap ") ||
            q.startsWith("press ") -> {

                val text =
                    q.removePrefix("tap ")
                        .removePrefix("press ")
                        .trim()

                if (text.isBlank()) {
                    false
                } else {
                    service.clickText(text)
                }
            }

            q.startsWith("type ") -> {

                val text =
                    command.substringAfter(
                        "type ",
                        ""
                    ).trim()

                if (text.isBlank()) {
                    false
                } else {
                    service.typeText(text)
                }
            }

            else -> false
        }
    }
}
