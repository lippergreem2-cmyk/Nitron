package com.nitron.overlay

import android.content.Context
import android.view.MotionEvent
import android.view.ScaleGestureDetector
import android.view.View
import android.view.WindowManager
import kotlin.math.roundToInt

class BubbleGestureController(
    context: Context,
    private val windowManager: WindowManager,
    private val bubbleView: View,
    private val layoutParams: WindowManager.LayoutParams,
    private val minSizePx: Int = (48 * context.resources.displayMetrics.density).roundToInt(),
    private val maxSizePx: Int = (220 * context.resources.displayMetrics.density).roundToInt()
) {
    private var initialTouchX = 0f
    private var initialTouchY = 0f
    private var initialParamX = 0
    private var initialParamY = 0
    private var isScaling = false

    private val scaleGestureDetector = ScaleGestureDetector(
        context,
        object : ScaleGestureDetector.SimpleOnScaleGestureListener() {
            override fun onScaleBegin(detector: ScaleGestureDetector): Boolean {
                isScaling = true
                return true
            }
            override fun onScale(detector: ScaleGestureDetector): Boolean {
                val newSize = (layoutParams.width * detector.scaleFactor).roundToInt().coerceIn(minSizePx, maxSizePx)
                layoutParams.width = newSize
                layoutParams.height = newSize
                safeUpdateLayout()
                return true
            }
            override fun onScaleEnd(detector: ScaleGestureDetector) { isScaling = false }
        }
    )

    fun onTouch(event: MotionEvent): Boolean {
        scaleGestureDetector.onTouchEvent(event)
        when (event.actionMasked) {
            MotionEvent.ACTION_DOWN -> {
                initialTouchX = event.rawX
                initialTouchY = event.rawY
                initialParamX = layoutParams.x
                initialParamY = layoutParams.y
            }
            MotionEvent.ACTION_MOVE -> {
                if (!isScaling && event.pointerCount == 1) {
                    layoutParams.x = initialParamX + (event.rawX - initialTouchX).roundToInt()
                    layoutParams.y = initialParamY + (event.rawY - initialTouchY).roundToInt()
                    safeUpdateLayout()
                }
            }
        }
        return true
    }

    fun resetSize(defaultSizePx: Int) {
        layoutParams.width = defaultSizePx
        layoutParams.height = defaultSizePx
        safeUpdateLayout()
    }

    private fun safeUpdateLayout() {
        try { windowManager.updateViewLayout(bubbleView, layoutParams) } catch (_: IllegalArgumentException) {}
    }
}
