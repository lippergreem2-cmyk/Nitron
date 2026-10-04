package com.nitron.bubble

import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.widget.Toast
import java.io.ByteArrayOutputStream
import android.util.Base64

class ImagePickerActivity : Activity() {

    companion object {
        private const val PICK_IMAGE = 5001
        const val EXTRA_IMAGE_URI = "nitron_image_uri"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val intent = Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
            addCategory(Intent.CATEGORY_OPENABLE)
            type = "image/*"
        }

        startActivityForResult(intent, PICK_IMAGE)
    }

    override fun onActivityResult(
        requestCode: Int,
        resultCode: Int,
        data: Intent?
    ) {
        super.onActivityResult(requestCode, resultCode, data)

        if (requestCode != PICK_IMAGE ||
            resultCode != RESULT_OK ||
            data?.data == null
        ) {
            finish()
            return
        }

        val uri = data.data!!

        // Return the selected picture to MainActivity immediately.
        setResult(
            RESULT_OK,
            Intent().apply {
                putExtra(EXTRA_IMAGE_URI, uri.toString())
            }
        )

        // Keep access to the selected image.
        try {
            contentResolver.takePersistableUriPermission(
                uri,
                Intent.FLAG_GRANT_READ_URI_PERMISSION
            )
        } catch (_: Exception) {
        }

        // Also send the picture to Nitron's backend.
        Thread {

            try {

                val bytes =
                    contentResolver.openInputStream(uri).use { input ->

                        if (input == null) {
                            throw Exception("Could not open image.")
                        }

                        val output = ByteArrayOutputStream()
                        val buffer = ByteArray(8192)

                        while (true) {

                            val count = input.read(buffer)

                            if (count == -1) break

                            output.write(buffer, 0, count)
                        }

                        output.toByteArray()
                    }

                val base64 =
                    Base64.encodeToString(
                        bytes,
                        Base64.NO_WRAP
                    )

                val filename =
                    uri.lastPathSegment
                        ?.substringAfterLast("/")
                        ?.substringAfterLast(":")
                        ?.takeIf { it.isNotBlank() }
                        ?: "picture.jpg"

                TermuxBridge.sendImage(
                    base64,
                    filename
                ) { reply ->

                    runOnUiThread {

                        Toast.makeText(
                            this,
                            reply,
                            Toast.LENGTH_LONG
                        ).show()
                    }
                }

            } catch (e: Exception) {

                runOnUiThread {

                    Toast.makeText(
                        this,
                        "Could not send picture: ${e.message}",
                        Toast.LENGTH_LONG
                    ).show()
                }
            }

        }.start()

        finish()
    }
}
