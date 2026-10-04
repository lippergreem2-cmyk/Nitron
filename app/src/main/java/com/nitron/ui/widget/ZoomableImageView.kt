package com.nitron.ui.widget

import android.content.Context
import android.graphics.Matrix
import android.util.AttributeSet
import android.view.GestureDetector
import android.view.MotionEvent
import android.view.ScaleGestureDetector
import androidx.appcompat.widget.AppCompatImageView
import kotlin.math.max
import kotlin.math.min

class ZoomableImageView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null,
    defStyle: Int = 0
) : AppCompatImageView(context, attrs, defStyle) {

    companion object {
        private const val MIN_SCALE = 1f
        private const val MAX_SCALE = 6f
        private const val DOUBLE_TAP_SCALE = 3f
    }

    private val matrixValues = FloatArray(9)
    private val imageMatrix2 = Matrix()
    private var scaleFactor = 1f
    private var lastFocusX = 0f
    private var lastFocusY = 0f

    init { scaleType = ScaleType.MATRIX }

    private val scaleGestureDetector = ScaleGestureDetector(
        context,
        object : ScaleGestureDetector.SimpleOnScaleGestureListener() {
            override fun onScale(detector: ScaleGestureDetector): Boolean {
                val newScale = (scaleFactor * detector.scaleFactor).coerceIn(MIN_SCALE, MAX_SCALE)
                val factor = newScale / scaleFactor
                scaleFactor = newScale
                imageMatrix2.postScale(factor, factor, detector.focusX, detector.focusY)
                applyMatrix()
                return true
            }
        }
    )

    private val gestureDetector = GestureDetector(
        context,
        object : GestureDetector.SimpleOnGestureListener() {
            override fun onDoubleTap(e: MotionEvent): Boolean {
                val targetScale = if (scaleFactor > MIN_SCALE) MIN_SCALE else DOUBLE_TAP_SCALE
                val factor = targetScale / scaleFactor
                scaleFactor = targetScale
                imageMatrix2.postScale(factor, factor, e.x, e.y)
                applyMatrix()
                return true
            }
        }
    )

    override fun onTouchEvent(event: MotionEvent): Boolean {
        scaleGestureDetector.onTouchEvent(event)
        gestureDetector.onTouchEvent(event)
        when (event.actionMasked) {
            MotionEvent.ACTION_DOWN -> {
                lastFocusX = event.x
                lastFocusY = event.y
            }
            MotionEvent.ACTION_MOVE -> {
                if (event.pointerCount == 1 && scaleFactor > MIN_SCALE) {
                    val dx = event.x - lastFocusX
                    val dy = event.y - lastFocusY
                    imageMatrix2.postTranslate(dx, dy)
                    applyMatrix()
                    lastFocusX = event.x
                    lastFocusY = event.y
                    parent?.requestDisallowInterceptTouchEvent(true)
                }
            }
            MotionEvent.ACTION_UP, MotionEvent.ACTION_CANCEL -> {
                parent?.requestDisallowInterceptTouchEvent(false)
            }
        }
        return true
    }

    fun resetZoom() {
        scaleFactor = MIN_SCALE
        imageMatrix2.reset()
        applyMatrix()
    }

    private fun applyMatrix() {
        imageMatrix2.getValues(matrixValues)
        val scaleX = matrixValues[Matrix.MSCALE_X]
        if (drawable != null) {
            val imgWidth = drawable.intrinsicWidth * scaleX
            val imgHeight = drawable.intrinsicHeight * matrixValues[Matrix.MSCALE_Y]
            var transX = matrixValues[Matrix.MTRANS_X]
            var transY = matrixValues[Matrix.MTRANS_Y]
            transX = if (imgWidth <= width) (width - imgWidth) / 2 else min(0f, max(transX, width - imgWidth))
            transY = if (imgHeight <= height) (height - imgHeight) / 2 else min(0f, max(transY, height - imgHeight))
            matrixValues[Matrix.MTRANS_X] = transX
            matrixValues[Matrix.MTRANS_Y] = transY
            imageMatrix2.setValues(matrixValues)
        }
        imageMatrix = imageMatrix2
    }
}
