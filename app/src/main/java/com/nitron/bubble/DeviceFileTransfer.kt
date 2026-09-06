package com.nitron.bubble

import android.content.Context
import android.content.Intent
import android.net.Uri

object DeviceFileTransfer {

    /**
     * Opens Android's secure sharing interface for a file.
     *
     * Compatible nearby-device and Bluetooth sharing options may
     * appear depending on the receiving device and Android version.
     */
    fun shareFile(
        context: Context,
        fileUri: Uri,
        mimeType: String = "*/*"
    ): Boolean {

        return try {

            val shareIntent =
                Intent(Intent.ACTION_SEND).apply {

                    type = mimeType

                    putExtra(
                        Intent.EXTRA_STREAM,
                        fileUri
                    )

                    addFlags(
                        Intent.FLAG_GRANT_READ_URI_PERMISSION
                    )
                }

            val chooser =
                Intent.createChooser(
                    shareIntent,
                    "Send file with Nitron"
                ).apply {
                    addFlags(
                        Intent.FLAG_ACTIVITY_NEW_TASK
                    )
                }

            context.startActivity(chooser)

            true

        } catch (_: Exception) {
            false
        }
    }

    /**
     * Opens Android's sharing interface for text.
     */
    fun shareText(
        context: Context,
        text: String
    ): Boolean {

        return try {

            val shareIntent =
                Intent(Intent.ACTION_SEND).apply {

                    type = "text/plain"

                    putExtra(
                        Intent.EXTRA_TEXT,
                        text
                    )
                }

            context.startActivity(
                Intent.createChooser(
                    shareIntent,
                    "Share with Nitron"
                ).apply {
                    addFlags(
                        Intent.FLAG_ACTIVITY_NEW_TASK
                    )
                }
            )

            true

        } catch (_: Exception) {
            false
        }
    }
}
