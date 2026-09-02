package com.nitron.bubble

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Bundle
import android.provider.Settings
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import android.util.Base64

import com.google.android.gms.auth.api.signin.GoogleSignIn
import com.google.android.gms.auth.api.signin.GoogleSignInClient
import com.google.android.gms.auth.api.signin.GoogleSignInOptions
import com.google.android.gms.common.api.ApiException
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.GoogleAuthProvider
import android.view.View
import android.view.WindowInsets
import android.widget.EditText
import android.widget.ImageButton
import android.widget.TextView
import androidx.activity.OnBackPressedCallback
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.app.AppCompatDelegate
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.drawerlayout.widget.DrawerLayout
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.nitron.bubble.chat.ChatManager
import com.nitron.bubble.chat.ChatHistoryStore
import com.nitron.bubble.chat.Message
import com.nitron.bubble.chat.MessageAdapter
import java.io.ByteArrayOutputStream

class MainActivity : AppCompatActivity() {

    // =========================================================
    // VARIABLES
    // =========================================================

    private var speechRecognizer: SpeechRecognizer? = null
    private var isRecordingVoice = false

    // =========================================================
    // GOOGLE SIGN-IN
    // =========================================================

    private val googleSignInLauncher =
        registerForActivityResult(
            ActivityResultContracts.StartActivityForResult()
        ) { result ->

            val task =
                GoogleSignIn.getSignedInAccountFromIntent(result.data)

            try {

                val account = task.getResult(ApiException::class.java)
                val idToken = account?.idToken

                if (idToken != null) {
                    firebaseAuthWithGoogle(idToken)
                } else {
                    addMessage(
                        Message(
                            "Google sign-in failed: no ID token returned.",
                            false
                        )
                    )
                }

            } catch (e: ApiException) {

                addMessage(
                    Message(
                        "Google sign-in failed: ${e.statusCode}",
                        false
                    )
                )
            }
        }

    private fun signInWithGoogle() {
        googleSignInLauncher.launch(googleSignInClient.signInIntent)
    }

    private fun firebaseAuthWithGoogle(idToken: String) {

        val credential = GoogleAuthProvider.getCredential(idToken, null)

        firebaseAuth.signInWithCredential(credential)
            .addOnCompleteListener(this) { task ->

                if (task.isSuccessful) {

                    val user = firebaseAuth.currentUser

                    addMessage(
                        Message(
                            "Signed in as ${user?.displayName ?: user?.email ?: "Google account"}.",
                            false
                        )
                    )

                    updateSignInButtonText()

                } else {

                    addMessage(
                        Message(
                            "Firebase sign-in failed: ${task.exception?.message}",
                            false
                        )
                    )
                }
            }
    }

    private fun updateSignInButtonText() {

        if (!::signInButtonView.isInitialized) return

        val user = firebaseAuth.currentUser

        signInButtonView.text = if (user != null) {
            "👤  Signed in as ${user.displayName ?: user.email ?: "Google"}"
        } else {
            "👤  Sign in with Google"
        }
    }

    private lateinit var drawerLayout: DrawerLayout
    private lateinit var messageInput: EditText
    private lateinit var welcomeText: TextView
    private lateinit var messageList: RecyclerView
    private lateinit var messageAdapter: MessageAdapter
    private lateinit var chatManager: ChatManager
    private lateinit var googleSignInClient: GoogleSignInClient
    private lateinit var firebaseAuth: FirebaseAuth
    private lateinit var signInButtonView: TextView

    // =========================================================
    // MICROPHONE PERMISSION
    // =========================================================

    private val microphonePermission =
        registerForActivityResult(
            ActivityResultContracts.RequestPermission()
        ) { granted ->
            if (granted) {
                startVoiceInput()
            } else {
                showMicrophonePermissionMessage()
            }
        }

    private fun requestMicrophonePermission() {

        when {
            ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.RECORD_AUDIO
            ) == PackageManager.PERMISSION_GRANTED -> {
                startVoiceInput()
            }

            ActivityCompat.shouldShowRequestPermissionRationale(
                this,
                Manifest.permission.RECORD_AUDIO
            ) -> {
                showMicrophonePermissionMessage()
            }

            else -> {
                microphonePermission.launch(
                    Manifest.permission.RECORD_AUDIO
                )
            }
        }
    }

    // =========================================================
    // VOICE INPUT
    // =========================================================

    private fun startVoiceInput() {

        if (!SpeechRecognizer.isRecognitionAvailable(this)) {

            AlertDialog.Builder(this)
                .setTitle("Voice input unavailable")
                .setMessage(
                    "Voice recognition is not available on this device."
                )
                .setPositiveButton("OK", null)
                .show()

            return
        }

        stopVoiceInput()

        speechRecognizer =
            SpeechRecognizer.createSpeechRecognizer(this)

        speechRecognizer?.setRecognitionListener(
            object : RecognitionListener {

                override fun onReadyForSpeech(params: Bundle?) {
                    isRecordingVoice = true
                    messageInput.hint = "Listening..."
                }

                override fun onBeginningOfSpeech() {
                    isRecordingVoice = true
                }

                override fun onRmsChanged(rmsdB: Float) {
                }

                override fun onBufferReceived(buffer: ByteArray?) {
                }

                override fun onEndOfSpeech() {
                    isRecordingVoice = false
                    messageInput.hint = "Message Nitron"
                }

                override fun onError(error: Int) {
                    isRecordingVoice = false
                    messageInput.hint = "Message Nitron"
                }

                override fun onResults(results: Bundle?) {

                    isRecordingVoice = false
                    messageInput.hint = "Message Nitron"

                    val matches =
                        results?.getStringArrayList(
                            SpeechRecognizer.RESULTS_RECOGNITION
                        )

                    if (!matches.isNullOrEmpty()) {

                        val spokenText = matches[0]

                        val existingText =
                            messageInput.text.toString().trim()

                        val finalText =
                            if (existingText.isEmpty()) {
                                spokenText
                            } else {
                                "$existingText $spokenText"
                            }

                        messageInput.setText(finalText)

                        messageInput.setSelection(
                            messageInput.text.length
                        )
                    }
                }

                override fun onPartialResults(
                    partialResults: Bundle?
                ) {

                    val matches =
                        partialResults?.getStringArrayList(
                            SpeechRecognizer.RESULTS_RECOGNITION
                        )

                    if (!matches.isNullOrEmpty()) {

                        messageInput.setText(matches[0])

                        messageInput.setSelection(
                            messageInput.text.length
                        )
                    }
                }

                override fun onEvent(
                    eventType: Int,
                    params: Bundle?
                ) {
                }
            }
        )

        val intent =
            Intent(
                RecognizerIntent.ACTION_RECOGNIZE_SPEECH
            ).apply {

                putExtra(
                    RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                    RecognizerIntent.LANGUAGE_MODEL_FREE_FORM
                )

                putExtra(
                    RecognizerIntent.EXTRA_PARTIAL_RESULTS,
                    true
                )

                putExtra(
                    RecognizerIntent.EXTRA_MAX_RESULTS,
                    1
                )
            }

        isRecordingVoice = true

        speechRecognizer?.startListening(intent)
    }

    private fun stopVoiceInput() {

        isRecordingVoice = false

        speechRecognizer?.stopListening()
        speechRecognizer?.cancel()
        speechRecognizer?.destroy()

        speechRecognizer = null

        if (::messageInput.isInitialized) {
            messageInput.hint = "Message Nitron"
        }
    }

    private fun showMicrophonePermissionMessage() {

        AlertDialog.Builder(this)
            .setTitle("Microphone permission")
            .setMessage(
                "Nitron needs microphone access for voice input."
            )
            .setPositiveButton("Open Settings") { _, _ ->

                val intent =
                    Intent(
                        Settings.ACTION_APPLICATION_DETAILS_SETTINGS,
                        Uri.parse("package:$packageName")
                    )

                startActivity(intent)
            }
            .setNegativeButton("Cancel", null)
            .show()
    }

    // =========================================================
    // IMAGE PICKER
    // =========================================================

    private val photoPicker =
        registerForActivityResult(
            ActivityResultContracts.GetContent()
        ) { uri ->

            if (uri == null) return@registerForActivityResult

            try {

                val bytes =
                    contentResolver
                        .openInputStream(uri)
                        .use { input ->

                            if (input == null) {
                                throw Exception(
                                    "Could not open selected image."
                                )
                            }

                            val output =
                                ByteArrayOutputStream()

                            val buffer =
                                ByteArray(8192)

                            while (true) {

                                val count =
                                    input.read(buffer)

                                if (count == -1) break

                                output.write(
                                    buffer,
                                    0,
                                    count
                                )
                            }

                            output.toByteArray()
                        }

                if (bytes.isEmpty()) {
                    throw Exception(
                        "Selected image is empty."
                    )
                }

                val base64Image =
                    Base64.encodeToString(
                        bytes,
                        Base64.NO_WRAP
                    )

                val filename =
                    uri.lastPathSegment
                        ?.substringAfterLast("/")
                        ?.substringAfterLast(":")
                        ?.takeIf { it.isNotBlank() }
                        ?: "picture.jpg"

                welcomeText.visibility = View.GONE

                addMessage(
                    Message(
                        "📷 Learning image: $filename",
                        true
                    )
                )

                scrollToBottom()

                TermuxBridge.sendImage(
                    base64Image,
                    filename
                ) { reply ->

                    runOnUiThread {

                        addMessage(
                            Message(
                                reply,
                                false
                            )
                        )

                        scrollToBottom()
                    }
                }

            } catch (e: Exception) {

                addMessage(
                    Message(
                        "Could not read image: ${e.message}",
                        false
                    )
                )

                scrollToBottom()
            }
        }

    // =========================================================
    // THEME
    // =========================================================

    private fun applySavedTheme() {

        val mode =
            getSharedPreferences(
                "nitron_settings",
                MODE_PRIVATE
            )
                .getString(
                    "theme",
                    "system"
                )

        when (mode) {

            "light" ->
                AppCompatDelegate.setDefaultNightMode(
                    AppCompatDelegate.MODE_NIGHT_NO
                )

            "dark" ->
                AppCompatDelegate.setDefaultNightMode(
                    AppCompatDelegate.MODE_NIGHT_YES
                )

            else ->
                AppCompatDelegate.setDefaultNightMode(
                    AppCompatDelegate.MODE_NIGHT_FOLLOW_SYSTEM
                )
        }
    }

    // =========================================================
    // MESSAGE HANDLING
    // =========================================================

    private fun addMessage(message: Message) {

        messageAdapter.addMessage(message)

        ChatHistoryStore.add(message)
    }

    private fun scrollToBottom() {

        if (messageAdapter.itemCount > 0) {

            messageList.smoothScrollToPosition(
                messageAdapter.itemCount - 1
            )
        }
    }

    // =========================================================
    // ACTIVITY
    // =========================================================

    override fun onCreate(
        savedInstanceState: Bundle?
    ) {

        super.onCreate(savedInstanceState)

        applySavedTheme()

        setContentView(R.layout.activity_main)

        setupKeyboardInsets()

        // -----------------------------------------------------
        // UI
        // -----------------------------------------------------

        drawerLayout =
            findViewById(R.id.drawerLayout)

        messageInput =
            findViewById(R.id.messageInput)

        welcomeText =
            findViewById(R.id.welcomeText)

        messageList =
            findViewById(R.id.messageList)

        // -----------------------------------------------------
        // CHAT
        // -----------------------------------------------------

        messageAdapter =
            MessageAdapter()

        messageList.layoutManager =
            LinearLayoutManager(this)

        messageList.adapter =
            messageAdapter

        ChatHistoryStore.init(this)

        for (pastMessage in ChatHistoryStore.getAll()) {

            messageAdapter.addMessage(
                pastMessage
            )
        }

        // -----------------------------------------------------
        // CHAT MANAGER
        // -----------------------------------------------------

        chatManager =
            ChatManager()

        chatManager.setListener(
            object : ChatManager.ChatListener {

                override fun onReply(
                    reply: String
                ) {

                    runOnUiThread {

                        addMessage(
                            Message(
                                reply,
                                false
                            )
                        )

                        scrollToBottom()
                    }
                }
            }
        )

        // =====================================================
        // BUTTONS
        // =====================================================

        val menuButton =
            findViewById<ImageButton>(
                R.id.menuButton
            )

        val editButton =
            findViewById<ImageButton>(
                R.id.editButton
            )

        val micButton =
            findViewById<ImageButton>(
                R.id.micButton
            )

        val closeButton =
            findViewById<ImageButton>(
                R.id.closeButton
            )

        val sendButton =
            findViewById<ImageButton>(
                R.id.sendButton
            )

        val attachButton =
            findViewById<ImageButton>(
                R.id.attachButton
            )

        val voiceModeButton =
            findViewById<ImageButton>(
                R.id.voiceModeButton
            )

        // -----------------------------------------------------
        // SEND / VOICE MODE
        // -----------------------------------------------------

        sendButton.visibility = View.GONE

        messageInput.addTextChangedListener(
            object : android.text.TextWatcher {

                override fun beforeTextChanged(
                    s: CharSequence?,
                    start: Int,
                    count: Int,
                    after: Int
                ) {
                }

                override fun onTextChanged(
                    s: CharSequence?,
                    start: Int,
                    before: Int,
                    count: Int
                ) {
                }

                override fun afterTextChanged(
                    s: android.text.Editable?
                ) {

                    if (s.isNullOrBlank()) {

                        sendButton.visibility =
                            View.GONE

                        voiceModeButton.visibility =
                            View.VISIBLE

                    } else {

                        sendButton.visibility =
                            View.VISIBLE

                        voiceModeButton.visibility =
                            View.GONE
                    }
                }
            }
        )

        voiceModeButton.setOnClickListener {

            startActivity(
                Intent(
                    this,
                    VoiceModeActivity::class.java
                )
            )
        }

        findViewById<ImageButton>(
            R.id.downArrowButton
        ).setOnClickListener {

            scrollToBottom()
        }

        // -----------------------------------------------------
        // MICROPHONE
        // -----------------------------------------------------

        micButton.setOnClickListener {

            if (isRecordingVoice) {
                stopVoiceInput()
            } else {
                requestMicrophonePermission()
            }
        }

        // -----------------------------------------------------
        // BUBBLE
        // -----------------------------------------------------

        findViewById<TextView>(
            R.id.realStartBubble
        ).setOnClickListener {

            if (!Settings.canDrawOverlays(this)) {

                startActivity(
                    Intent(
                        Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                        Uri.parse(
                            "package:$packageName"
                        )
                    )
                )

            } else {

                startService(
                    Intent(
                        this,
                        BubbleService::class.java
                    )
                )
            }
        }

        // -----------------------------------------------------
        // IMAGE
        // -----------------------------------------------------

        attachButton.setOnClickListener {

            photoPicker.launch("image/*")
        }

        // =====================================================
        // DRAWER
        // =====================================================

        menuButton.setOnClickListener {

            drawerLayout.openDrawer(
                android.view.Gravity.START
            )
        }

        // -----------------------------------------------------
        // NEW CHAT
        // -----------------------------------------------------

        editButton.setOnClickListener {

            stopVoiceInput()

            messageInput.setText("")

            welcomeText.text =
                "How can I help?"

            welcomeText.visibility =
                View.VISIBLE

            drawerLayout.closeDrawers()
        }

        // -----------------------------------------------------
        // CLOSE / CLEAR
        // -----------------------------------------------------

        closeButton.setOnClickListener {

            stopVoiceInput()

            messageInput.setText("")

            messageInput.clearFocus()

            messageInput.hint =
                "Message Nitron"
        }

        // -----------------------------------------------------
        // SEND
        // -----------------------------------------------------

        sendButton.setOnClickListener {

            stopVoiceInput()

            val text =
                messageInput.text
                    .toString()
                    .trim()

            if (text.isEmpty()) return@setOnClickListener

            welcomeText.visibility =
                View.GONE

            addMessage(
                Message(
                    text,
                    true
                )
            )

            scrollToBottom()

            messageInput.setText("")

            chatManager.sendMessage(text)
        }

        // =====================================================
        // SIDE MENU
        // =====================================================

        findViewById<TextView>(
            R.id.projectsButton
        ).setOnClickListener {

            drawerLayout.closeDrawers()

            startActivity(
                Intent(
                    this,
                    ProjectsActivity::class.java
                )
            )
        }

        findViewById<TextView>(
            R.id.libraryButton
        ).setOnClickListener {

            drawerLayout.closeDrawers()

            welcomeText.text =
                "Library"

            welcomeText.visibility =
                View.VISIBLE
        }

        findViewById<TextView>(
            R.id.imagesButton
        ).setOnClickListener {

            drawerLayout.closeDrawers()

            welcomeText.text =
                "Images"

            welcomeText.visibility =
                View.VISIBLE
        }

        findViewById<TextView>(
            R.id.recentButton
        ).setOnClickListener {

            drawerLayout.closeDrawers()

            welcomeText.text =
                "Recent"

            welcomeText.visibility =
                View.VISIBLE
        }

        findViewById<TextView>(
            R.id.settingsButton
        ).setOnClickListener {

            startActivity(
                Intent(
                    this,
                    SettingsActivity::class.java
                )
            )
        }

        // =====================================================
        // BACK BUTTON
        // =====================================================

        onBackPressedDispatcher.addCallback(
            this,
            object : OnBackPressedCallback(true) {

                override fun handleOnBackPressed() {

                    when {

                        drawerLayout.isDrawerOpen(
                            android.view.Gravity.START
                        ) -> {

                            drawerLayout.closeDrawers()
                        }

                        isRecordingVoice -> {

                            stopVoiceInput()
                        }

                        else -> {

                            finish()
                        }
                    }
                }
            }
        )
    }

    // =========================================================
    // KEYBOARD
    // =========================================================

    private fun setupKeyboardInsets() {

        if (android.os.Build.VERSION.SDK_INT >= 30) {

            window.decorView.setOnApplyWindowInsetsListener {
                    view,
                    insets ->

                val imeInsets =
                    insets.getInsets(
                        WindowInsets.Type.ime()
                    )

                view.setPadding(
                    view.paddingLeft,
                    view.paddingTop,
                    view.paddingRight,
                    imeInsets.bottom
                )

                insets
            }
        }
    }

    // =========================================================
    // DESTROY
    // =========================================================

    override fun onDestroy() {

        stopVoiceInput()

        super.onDestroy()
    }
}
