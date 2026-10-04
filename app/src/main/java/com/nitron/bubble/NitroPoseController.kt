package com.nitron.bubble

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.ImageFormat
import android.graphics.Rect
import android.graphics.YuvImage
import android.util.Log
import androidx.camera.core.ImageProxy
import com.google.mediapipe.framework.image.BitmapImageBuilder
import com.google.mediapipe.tasks.core.BaseOptions
import com.google.mediapipe.tasks.vision.core.ImageProcessingOptions
import com.google.mediapipe.tasks.vision.core.RunningMode
import com.google.mediapipe.tasks.vision.poselandmarker.PoseLandmarker
import com.google.mediapipe.tasks.vision.poselandmarker.PoseLandmarkerResult
import java.io.ByteArrayOutputStream
import kotlin.math.sqrt

class NitroPoseController(
    private val context: Context,
    private val onPoseDetected: (String) -> Unit = {}
) {

    private var poseLandmarker: PoseLandmarker? = null
    private var isDetecting = false
    private var frameCounter = 0

    fun start() {
        try {
            val baseOptions = BaseOptions.builder()
                .setModelAssetPath("pose_landmarker_lite.task")
                .build()

            val options = PoseLandmarker.PoseLandmarkerOptions.builder()
                .setBaseOptions(baseOptions)
                .setRunningMode(RunningMode.LIVE_STREAM)
                .setNumPoses(1)
                .setMinPoseDetectionConfidence(0.5f)
                .setMinPosePresenceConfidence(0.5f)
                .setMinTrackingConfidence(0.5f)
                .setResultListener { result, _ ->
                    handleResult(result)
                }
                .setErrorListener { error ->
                    Log.e(
                        "NITRON_POSE",
                        "PoseLandmarker error: ${error.message}"
                    )
                }
                .build()

            poseLandmarker =
                PoseLandmarker.createFromOptions(context, options)

            Log.d("NITRON_POSE", "Pose model loaded")

        } catch (error: Throwable) {
            Log.e(
                "NITRON_POSE",
                "Failed to create PoseLandmarker",
                error
            )
        }
    }

    fun processFrame(imageProxy: ImageProxy) {

        frameCounter++

        if (frameCounter % 5 != 0 || isDetecting) {
            imageProxy.close()
            return
        }

        try {
            val bitmap = imageProxyToBitmap(imageProxy)

            val mpImage =
                BitmapImageBuilder(bitmap).build()

            val processingOptions =
                ImageProcessingOptions.builder()
                    .setRotationDegrees(
                        imageProxy.imageInfo.rotationDegrees
                    )
                    .build()

            isDetecting = true

            poseLandmarker?.detectAsync(
                mpImage,
                processingOptions,
                imageProxy.imageInfo.timestamp
            )

        } catch (error: Throwable) {
            isDetecting = false

            Log.e(
                "NITRON_POSE",
                "Frame processing failed",
                error
            )
        } finally {
            imageProxy.close()
        }
    }

    private fun imageProxyToBitmap(
        imageProxy: ImageProxy
    ): Bitmap {

        val yBuffer = imageProxy.planes[0].buffer
        val uBuffer = imageProxy.planes[1].buffer
        val vBuffer = imageProxy.planes[2].buffer

        val ySize = yBuffer.remaining()
        val uSize = uBuffer.remaining()
        val vSize = vBuffer.remaining()

        val nv21 = ByteArray(
            ySize + uSize + vSize
        )

        yBuffer.get(nv21, 0, ySize)
        vBuffer.get(nv21, ySize, vSize)
        uBuffer.get(
            nv21,
            ySize + vSize,
            uSize
        )

        val yuvImage = YuvImage(
            nv21,
            ImageFormat.NV21,
            imageProxy.width,
            imageProxy.height,
            null
        )

        val output = ByteArrayOutputStream()

        yuvImage.compressToJpeg(
            Rect(
                0,
                0,
                imageProxy.width,
                imageProxy.height
            ),
            50,
            output
        )

        val bytes = output.toByteArray()

        return BitmapFactory.decodeByteArray(
            bytes,
            0,
            bytes.size
        )
    }

    private fun handleResult(
        result: PoseLandmarkerResult
    ) {

        isDetecting = false

        if (result.landmarks().isEmpty()) {
            onPoseDetected("NO PERSON DETECTED")
            return
        }

        try {
            val landmarks = result.landmarks()[0]

            val leftShoulder = landmarks[11]
            val rightShoulder = landmarks[12]
            val leftHip = landmarks[23]
            val rightHip = landmarks[24]

            val shoulderDistance = distance(
                leftShoulder.x(),
                leftShoulder.y(),
                rightShoulder.x(),
                rightShoulder.y()
            )

            val hipCenterY =
                (leftHip.y() + rightHip.y()) / 2f

            val shoulderCenterY =
                (leftShoulder.y() + rightShoulder.y()) / 2f

            val torsoLength =
                kotlin.math.abs(
                    hipCenterY - shoulderCenterY
                )

            val status = when {
                shoulderDistance < 0.08f ->
                    "MOVE CLOSER"

                torsoLength < 0.10f ->
                    "ADJUST POSITION"

                else ->
                    "POSE DETECTED"
            }

            onPoseDetected(
                "$status  |  BODY TRACKING ACTIVE"
            )

        } catch (error: Throwable) {
            Log.e(
                "NITRON_POSE",
                "Result processing failed",
                error
            )
        }
    }

    private fun distance(
        x1: Float,
        y1: Float,
        x2: Float,
        y2: Float
    ): Float {

        val dx = x1 - x2
        val dy = y1 - y2

        return sqrt(
            dx * dx + dy * dy
        )
    }

    fun stop() {
        try {
            poseLandmarker?.close()
        } catch (_: Exception) {
        }

        poseLandmarker = null
        isDetecting = false
    }
}
