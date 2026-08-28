package com.nitron.bubble

import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Build
import android.provider.Settings

class BubbleOverlay(private val context: Context) {

    fun hasPermission(): Boolean {
        return Build.VERSION.SDK_INT < Build.VERSION_CODES.M ||
                Settings.canDrawOverlays(context)
    }

    fun requestPermission() {
        if (!hasPermission()) {
            val intent = Intent(
                Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                Uri.parse("package:${context.packageName}")
            )

            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            context.startActivity(intent)
        }
    }

    fun show(): Boolean {

        if (!hasPermission()) {
            requestPermission()
            return false
        }

        return try {
            context.startService(
                Intent(
                    context,
                    BubbleService::class.java
                )
            )
            true
        } catch (e: Exception) {
            e.printStackTrace()
            false
        }
    }

    fun hide() {
        try {
            context.stopService(
                Intent(
                    context,
                    BubbleService::class.java
                )
            )
        } catch (_: Exception) {
        }
    }

    fun restart(): Boolean {
        hide()
        return show()
    }

    fun isRunning(): Boolean {
        return BubbleService.isRunning
    }
}
