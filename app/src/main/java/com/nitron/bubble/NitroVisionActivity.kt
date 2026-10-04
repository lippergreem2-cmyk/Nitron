package com.nitron.bubble

import android.Manifest
import android.app.Activity
import android.content.pm.PackageManager
import android.graphics.Color
import android.os.Bundle
import android.view.Gravity
import android.widget.*
import androidx.activity.ComponentActivity
import androidx.camera.core.CameraSelector
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.Preview
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.view.PreviewView
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import java.util.concurrent.Executors

class NitroVisionActivity : ComponentActivity() {

    private lateinit var previewView: PreviewView
    private lateinit var statusText: TextView
    private lateinit var infoText: TextView

    private val cameraExecutor = Executors.newSingleThreadExecutor()

    private lateinit var poseController: NitroPoseController

    private val blue = Color.rgb(40, 150, 255)
    private val cyan = Color.CYAN
    private val dark = Color.rgb(3, 12, 28)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        buildScreen()

        poseController = NitroPoseController(
            this
        ) { message ->
            runOnUiThread {
                statusText.text = "SYSTEM: $message"
            }
        }

        poseController.start()

        if (ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.CAMERA
            ) == PackageManager.PERMISSION_GRANTED
        ) {
            startCamera()
        } else {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.CAMERA),
                1001
            )
        }
    }

    private fun buildScreen() {

        val root = FrameLayout(this)
        root.setBackgroundColor(dark)

        previewView = PreviewView(this)

        root.addView(
            previewView,
            FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.MATCH_PARENT,
                FrameLayout.LayoutParams.MATCH_PARENT
            )
        )

        val overlay = LinearLayout(this)
        overlay.orientation = LinearLayout.VERTICAL
        overlay.setPadding(24, 40, 24, 24)

        val title = TextView(this)
        title.text = "NITROVISION"
        title.textSize = 28f
        title.setTextColor(blue)
        title.gravity = Gravity.CENTER
        title.setTypeface(null, android.graphics.Typeface.BOLD)

        val subtitle = TextView(this)
        subtitle.text = "MOVEMENT ANALYSIS"
        subtitle.textSize = 14f
        subtitle.setTextColor(cyan)
        subtitle.gravity = Gravity.CENTER

        statusText = TextView(this)
        statusText.text = "SYSTEM: CAMERA READY"
        statusText.textSize = 18f
        statusText.setTextColor(Color.WHITE)
        statusText.gravity = Gravity.CENTER
        statusText.setPadding(0, 30, 0, 20)

        infoText = TextView(this)
        infoText.text =
            "Position yourself inside the camera view.\n\n" +
            "NitroVision will begin with basic movement detection."

        infoText.textSize = 16f
        infoText.setTextColor(Color.WHITE)
        infoText.gravity = Gravity.CENTER

        overlay.addView(title)
        overlay.addView(subtitle)
        overlay.addView(statusText)
        overlay.addView(infoText)

        val overlayParams = FrameLayout.LayoutParams(
            FrameLayout.LayoutParams.MATCH_PARENT,
            FrameLayout.LayoutParams.WRAP_CONTENT
        )

        overlayParams.gravity = Gravity.TOP

        root.addView(overlay, overlayParams)

        val end = Button(this)
        end.text = "END SESSION"
        end.setTextColor(Color.WHITE)
        end.setBackgroundColor(Color.rgb(40, 40, 40))

        end.setOnClickListener {
            finish()
        }

        val endParams = FrameLayout.LayoutParams(
            FrameLayout.LayoutParams.MATCH_PARENT,
            FrameLayout.LayoutParams.WRAP_CONTENT
        )

        endParams.gravity = Gravity.BOTTOM
        endParams.setMargins(30, 20, 30, 40)

        root.addView(end, endParams)

        setContentView(root)
    }

    private fun startCamera() {

        val cameraProviderFuture =
            ProcessCameraProvider.getInstance(this)

        cameraProviderFuture.addListener({

            val cameraProvider = cameraProviderFuture.get()

            val preview = Preview.Builder()
                .build()

            preview.setSurfaceProvider(
                previewView.surfaceProvider
            )

            val analysis = ImageAnalysis.Builder()
                .setBackpressureStrategy(
                    ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST
                )
                .build()

            analysis.setAnalyzer(cameraExecutor) { imageProxy ->

                poseController.processFrame(imageProxy)

            }

            try {

                cameraProvider.unbindAll()

                cameraProvider.bindToLifecycle(
                    this@NitroVisionActivity,
                    CameraSelector.DEFAULT_FRONT_CAMERA,
                    preview,
                    analysis
                )

            } catch (error: Exception) {

                runOnUiThread {
                    statusText.text =
                        "SYSTEM: CAMERA ERROR"
                    infoText.text =
                        error.message ?: "Camera could not start."
                }
            }

        }, ContextCompat.getMainExecutor(this))
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(
            requestCode,
            permissions,
            grantResults
        )

        if (requestCode == 1001 &&
            grantResults.isNotEmpty() &&
            grantResults[0] == PackageManager.PERMISSION_GRANTED
        ) {
            startCamera()
        } else {
            statusText.text =
                "SYSTEM: CAMERA PERMISSION REQUIRED"

            infoText.text =
                "Camera access was not granted."
        }
    }

    override fun onDestroy() {
        poseController.stop()
        cameraExecutor.shutdown()
        super.onDestroy()
    }
}
