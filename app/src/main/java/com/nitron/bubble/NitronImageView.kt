package com.nitron.bubble

import android.content.Context
import android.graphics.Matrix
import android.graphics.drawable.Drawable
import android.net.Uri
import android.util.AttributeSet
import android.view.MotionEvent
import android.view.ScaleGestureDetector
import android.widget.ImageView

class NitronImageView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null
) : ImageView(context, attrs) {

    private val zoomMatrix = Matrix()

    private var zoom = 1f
    private var moveX = 0f
    private var moveY = 0f

    private var lastX = 0f
    private var lastY = 0f

    private val scaleDetector =
        ScaleGestureDetector(
            context,
            object : ScaleGestureDetector.SimpleOnScaleGestureListener() {

                override fun onScale(
                    detector: ScaleGestureDetector
                ): Boolean {

                    zoom *= detector.scaleFactor
                    zoom = zoom.coerceIn(1f, 5f)

                    updateMatrix()
                    return true
                }
            }
        )

    init {
        scaleType = ScaleType.FIT_CENTER
        isClickable = true
        isFocusable = true
    }

    private fun updateMatrix() {

        zoomMatrix.reset()

        zoomMatrix.postScale(
            zoom,
            zoom,
            width / 2f,
            height / 2f
        )

        zoomMatrix.postTranslate(
            moveX,
            moveY
        )

        imageMatrix = zoomMatrix
    }

    override fun onTouchEvent(event: MotionEvent): Boolean {

        scaleDetector.onTouchEvent(event)

        when (event.actionMasked) {

            MotionEvent.ACTION_DOWN -> {

                lastX = event.x
                lastY = event.y

                parent?.requestDisallowInterceptTouchEvent(true)

                return true
            }

            MotionEvent.ACTION_MOVE -> {

                if (
                    event.pointerCount == 1 &&
                    zoom > 1f
                ) {

                    moveX += event.x - lastX
                    moveY += event.y - lastY

                    lastX = event.x
                    lastY = event.y

                    updateMatrix()
                }

                return true
            }

            MotionEvent.ACTION_UP -> {

                parent?.requestDisallowInterceptTouchEvent(false)

                performClick()

                return true
            }

            MotionEvent.ACTION_CANCEL -> {

                parent?.requestDisallowInterceptTouchEvent(false)

                return true
            }
        }

        return true
    }

    override fun performClick(): Boolean {
        super.performClick()
        return true
    }

    override fun setImageDrawable(drawable: Drawable?) {

        super.setImageDrawable(drawable)

        zoom = 1f
        moveX = 0f
        moveY = 0f

        post {
            updateMatrix()
        }
    }

    override fun setImageURI(uri: Uri?) {

        zoom = 1f
        moveX = 0f
        moveY = 0f

        if (uri == null) {
            super.setImageDrawable(null)
            post { updateMatrix() }
            return
        }

        try {
            val source =
                android.graphics.ImageDecoder.createSource(
                    context.contentResolver,
                    uri
                )
            val bitmap =
                android.graphics.ImageDecoder.decodeBitmap(source)
            super.setImageBitmap(bitmap)
        } catch (e: Exception) {
            super.setImageDrawable(null)
        }

        post {
            updateMatrix()
        }
    }

    fun setExternalZoom(scale: Float) {
        zoom = scale.coerceIn(1f, 5f)
        updateMatrix()
    }
}
