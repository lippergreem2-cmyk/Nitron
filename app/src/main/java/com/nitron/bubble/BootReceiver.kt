package com.nitron.bubble

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.os.Build

class BootReceiver : BroadcastReceiver() {

    override fun onReceive(
        context: Context,
        intent: Intent?
    ) {

        if (intent?.action != Intent.ACTION_BOOT_COMPLETED) {
            return
        }

        val prefs = context.getSharedPreferences(
            "nitron_settings",
            Context.MODE_PRIVATE
        )

        val autoStart = prefs.getBoolean(
            "autostart",
            true
        )

        val bubbleEnabled = prefs.getBoolean(
            "bubble",
            true
        )

        if (!autoStart || !bubbleEnabled) {
            return
        }

        val serviceIntent = Intent(
            context,
            NotificationService::class.java
        )

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            context.startForegroundService(serviceIntent)
        } else {
            context.startService(serviceIntent)
        }
    }
}
