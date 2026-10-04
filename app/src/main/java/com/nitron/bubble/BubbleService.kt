package com.nitron.bubble

import android.app.Service
import androidx.lifecycle.LifecycleService
import android.content.Intent
import android.graphics.PixelFormat
import android.os.Build
import android.os.IBinder
import android.provider.Settings
import android.view.GestureDetector
import android.view.Gravity
import android.view.LayoutInflater
import android.view.MotionEvent
import android.view.ScaleGestureDetector
import android.view.View
import android.view.WindowManager
import android.view.animation.AlphaAnimation
import android.view.animation.Animation
import android.widget.TextView

class BubbleService : LifecycleService() {

    companion object {
        @JvmStatic
        var isRunning: Boolean = false
            private set

        private var instance: BubbleService? = null

        @JvmStatic
        fun restoreBubbleAtBottom() {
            instance?.restoreBubbleAtBottomInternal()
        }

        @JvmStatic
        fun setSpeaking(speaking: Boolean) {
            if (speaking) {
                instance?.startGlowPulse()
            } else {
                instance?.stopGlowPulse()
            }
        }
    }

    private lateinit var windowManager: WindowManager
    private lateinit var bubbleView: View
    private lateinit var params: WindowManager.LayoutParams
    private lateinit var bubbleMenu: BubbleMenu
    private lateinit var glowView: View
    private var handGestureController: HandGestureController? = null

    private var startX = 0
    private var startY = 0
    private var touchX = 0f
    private var touchY = 0f

    private var moved = false
    private var bubbleScale = 1.0f
    private lateinit var scaleGestureDetector: ScaleGestureDetector

    override fun onCreate() {
        super.onCreate()

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (!Settings.canDrawOverlays(this)) {
                stopSelf()
                return
            }
        }

        isRunning = true
        instance = this

        windowManager =
            getSystemService(WINDOW_SERVICE) as WindowManager

        bubbleMenu = BubbleMenu(this)

        bubbleView = LayoutInflater.from(this)
            .inflate(R.layout.bubble_layout, null)

        glowView = bubbleView.findViewById(R.id.bubbleGlow)

        params = WindowManager.LayoutParams(
            WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or
                    WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS,
            PixelFormat.TRANSLUCENT
        )

        params.gravity =
            Gravity.TOP or Gravity.START

        params.x = 20
        params.y = 300

        try {
            windowManager.addView(
                bubbleView,
                params
            )
        } catch (_: Exception) {
            isRunning = false
            stopSelf()
            return
        }

        val nitronBubble =
            bubbleView.findViewById<TextView>(R.id.nitronBubble)

        val gestureDetector = GestureDetector(
            this,
            object : GestureDetector.SimpleOnGestureListener() {

                override fun onDown(
                    e: MotionEvent
                ): Boolean {
                    return true
                }

                override fun onSingleTapConfirmed(
                    e: MotionEvent
                ): Boolean {

                    if (!moved) {
                        openChat()
                    }

                    return true
                }

                override fun onLongPress(
                    e: MotionEvent
                ) {

                    bubbleMenu.show(bubbleView)
                }
            }
        )

        scaleGestureDetector = ScaleGestureDetector(
            this,
            object : ScaleGestureDetector.SimpleOnScaleGestureListener() {

                override fun onScale(
                    detector: ScaleGestureDetector
                ): Boolean {

                    bubbleScale *= detector.scaleFactor
                    bubbleScale = bubbleScale.coerceIn(0.5f, 2.5f)

                    bubbleView.scaleX = bubbleScale
                    bubbleView.scaleY = bubbleScale

                    return true
                }
            }
        )

        // Drag + tap only on the center circle now
        nitronBubble.setOnTouchListener { _, event ->

            scaleGestureDetector.onTouchEvent(event)

            if (event.pointerCount > 1 || scaleGestureDetector.isInProgress) {
                return@setOnTouchListener true
            }

            gestureDetector.onTouchEvent(event)

            when (event.actionMasked) {

                MotionEvent.ACTION_DOWN -> {

                    startX = params.x
                    startY = params.y

                    touchX = event.rawX
                    touchY = event.rawY

                    moved = false

                    true
                }

                MotionEvent.ACTION_MOVE -> {

                    val dx =
                        event.rawX - touchX

                    val dy =
                        event.rawY - touchY

                    if (
                        kotlin.math.abs(dx) > 8 ||
                        kotlin.math.abs(dy) > 8
                    ) {
                        moved = true
                    }

                    params.x =
                        startX + dx.toInt()

                    params.y =
                        startY + dy.toInt()

                    keepInsideScreen()

                    try {
                        windowManager.updateViewLayout(
                            bubbleView,
                            params
                        )
                    } catch (_: Exception) {
                    }

                    true
                }

                MotionEvent.ACTION_UP,
                MotionEvent.ACTION_CANCEL -> {

                    if (moved) {
                        snapToEdge()
                    }

                    true
                }

                else -> true
            }
        }

        // Satellite icons — plain clicks, no drag
        bubbleView.findViewById<TextView>(R.id.bubbleMenuIcon)
            ?.setOnClickListener {
                bubbleMenu.show(bubbleView)
            }

        bubbleView.findViewById<TextView>(R.id.bubbleCloseIcon)
            ?.setOnClickListener {
                stopSelf()
            }

        bubbleView.findViewById<TextView>(R.id.bubbleMicIcon)
            ?.setOnClickListener {
                openChat()
            }
    }

    fun startGlowPulse() {

        if (!::glowView.isInitialized) return

        val anim = AlphaAnimation(0.4f, 1.0f)
        anim.duration = 600
        anim.repeatMode = Animation.REVERSE
        anim.repeatCount = Animation.INFINITE

        glowView.startAnimation(anim)
    }

    fun stopGlowPulse() {

        if (!::glowView.isInitialized) return

        glowView.clearAnimation()
        glowView.alpha = 1.0f
    }

    private fun restoreBubbleAtBottomInternal() {

        if (!::bubbleView.isInitialized) {
            return
        }

        try {
            val metrics = resources.displayMetrics

            val screenWidth = metrics.widthPixels
            val screenHeight = metrics.heightPixels

            params.x =
                ((screenWidth - bubbleView.width) / 2)
                    .coerceAtLeast(0)

            params.y =
                (screenHeight - bubbleView.height - 120)
                    .coerceAtLeast(0)

            bubbleView.visibility = View.VISIBLE
            bubbleView.alpha = 1.0f
            bubbleView.scaleX = 1.0f
            bubbleView.scaleY = 1.0f

            try {
                windowManager.updateViewLayout(
                    bubbleView,
                    params
                )
            } catch (_: Exception) {
                // The overlay may have been removed. Re-add it.
                try {
                    windowManager.addView(
                        bubbleView,
                        params
                    )
                } catch (_: Exception) {
                }
            }

            bubbleView.visibility = View.VISIBLE
            bubbleView.alpha = 1.0f
            bubbleView.scaleX = 1.0f
            bubbleView.scaleY = 1.0f
            bubbleView.bringToFront()

        } catch (_: Exception) {
        }
    }

    private fun openChat() {

        try {

            val state =
                getSharedPreferences(
                    "nitron_voice_state",
                    MODE_PRIVATE
                )

            val openNormalChat =
                state.getBoolean(
                    "open_chat_on_bubble_tap",
                    false
                )

            if (openNormalChat) {

                state.edit()
                    .putBoolean(
                        "open_chat_on_bubble_tap",
                        false
                    )
                    .apply()

                val intent =
                    Intent(
                        this,
                        ChatActivity::class.java
                    )

                intent.addFlags(
                    Intent.FLAG_ACTIVITY_NEW_TASK or
                            Intent.FLAG_ACTIVITY_SINGLE_TOP
                )

                startActivity(intent)

            } else {

                val intent =
                    Intent(
                        this,
                        VoiceModeActivity::class.java
                    )

                intent.addFlags(
                    Intent.FLAG_ACTIVITY_NEW_TASK or
                            Intent.FLAG_ACTIVITY_SINGLE_TOP
                )

                startActivity(intent)
            }

        } catch (_: Exception) {
        }
    }

    private fun keepInsideScreen() {

        val metrics =
            resources.displayMetrics

        val screenWidth =
            metrics.widthPixels

        val screenHeight =
            metrics.heightPixels

        val bubbleWidth =
            bubbleView.width

        val bubbleHeight =
            bubbleView.height

        val maxX =
            (screenWidth - bubbleWidth)
                .coerceAtLeast(0)

        val maxY =
            (screenHeight - bubbleHeight)
                .coerceAtLeast(0)

        params.x =
            params.x.coerceIn(0, maxX)

        params.y =
            params.y.coerceIn(0, maxY)
    }

    private fun snapToEdge() {

        val screenWidth =
            resources.displayMetrics.widthPixels

        val bubbleWidth =
            bubbleView.width

        params.x =
            if (
                params.x +
                bubbleWidth / 2 <
                screenWidth / 2
            ) {
                0
            } else {
                screenWidth - bubbleWidth
            }

        try {
            windowManager.updateViewLayout(
                bubbleView,
                params
            )
        } catch (_: Exception) {
        }
    }

    override fun onDestroy() {

        handGestureController?.stop()

        instance = null
        isRunning = false

        if (::bubbleView.isInitialized) {

            try {
                windowManager.removeView(
                    bubbleView
                )
            } catch (_: Exception) {
            }
        }

        super.onDestroy()
    }

}
