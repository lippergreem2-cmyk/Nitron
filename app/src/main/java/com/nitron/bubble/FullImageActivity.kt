package com.nitron.bubble

import android.Manifest
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Bundle
import android.widget.ImageButton
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import java.net.HttpURLConnection
import java.net.URL
import kotlin.concurrent.thread

class FullImageActivity : AppCompatActivity() {

    private var handGestureController: HandGestureController? = null
    private val cameraPermissionRequestCode = 4821

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_full_image)

        val imageView = findViewById<NitronImageView>(R.id.fullImageView)
        val closeButton = findViewById<ImageButton>(R.id.fullImageCloseButton)

        closeButton.setOnClickListener {
            finish()
        }

        val imageUriString = intent.getStringExtra("image_uri")

        if (imageUriString != null) {

            if (
                imageUriString.startsWith("http://") ||
                imageUriString.startsWith("https://")
            ) {

                thread {
                    try {
                        val connection =
                            URL(imageUriString).openConnection() as HttpURLConnection
                        connection.connectTimeout = 10000
                        connection.readTimeout = 15000

                        val bytes = connection.inputStream.use { it.readBytes() }

                        val bitmap =
                            android.graphics.BitmapFactory.decodeByteArray(
                                bytes, 0, bytes.size
                            )

                        connection.disconnect()

                        runOnUiThread {
                            if (bitmap != null) {
                                imageView.setImageBitmap(bitmap)
                            }
                        }
                    } catch (_: Exception) {
                    }
                }

            } else {
                imageView.setImageURI(Uri.parse(imageUriString))
            }
        }

        requestCameraAndStartHandTracking(imageView)
    }

    private fun requestCameraAndStartHandTracking(imageView: NitronImageView) {

        if (
            ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.CAMERA
            ) != PackageManager.PERMISSION_GRANTED
        ) {

            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.CAMERA),
                cameraPermissionRequestCode
            )

            return
        }

        startHandTracking(imageView)
    }

    private fun startHandTracking(imageView: NitronImageView) {

        handGestureController =
            HandGestureController(this, this) { spread ->

                runOnUiThread {
                    try {
                        val scale = (1f + spread * 12f).coerceIn(1f, 5f)
                        imageView.setExternalZoom(scale)
                    } catch (e: Throwable) {
                    }
                }
            }

        handGestureController?.start()
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)

        if (
            requestCode == cameraPermissionRequestCode &&
            grantResults.isNotEmpty() &&
            grantResults[0] == PackageManager.PERMISSION_GRANTED
        ) {
            val imageView = findViewById<NitronImageView>(R.id.fullImageView)
            startHandTracking(imageView)
        }
    }

    override fun onDestroy() {
        handGestureController?.stop()
        super.onDestroy()
    }
}
