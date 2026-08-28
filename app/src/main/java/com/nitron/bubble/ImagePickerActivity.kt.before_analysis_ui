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

        if (requestCode != PICK_IMAGE) {
            finish()
            return
        }

        if (resultCode != RESULT_OK || data?.data == null) {
            finish()
            return
        }

        val uri: Uri = data.data!!

        try {
            val resolver = contentResolver

            val bytes = resolver.openInputStream(uri).use { input ->
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

            val base64 = Base64.encodeToString(bytes, Base64.NO_WRAP)

            val filename = uri.lastPathSegment
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

                    finish()
                }
            }

        } catch (e: Exception) {

            Toast.makeText(
                this,
                "Could not read picture: ${e.message}",
                Toast.LENGTH_LONG
            ).show()

            finish()
        }
    }
}
