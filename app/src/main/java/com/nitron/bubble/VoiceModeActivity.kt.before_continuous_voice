package com.nitron.bubble

import android.Manifest
import android.animation.ObjectAnimator
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import android.view.MotionEvent
import android.view.View
import android.view.animation.LinearInterpolator
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

    private lateinit var chatManager: ChatManager
    private lateinit var speechRecognizer: SpeechRecognizer
    private lateinit var tts: TextToSpeech

    private lateinit var replyFrame: FrameLayout
    private lateinit var replyText: TextView
    private lateinit var micIcon: TextView

    private var isListening = false

    private val micPermissionRequestCode = 501

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_voice_mode)

        ChatHistoryStore.init(this)

        replyFrame = findViewById(R.id.voiceReplyFrame)
        replyText = findViewById(R.id.voiceReplyText)
        micIcon = findViewById(R.id.voiceMicIcon)

        chatManager = ChatManager()
        chatManager.setListener(object : ChatManager.ChatListener {
            override fun onReply(reply: String) {
                runOnUiThread {
                    replyFrame.visibility = View.VISIBLE
                    replyText.text = reply
                    speak(reply)
                    ChatHistoryStore.add(Message(reply, false))
                }
            }
        })

        tts = TextToSpeech(this) { }

        setupSpeechRecognizer()
        startOrbitAnimations()
        setupOrbDragRotation()
        makeOrbTextHollow()

        micIcon.setOnClickListener {
            if (isListening) {
                stopListening()
            } else {
                requestMicAndListen()
            }
        }

        findViewById<TextView>(R.id.voiceCloseIcon).setOnClickListener {
            finish()
        }

        findViewById<TextView>(R.id.voiceMenuIcon).setOnClickListener {
            val panel = findViewById<View>(R.id.voiceActionPanel)
            panel.visibility =
                if (panel.visibility == View.VISIBLE) View.GONE else View.VISIBLE
        }

        findViewById<TextView>(R.id.actionTalk).setOnClickListener {
            if (!isListening) requestMicAndListen()
        }

        findViewById<TextView>(R.id.actionSettings).setOnClickListener {
            startActivity(Intent(this, SettingsActivity::class.java))
        }

        findViewById<TextView>(R.id.actionScreenshot).setOnClickListener {
            Toast.makeText(this, "Screenshot: coming soon", Toast.LENGTH_SHORT).show()
        }

        findViewById<TextView>(R.id.actionApps).setOnClickListener {
            startActivity(Intent(this, AppsListActivity::class.java))
        }

        findViewById<TextView>(R.id.actionQR).setOnClickListener {
            Toast.makeText(this, "QR Scan: coming soon", Toast.LENGTH_SHORT).show()
        }
    }

    private fun startOrbitAnimations() {
        val ring1 = findViewById<View>(R.id.orbitRing1)
        val ring2 = findViewById<View>(R.id.orbitRing2)

        val anim1 = ObjectAnimator.ofFloat(ring1, "rotation", ring1.rotation, ring1.rotation + 360f)
        anim1.duration = 9000
        anim1.repeatCount = ObjectAnimator.INFINITE
        anim1.interpolator = LinearInterpolator()
        anim1.start()

        val anim2 = ObjectAnimator.ofFloat(ring2, "rotation", ring2.rotation, ring2.rotation - 360f)
        anim2.duration = 13000
        anim2.repeatCount = ObjectAnimator.INFINITE
        anim2.interpolator = LinearInterpolator()
        anim2.start()
    }

    private fun makeOrbTextHollow() {
        val orbText = findViewById<TextView>(R.id.voiceOrbText)
        orbText.setLayerType(View.LAYER_TYPE_SOFTWARE, orbText.paint)
        orbText.paint.style = android.graphics.Paint.Style.STROKE
        orbText.paint.strokeWidth = 1.3f * resources.displayMetrics.density
        orbText.invalidate()
    }

    private fun setupOrbDragRotation() {
        val orb = findViewById<View>(R.id.voiceOrbContainer)
        orb.cameraDistance = 12000 * resources.displayMetrics.density

        var lastX = 0f
        var lastY = 0f

        orb.setOnTouchListener { view, event ->
            when (event.actionMasked) {
                MotionEvent.ACTION_DOWN -> {
                    lastX = event.rawX
                    lastY = event.rawY
                    true
                }
                MotionEvent.ACTION_MOVE -> {
                    val dx = event.rawX - lastX
                    val dy = event.rawY - lastY

                    // East-west drag spins around the vertical axis
                    view.rotationY += dx * 0.4f

                    // North-south drag tilts around the horizontal axis, clamped
                    val newRotationX = (view.rotationX - dy * 0.4f).coerceIn(-60f, 60f)
                    view.rotationX = newRotationX

                    lastX = event.rawX
                    lastY = event.rawY
                    true
                }
                else -> true
            }
        }
    }

    private fun setupSpeechRecognizer() {
        speechRecognizer = SpeechRecognizer.createSpeechRecognizer(this)
        speechRecognizer.setRecognitionListener(object : RecognitionListener {

            override fun onReadyForSpeech(params: Bundle?) {}
            override fun onBeginningOfSpeech() {}
            override fun onRmsChanged(rmsdB: Float) {}
            override fun onBufferReceived(buffer: ByteArray?) {}
            override fun onEndOfSpeech() {}

            override fun onError(error: Int) {
                isListening = false
                micIcon.alpha = 1.0f
            }

            override fun onResults(results: Bundle?) {
                val matches = results?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
                val spokenText = matches?.firstOrNull()?.trim()

                isListening = false
                micIcon.alpha = 1.0f

                if (!spokenText.isNullOrBlank()) {
                    ChatHistoryStore.add(Message(spokenText, true))
                    chatManager.sendMessage(spokenText)
                }
            }

            override fun onPartialResults(partialResults: Bundle?) {
                val matches = partialResults?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
                val partial = matches?.firstOrNull()
                if (!partial.isNullOrBlank()) {
                    replyFrame.visibility = View.VISIBLE
                    replyText.text = partial
                }
            }

            override fun onEvent(eventType: Int, params: Bundle?) {}
        })
    }

    private fun requestMicAndListen() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO)
            != PackageManager.PERMISSION_GRANTED
        ) {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.RECORD_AUDIO),
                micPermissionRequestCode
            )
            return
        }
        startListening()
    }

    private fun startListening() {
        isListening = true
        micIcon.alpha = 0.5f

        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
        intent.putExtra(
            RecognizerIntent.EXTRA_LANGUAGE_MODEL,
            RecognizerIntent.LANGUAGE_MODEL_FREE_FORM
        )
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault())
        intent.putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, true)

        try {
            speechRecognizer.startListening(intent)
        } catch (_: Exception) {
            isListening = false
            micIcon.alpha = 1.0f
        }
    }

    private fun stopListening() {
        isListening = false
        micIcon.alpha = 1.0f
        try {
            speechRecognizer.stopListening()
        } catch (_: Exception) {
        }
    }

    private fun speak(text: String) {
        tts.setOnUtteranceProgressListener(object : UtteranceProgressListener() {
            override fun onStart(utteranceId: String?) {}
            override fun onDone(utteranceId: String?) {}
            override fun onError(utteranceId: String?) {}
        })
        tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, "nitron_reply")
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == micPermissionRequestCode &&
            grantResults.isNotEmpty() &&
            grantResults[0] == PackageManager.PERMISSION_GRANTED
        ) {
            startListening()
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        try {
            speechRecognizer.destroy()
        } catch (_: Exception) {
        }
        try {
            tts.stop()
            tts.shutdown()
        } catch (_: Exception) {
        }
    }
}
