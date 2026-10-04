package com.nitron.bubble

import android.Manifest
import android.animation.ObjectAnimator
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import android.view.MotionEvent
import android.view.ScaleGestureDetector
import android.view.View
import android.view.animation.LinearInterpolator
import android.view.inputmethod.EditorInfo
import android.view.inputmethod.InputMethodManager
import android.widget.EditText
import android.widget.FrameLayout
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.nitron.bubble.chat.ChatHistoryStore
import com.nitron.bubble.chat.ChatManager
import com.nitron.bubble.chat.Message
import java.util.Locale

class VoiceModeActivity : AppCompatActivity() {

    private var handGestureController: HandGestureController? = null

    private fun sendTypedMessage() {

        val typedText = voiceInputField.text.toString().trim()

        if (typedText.isNotBlank()) {

            ChatHistoryStore.add(
                Message(
                    typedText,
                    true
                )
            )

            chatManager.sendMessage(
                typedText
            )

            voiceInputField.text.clear()

            val imm = getSystemService(INPUT_METHOD_SERVICE) as InputMethodManager
            imm.hideSoftInputFromWindow(voiceInputField.windowToken, 0)
        }
    }

    private fun getVoiceLocale(): Locale {

        val savedTag = getSharedPreferences(
            "nitron_settings",
            MODE_PRIVATE
        ).getString("voice_language", null)

        return if (savedTag != null) {
            Locale.forLanguageTag(savedTag)
        } else {
            Locale.getDefault()
        }
    }


    private lateinit var chatManager: ChatManager
    private lateinit var speechRecognizer: SpeechRecognizer
    private lateinit var tts: TextToSpeech

    private lateinit var replyFrame: FrameLayout
    private lateinit var replyText: TextView
    private lateinit var micIcon: TextView
    private lateinit var voiceInputField: EditText

    private val handler = Handler(Looper.getMainLooper())

    private var isListening = false
    private var voiceModeActive = true
    private var userStopped = false

    private var ttsReady = false
    private var isNitronSpeaking = false

    private var recognizerStarting = false
    private var lastRecognizedText = ""
    private var silenceRestartCount = 0
    private var pendingChunks: MutableList<String> = mutableListOf()
    private var chunkIndex = 0
    private var bargeInWindowActive = false

    private val micPermissionRequestCode = 501

    private val restartRunnable = Runnable {
        if (
            !isFinishing &&
            voiceModeActive &&
            !userStopped &&
            !isListening &&
            !isNitronSpeaking
        ) {
            startListening()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_voice_mode)

        ChatHistoryStore.init(this)

        replyFrame = findViewById(R.id.voiceReplyFrame)
        replyText = findViewById(R.id.voiceReplyText)
        micIcon = findViewById(R.id.voiceMicIcon)
        voiceInputField = findViewById(R.id.voiceInputField)

        voiceInputField.setOnEditorActionListener { _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_SEND) {
                sendTypedMessage()
                true
            } else {
                false
            }
        }

        findViewById<TextView>(R.id.voiceSendIcon).setOnClickListener {
            sendTypedMessage()
        }

        findViewById<TextView>(R.id.voicePlusIcon).setOnClickListener {

            val panel =
                findViewById<View>(R.id.voiceActionPanel)

            panel.visibility =
                if (panel.visibility == View.VISIBLE) {
                    View.GONE
                } else {
                    View.VISIBLE
                }
        }

        chatManager = ChatManager()

        chatManager.setListener(object : ChatManager.ChatListener {

            override fun onReply(reply: String) {
                runOnUiThread {

                    ChatHistoryStore.add(
                        Message(reply, false)
                    )

                    speak(reply)
                }
            }
        })

        tts = TextToSpeech(this) { status ->

            if (status == TextToSpeech.SUCCESS) {

                val result = tts.setLanguage(getVoiceLocale())

                tts.setPitch(1.0f)
                tts.setSpeechRate(1.0f)

                ttsReady =
                    result != TextToSpeech.LANG_MISSING_DATA &&
                    result != TextToSpeech.LANG_NOT_SUPPORTED

                tts.setOnUtteranceProgressListener(
                    object : UtteranceProgressListener() {

                        override fun onStart(utteranceId: String?) {
                            runOnUiThread {
                                isNitronSpeaking = true
                            }
                        }

                        override fun onDone(utteranceId: String?) {
                            runOnUiThread {
                                chunkIndex++
                                attemptBriefListen()
                            }
                        }

                        override fun onError(utteranceId: String?) {
                            runOnUiThread {

                                isNitronSpeaking = false
                                BubbleService.setSpeaking(false)
                                pendingChunks.clear()

                                scheduleListening(700)
                            }
                        }
                    }
                )
            }
        }

        setupSpeechRecognizer()
        startOrbitAnimations()
        setupOrbDragRotation()
        makeOrbTextHollow()

        // Disabled: camera+hand-tracking overloads this device.
        // startHandGestureControl()

        /*
         * The bubble itself starts voice mode.
         * The microphone button is NOT required.
         */
        window.decorView.postDelayed({

            if (!isFinishing && voiceModeActive) {
                requestMicAndListen()
            }

        }, 500)

        /*
         * Microphone icon is now only a manual
         * stop/start control. Voice mode itself is automatic.
         */
        micIcon.setOnClickListener {

            if (isListening) {

                userStopped = true
                voiceModeActive = false

                try {
                    speechRecognizer.stopListening()
                } catch (_: Exception) {
                }

                isListening = false
                micIcon.alpha = 1.0f

            } else {

                userStopped = false
                voiceModeActive = true

                requestMicAndListen()
            }
        }

        findViewById<TextView>(R.id.voiceCloseIcon).setOnClickListener {
            finish()
        }

        findViewById<View>(R.id.voiceOrbContainer).setOnClickListener {
            if (isNitronSpeaking) {
                interruptNitron()
                if (!isListening && !recognizerStarting) {
                    requestMicAndListen()
                }
            }
        }

        findViewById<View>(R.id.voiceOrbContainer).setOnClickListener {
            if (isNitronSpeaking) {
                interruptNitron()
                if (!isListening && !recognizerStarting) {
                    requestMicAndListen()
                }
            }
        }

        findViewById<TextView>(R.id.voiceSettingsIcon).setOnClickListener {
            startActivity(
                Intent(this, SettingsActivity::class.java)
            )
        }

        findViewById<TextView>(R.id.voiceMenuIcon).setOnClickListener {

            val panel =
                findViewById<View>(R.id.voiceActionPanel)

            panel.visibility =
                if (panel.visibility == View.VISIBLE) {
                    View.GONE
                } else {
                    View.VISIBLE
                }
        }

        findViewById<TextView>(R.id.actionTalk).setOnClickListener {

            userStopped = false
            voiceModeActive = true

            if (!isListening) {
                requestMicAndListen()
            }
        }

        findViewById<TextView>(R.id.actionSettings).setOnClickListener {
            startActivity(
                Intent(this, SettingsActivity::class.java)
            )
        }

        findViewById<TextView>(R.id.actionScreenshot).setOnClickListener {
            Toast.makeText(
                this,
                "Screenshot: coming soon",
                Toast.LENGTH_SHORT
            ).show()
        }

        findViewById<TextView>(R.id.actionApps).setOnClickListener {
            startActivity(
                Intent(this, AppsListActivity::class.java)
            )
        }

        findViewById<TextView>(R.id.actionQR).setOnClickListener {
            Toast.makeText(
                this,
                "QR Scan: coming soon",
                Toast.LENGTH_SHORT
            ).show()
        }
    }

    private fun startOrbitAnimations() {

        val ring1 =
            findViewById<View>(R.id.orbitRing1)

        val ring2 =
            findViewById<View>(R.id.orbitRing2)

        val anim1 =
            ObjectAnimator.ofFloat(
                ring1,
                "rotation",
                ring1.rotation,
                ring1.rotation + 360f
            )

        anim1.duration = 9000
        anim1.repeatCount = ObjectAnimator.INFINITE
        anim1.interpolator = LinearInterpolator()
        anim1.start()

        val anim2 =
            ObjectAnimator.ofFloat(
                ring2,
                "rotation",
                ring2.rotation,
                ring2.rotation - 360f
            )

        anim2.duration = 13000
        anim2.repeatCount = ObjectAnimator.INFINITE
        anim2.interpolator = LinearInterpolator()
        anim2.start()
    }

    private fun makeOrbTextHollow() {

        val orbText =
            findViewById<TextView>(R.id.voiceOrbText)

        orbText.setLayerType(
            View.LAYER_TYPE_SOFTWARE,
            orbText.paint
        )

        orbText.paint.style =
            android.graphics.Paint.Style.STROKE

        orbText.paint.strokeWidth =
            1.3f * resources.displayMetrics.density

        orbText.invalidate()
    }

    private var orbTouchScale = 1.0f
    private lateinit var orbScaleGestureDetector: ScaleGestureDetector

    private fun setupOrbDragRotation() {
        val orb = findViewById<View>(R.id.voiceOrbContainer)

        orb.cameraDistance =
            12000 * resources.displayMetrics.density

        orbScaleGestureDetector = ScaleGestureDetector(
            this,
            object : ScaleGestureDetector.SimpleOnScaleGestureListener() {

                override fun onScale(detector: ScaleGestureDetector): Boolean {

                    orbTouchScale *= detector.scaleFactor
                    orbTouchScale = orbTouchScale.coerceIn(0.5f, 2.5f)

                    orb.scaleX = orbTouchScale
                    orb.scaleY = orbTouchScale

                    return true
                }
            }
        )

        var lastX = 0f
        var lastY = 0f

        orb.setOnTouchListener { view, event ->

            orbScaleGestureDetector.onTouchEvent(event)

            if (event.pointerCount > 1 || orbScaleGestureDetector.isInProgress) {
                return@setOnTouchListener true
            }

            when (event.actionMasked) {

                MotionEvent.ACTION_DOWN -> {
                    lastX = event.rawX
                    lastY = event.rawY
                    true
                }

                MotionEvent.ACTION_MOVE -> {

                    val dx = event.rawX - lastX
                    val dy = event.rawY - lastY

                    view.rotationY += dx * 0.4f

                    val newRotationX =
                        (
                            view.rotationX -
                            dy * 0.4f
                        ).coerceIn(-60f, 60f)

                    view.rotationX = newRotationX

                    lastX = event.rawX
                    lastY = event.rawY

                    true
                }

                MotionEvent.ACTION_UP -> {
                    true
                }

                else -> true
            }
        }
    }

    private var swipeStartX = 0f
    private var swipeStartY = 0f

    override fun dispatchTouchEvent(event: MotionEvent): Boolean {
        when (event.actionMasked) {
            MotionEvent.ACTION_DOWN -> {
                swipeStartX = event.rawX
                swipeStartY = event.rawY
            }

            MotionEvent.ACTION_UP -> {
                val dx = event.rawX - swipeStartX
                val dy = event.rawY - swipeStartY

                if (
                    dy > 120f &&
                    kotlin.math.abs(dy) > kotlin.math.abs(dx) * 1.2f
                ) {
                    collapseVoiceMode()
                    return true
                }
            }
        }

        return super.dispatchTouchEvent(event)
    }

    private fun collapseVoiceMode() {

        // The next tap on the small floating bubble
        // should open the normal chat.
        getSharedPreferences(
            "nitron_voice_state",
            MODE_PRIVATE
        )
            .edit()
            .putBoolean(
                "open_chat_on_bubble_tap",
                true
            )
            .apply()

        voiceModeActive = false
        userStopped = true

        handler.removeCallbacksAndMessages(null)

        try {
            speechRecognizer.cancel()
        } catch (_: Exception) {
        }

        try {
            tts.stop()
        } catch (_: Exception) {
        }

        isListening = false
        isNitronSpeaking = false
        recognizerStarting = false

        // Ask the existing floating-bubble service
        // to restore the small bubble at the bottom.
        try {
            BubbleService.restoreBubbleAtBottom()
        } catch (_: Exception) {
        }

        // Close the large voice interface.
        findViewById<View>(
            R.id.voiceOrbContainer
        ).animate()
            .scaleX(0.15f)
            .scaleY(0.15f)
            .alpha(0f)
            .setDuration(220)
            .withEndAction {
                finish()
            }
            .start()

        findViewById<View>(
            R.id.voiceGreeting
        ).animate()
            .alpha(0f)
            .setDuration(180)
            .start()

        findViewById<View>(
            R.id.voiceReplyFrame
        ).animate()
            .alpha(0f)
            .setDuration(180)
            .start()
    }

    private fun setupSpeechRecognizer() {

        if (!SpeechRecognizer.isRecognitionAvailable(this)) {
            Toast.makeText(
                this,
                "NITRON DEBUG: Speech recognition is not available on this device",
                Toast.LENGTH_LONG
            ).show()
        }

        speechRecognizer =
            SpeechRecognizer.createSpeechRecognizer(this)

        speechRecognizer.setRecognitionListener(
            object : RecognitionListener {

                override fun onReadyForSpeech(
                    params: Bundle?
                ) {
                    recognizerStarting = false
                    isListening = true

                    runOnUiThread {
                        micIcon.alpha = 0.5f
                    }
                }

                override fun onBeginningOfSpeech() {

                    bargeInWindowActive = false
                    pendingChunks.clear()
                    chunkIndex = 0

                    if (isNitronSpeaking) {
                        interruptNitron()
                    }
                }

                override fun onRmsChanged(
                    rmsdB: Float
                ) {
                }

                override fun onBufferReceived(
                    buffer: ByteArray?
                ) {
                }

                override fun onEndOfSpeech() {
                    /*
                     * Do not restart here.
                     * onResults/onError handles the session.
                     */
                }

                override fun onError(error: Int) {

                    recognizerStarting = false
                    isListening = false

                    runOnUiThread {
                        micIcon.alpha = 1.0f

                        Toast.makeText(
                            this@VoiceModeActivity,
                            "NITRON DEBUG: mic error code $error",
                            Toast.LENGTH_LONG
                        ).show()
                    }

                    /*
                     * Important:
                     * never hammer SpeechRecognizer with
                     * immediate restarts.
                     */
                    // Do NOT automatically start another
                    // recognition session here.
                    //
                    // Repeated SpeechRecognizer sessions cause
                    // Android's microphone "beep" to repeat.
                    // Listening will be started again when the
                    // user activates the microphone/talk control.
                }

                override fun onResults(
                    results: Bundle?
                ) {

                    recognizerStarting = false
                    isListening = false

                    runOnUiThread {
                        micIcon.alpha = 1.0f
                    }

                    val matches =
                        results?.getStringArrayList(
                            SpeechRecognizer.RESULTS_RECOGNITION
                        )

                    val spokenText =
                        matches
                            ?.firstOrNull()
                            ?.trim()

                    if (!spokenText.isNullOrBlank()) {

                        /*
                         * Ignore an accidental duplicate result.
                         */
                        if (spokenText != lastRecognizedText) {

                            lastRecognizedText =
                                spokenText

                            silenceRestartCount = 0

                            ChatHistoryStore.add(
                                Message(
                                    spokenText,
                                    true
                                )
                            )

                            /*
                             * This is the actual path that
                             * sends the user's words to Nitron,
                             * unless it was a device command like
                             * "open X" or "close", handled locally.
                             */
                            if (!tryHandleAppCommand(spokenText)) {
                                chatManager.sendMessage(
                                    spokenText
                                )
                            }

                            /*
                             * Don't reopen the microphone
                             * immediately. ChatManager will
                             * call speak() when the reply arrives.
                             */
                        }
                    } else {

                        silenceRestartCount++

                        if (silenceRestartCount <= 2) {
                            scheduleListening(700)
                        } else {
                            silenceRestartCount = 0
                            /*
                             * Stop auto-restarting after repeated
                             * silence. This is what was causing the
                             * rapid mic "beep beep" loop. The user
                             * can re-engage with the mic button.
                             */
                        }
                    }
                }

                override fun onPartialResults(
                    partialResults: Bundle?
                ) {

                    val matches =
                        partialResults?.getStringArrayList(
                            SpeechRecognizer.RESULTS_RECOGNITION
                        )

                    val partial =
                        matches?.firstOrNull()?.trim()

                    if (!partial.isNullOrBlank()) {

                        /*
                         * If Nitron is talking and the
                         * user starts speaking, stop TTS.
                         */
                        if (isNitronSpeaking) {
                            interruptNitron()
                        }
                    }
                }

                override fun onEvent(
                    eventType: Int,
                    params: Bundle?
                ) {
                }
            }
        )
    }

    private fun requestMicAndListen() {

        if (
            ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.RECORD_AUDIO
            ) != PackageManager.PERMISSION_GRANTED
        ) {

            ActivityCompat.requestPermissions(
                this,
                arrayOf(
                    Manifest.permission.RECORD_AUDIO
                ),
                micPermissionRequestCode
            )

            return
        }

        startListening()
    }

    private fun startListening() {

        if (
            isFinishing ||
            userStopped ||
            !voiceModeActive ||
            isListening ||
            recognizerStarting
        ) {
            return
        }

        recognizerStarting = true

        val intent =
            Intent(
                RecognizerIntent.ACTION_RECOGNIZE_SPEECH
            )

        intent.putExtra(
            RecognizerIntent.EXTRA_LANGUAGE_MODEL,
            RecognizerIntent.LANGUAGE_MODEL_FREE_FORM
        )

        intent.putExtra(
            RecognizerIntent.EXTRA_LANGUAGE,
            getVoiceLocale()
        )

        intent.putExtra(
            RecognizerIntent.EXTRA_PARTIAL_RESULTS,
            true
        )

        /*
         * Some Samsung / OEM devices bind the recognition
         * intent to a broken or unrelated service by default,
         * causing an immediate ERROR_NO_MATCH regardless of
         * what's said. Forcing Google's app explicitly is the
         * standard workaround.
         */
        intent.setPackage("com.google.android.googlequicksearchbox")

        /*
         * These custom silence/length timing extras were
         * removed: on some OEM speech services (e.g. Samsung)
         * they cause the recognizer to give up almost
         * immediately with ERROR_NO_MATCH. Using the
         * recognizer's own default timing instead.
         */

        try {

            speechRecognizer.startListening(intent)

        } catch (_: Exception) {

            recognizerStarting = false
            isListening = false

            micIcon.alpha = 1.0f

            scheduleListening(1200)
        }
    }

    private fun scheduleListening(delay: Long) {

        handler.removeCallbacks(restartRunnable)

        if (
            isFinishing ||
            userStopped ||
            !voiceModeActive
        ) {
            return
        }

        handler.postDelayed(
            restartRunnable,
            delay
        )
    }

    private fun tryHandleAppCommand(text: String): Boolean {

        val lower = text.trim().lowercase(Locale.getDefault())

        val closeWords = setOf(
            "close", "close this", "close app",
            "go home", "go to home screen", "exit"
        )

        if (lower in closeWords) {
            val homeIntent = Intent(Intent.ACTION_MAIN).apply {
                addCategory(Intent.CATEGORY_HOME)
                flags = Intent.FLAG_ACTIVITY_NEW_TASK
            }
            startActivity(homeIntent)
            speak("Closing.")
            return true
        }

        if (lower.startsWith("open ")) {

            val appName = lower.removePrefix("open ").trim()

            if (appName.isBlank()) {
                return false
            }

            val pm = packageManager
            val installedApps = pm.getInstalledApplications(
                PackageManager.GET_META_DATA
            ).filter {
                pm.getLaunchIntentForPackage(it.packageName) != null
            }

            val match = installedApps
                .map { it to it.loadLabel(pm).toString() }
                .filter {
                    it.second.lowercase(Locale.getDefault()).contains(appName)
                }
                .minByOrNull { it.second.length }

            if (match != null) {
                val launchIntent = pm.getLaunchIntentForPackage(
                    match.first.packageName
                )
                if (launchIntent != null) {
                    startActivity(launchIntent)
                    speak("Opening " + match.second + ".")
                    return true
                }
            }

            speak("I couldn't find an app called " + appName + ".")
            return true
        }

        return false
    }

    private fun speak(text: String) {

        if (text.isBlank()) {
            scheduleListening(500)
            return
        }

        if (!ttsReady) {

            handler.postDelayed(
                {
                    if (!isFinishing) {
                        speak(text)
                    }
                },
                300
            )

            return
        }

        pendingChunks = splitIntoSentences(text).toMutableList()
        chunkIndex = 0

        speakNextChunk()
    }

    private fun splitIntoSentences(text: String): List<String> {
        val parts = text.split(Regex("(?<=[.!?])\\s+"))
        return parts.map { it.trim() }.filter { it.isNotBlank() }
    }

    private fun speakNextChunk() {

        if (chunkIndex >= pendingChunks.size) {
            isNitronSpeaking = false
            BubbleService.setSpeaking(false)
            scheduleListening(700)
            return
        }

        isNitronSpeaking = true
        BubbleService.setSpeaking(true)

        if (isListening) {
            try {
                speechRecognizer.stopListening()
            } catch (_: Exception) {
            }
            isListening = false
            recognizerStarting = false
        }

        val chunk = pendingChunks[chunkIndex]

        val result = tts.speak(
            chunk,
            TextToSpeech.QUEUE_FLUSH,
            null,
            "nitron_chunk"
        )

        if (result == TextToSpeech.ERROR) {
            isNitronSpeaking = false
            BubbleService.setSpeaking(false)
            pendingChunks.clear()
            scheduleListening(1200)
        }
    }

    private fun attemptBriefListen() {

        isNitronSpeaking = false
        BubbleService.setSpeaking(false)

        if (isFinishing || userStopped || !voiceModeActive) {
            return
        }

        bargeInWindowActive = true

        startListening()

        handler.postDelayed(
            {
                if (bargeInWindowActive) {
                    bargeInWindowActive = false
                    try {
                        speechRecognizer.stopListening()
                    } catch (_: Exception) {
                    }
                    isListening = false
                    recognizerStarting = false
                    speakNextChunk()
                }
            },
            900
        )
    }
    private fun interruptNitron() {

        try {
            tts.stop()
        } catch (_: Exception) {
        }

        isNitronSpeaking = false
        BubbleService.setSpeaking(false)
        pendingChunks.clear()
        chunkIndex = 0
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {

        super.onRequestPermissionsResult(
            requestCode,
            permissions,
            grantResults
        )

        if (
            requestCode == micPermissionRequestCode &&
            grantResults.isNotEmpty() &&
            grantResults[0] ==
            PackageManager.PERMISSION_GRANTED
        ) {

            userStopped = false
            voiceModeActive = true

            scheduleListening(300)
        }
    }

    private fun startHandGestureControl() {

        val orb = findViewById<View>(R.id.voiceOrbContainer)

        handGestureController = HandGestureController(this, this) { spread ->

            runOnUiThread {

                try {
                    val scale = (spread * 6f).coerceIn(0.6f, 2.2f)

                    orb.scaleX = scale
                    orb.scaleY = scale
                } catch (e: Throwable) {
                    Toast.makeText(this, "NITRON DEBUG: orb scale error: ${e.message}", Toast.LENGTH_LONG).show()
                }
            }
        }

        handGestureController?.start()
    }

    override fun onDestroy() {

        handGestureController?.stop()

        voiceModeActive = false
        userStopped = true
        isNitronSpeaking = false

        handler.removeCallbacksAndMessages(null)

        try {
            speechRecognizer.cancel()
        } catch (_: Exception) {
        }

        try {
            speechRecognizer.destroy()
        } catch (_: Exception) {
        }

        try {
            tts.stop()
            tts.shutdown()
        } catch (_: Exception) {
        }

        super.onDestroy()
    }
}
