package com.nitron.bubble

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.ImageFormat
import android.graphics.Rect
import android.graphics.YuvImage
import android.util.Log
import android.widget.Toast
import android.util.Size
import androidx.camera.core.CameraSelector
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.ImageProxy
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.core.content.ContextCompat
import androidx.lifecycle.LifecycleOwner
import com.google.mediapipe.framework.image.BitmapImageBuilder
import com.google.mediapipe.tasks.core.BaseOptions
import java.io.ByteArrayOutputStream
import com.google.mediapipe.tasks.vision.core.ImageProcessingOptions
import com.google.mediapipe.tasks.vision.core.RunningMode
import com.google.mediapipe.tasks.vision.handlandmarker.HandLandmarker
import com.google.mediapipe.tasks.vision.handlandmarker.HandLandmarkerResult

class HandGestureController(
    private val context: Context,
    private val lifecycleOwner: LifecycleOwner,
    private val onSpreadChanged: (Float) -> Unit = {}
) {

    private var handLandmarker: HandLandmarker? = null
    private var cameraProvider: ProcessCameraProvider? = null

    fun start() {

        try {
            val baseOptions = BaseOptions.builder()
                .setModelAssetPath("hand_landmarker.task")
                .build()

            val options = HandLandmarker.HandLandmarkerOptions.builder()
                .setBaseOptions(baseOptions)
                .setRunningMode(RunningMode.LIVE_STREAM)
                .setNumHands(1)
                .setResultListener { result, _ -> handleResult(result) }
                .setErrorListener { e ->
                    Log.e("NITRON_HAND", "HandLandmarker error: ${e.message}")
                }
                .build()

            handLandmarker = HandLandmarker.createFromOptions(context, options)

            Toast.makeText(context, "NITRON DEBUG: hand model loaded", Toast.LENGTH_SHORT).show()

        } catch (e: Throwable) {
            Toast.makeText(context, "NITRON DEBUG: model load failed: ${e.message}", Toast.LENGTH_LONG).show()
            Log.e("NITRON_HAND", "Failed to create HandLandmarker: ${e.message}")
            return
        }

        val cameraProviderFuture = ProcessCameraProvider.getInstance(context)

        cameraProviderFuture.addListener({

            try {
                cameraProvider = cameraProviderFuture.get()

                val analysis = ImageAnalysis.Builder()
                    .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST)
                    .setTargetResolution(Size(160, 120))
                    .build()

                analysis.setAnalyzer(ContextCompat.getMainExecutor(context)) { imageProxy ->
                    processFrame(imageProxy)
                }

                cameraProvider?.unbindAll()
                cameraProvider?.bindToLifecycle(
                    lifecycleOwner,
                    CameraSelector.DEFAULT_FRONT_CAMERA,
                    analysis
                )

                Toast.makeText(context, "NITRON DEBUG: camera bound", Toast.LENGTH_SHORT).show()
                Log.d("NITRON_HAND", "Camera bound successfully")

            } catch (e: Throwable) {
                Toast.makeText(context, "NITRON DEBUG: camera bind failed: ${e.message}", Toast.LENGTH_LONG).show()
                Log.e("NITRON_HAND", "Camera bind failed: ${e.message}")
            }

        }, ContextCompat.getMainExecutor(context))
    }

    private fun imageProxyToBitmap(imageProxy: ImageProxy): Bitmap {

        val yBuffer = imageProxy.planes[0].buffer
        val uBuffer = imageProxy.planes[1].buffer
        val vBuffer = imageProxy.planes[2].buffer

        val ySize = yBuffer.remaining()
        val uSize = uBuffer.remaining()
        val vSize = vBuffer.remaining()

        val nv21 = ByteArray(ySize + uSize + vSize)

        yBuffer.get(nv21, 0, ySize)
        vBuffer.get(nv21, ySize, vSize)
        uBuffer.get(nv21, ySize + vSize, uSize)

        val yuvImage = YuvImage(
            nv21,
            ImageFormat.NV21,
            imageProxy.width,
            imageProxy.height,
            null
        )

        val out = ByteArrayOutputStream()

        yuvImage.compressToJpeg(
            Rect(0, 0, imageProxy.width, imageProxy.height),
            50,
            out
        )

        val jpegBytes = out.toByteArray()

        return BitmapFactory.decodeByteArray(jpegBytes, 0, jpegBytes.size)
    }

    private var frameCounter = 0
    private var isDetecting = false

    private fun processFrame(imageProxy: ImageProxy) {

        frameCounter++

        if (frameCounter % 10 != 0 || isDetecting) {
            imageProxy.close()
            return
        }

        try {
            val bitmap = imageProxyToBitmap(imageProxy)

            val mpImage = BitmapImageBuilder(bitmap).build()

            val rotation = imageProxy.imageInfo.rotationDegrees

            val processingOptions = ImageProcessingOptions.builder()
                .setRotationDegrees(rotation)
                .build()

            isDetecting = true
            handLandmarker?.detectAsync(
                mpImage,
                processingOptions,
                imageProxy.imageInfo.timestamp
            )

        } catch (e: Throwable) {
            Toast.makeText(context, "NITRON DEBUG: frame error: ${e.message}", Toast.LENGTH_SHORT).show()
            Log.e("NITRON_HAND", "Frame processing failed: ${e.message}")
        } finally {
            imageProxy.close()
        }
    }

    private var emptyResultCount = 0

    private fun handleResult(result: HandLandmarkerResult) {

        isDetecting = false

        if (result.landmarks().isEmpty()) {
            emptyResultCount++
            if (emptyResultCount % 30 == 1) {
                Toast.makeText(context, "NITRON DEBUG: no hand seen ($emptyResultCount)", Toast.LENGTH_SHORT).show()
            }
            return
        }

        emptyResultCount = 0

        try {
            val landmarks = result.landmarks()[0]

            val thumbTip = landmarks[4]
            val indexTip = landmarks[8]

            val dx = thumbTip.x() - indexTip.x()
            val dy = thumbTip.y() - indexTip.y()

            val spread = kotlin.math.sqrt(dx * dx + dy * dy)

            onSpreadChanged(spread)

        } catch (e: Throwable) {
            Toast.makeText(context, "NITRON DEBUG: handleResult error: ${e.message}", Toast.LENGTH_LONG).show()
        }
    }

    fun stop() {

        try {
            cameraProvider?.unbindAll()
        } catch (_: Exception) {
        }

        try {
            handLandmarker?.close()
        } catch (_: Exception) {
        }
    }
}
