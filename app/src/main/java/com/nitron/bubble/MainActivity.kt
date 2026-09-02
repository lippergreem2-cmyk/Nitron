package com.nitron.bubble
import com.google.android.gms.ads.AdRequest
import com.google.android.gms.ads.AdView
import com.google.android.gms.ads.MobileAds

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.location.Geocoder
import android.location.Location
import android.net.Uri
import android.os.Bundle
import android.provider.Settings
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import android.view.View
import android.view.WindowInsets
import android.os.Handler
import android.os.Looper
import android.widget.EditText
import android.widget.ImageButton
import android.widget.TextView
import android.widget.LinearLayout
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
import com.nitron.bubble.chat.Message
import com.nitron.bubble.chat.MessageAdapter
import java.io.ByteArrayOutputStream
import java.util.Locale
import android.util.Base64

import com.google.android.gms.auth.api.signin.GoogleSignIn
import com.google.android.gms.auth.api.signin.GoogleSignInClient
import com.google.android.gms.auth.api.signin.GoogleSignInOptions
import com.google.android.gms.common.api.ApiException
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.GoogleAuthProvider


class MainActivity : AppCompatActivity() {

    // =========================================================
    // VOICE
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

                    updateSignInButtonText()
                    updateWelcomeGreeting()

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

    private fun updateWelcomeGreeting() {

        if (!::welcomeText.isInitialized) return

        val user = firebaseAuth.currentUser

        if (user == null) {
            welcomeText.text = "How can I help?"
            return
        }

        val firstName = (user.displayName ?: user.email ?: "there")
            .trim()
            .split(" ")
            .firstOrNull()
            ?: "there"

        val hour = java.util.Calendar.getInstance().get(java.util.Calendar.HOUR_OF_DAY)

        val greeting = when {
            hour < 12 -> "Good morning"
            hour < 17 -> "Good afternoon"
            else -> "Good evening"
        }

        welcomeText.text = "$greeting $firstName, how may I help you?"
    }

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

                override fun onRmsChanged(rmsdB: Float) {}

                override fun onBufferReceived(buffer: ByteArray?) {}

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
                            messageInput.text
                                .toString()
                                .trim()

                        if (existingText.isEmpty()) {
                            messageInput.setText(spokenText)
                        } else {
                            messageInput.setText(
                                "$existingText $spokenText"
                            )
                        }

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
                ) {}
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

                startActivity(
                    Intent(
                        Settings.ACTION_APPLICATION_DETAILS_SETTINGS,
                        Uri.parse("package:$packageName")
                    )
                )
            }
            .setNegativeButton("Cancel", null)
            .show()
    }


    // =========================================================
    // LOCATION
    // =========================================================

    private val locationPermission =
        registerForActivityResult(
            ActivityResultContracts.RequestMultiplePermissions()
        ) { permissions ->

            val fine =
                permissions[
                    Manifest.permission.ACCESS_FINE_LOCATION
                ] == true

            val coarse =
                permissions[
                    Manifest.permission.ACCESS_COARSE_LOCATION
                ] == true

            if (fine || coarse) {
                showMyLocation()
            } else {

                AlertDialog.Builder(this)
                    .setTitle("Location permission")
                    .setMessage(
                        "Nitron needs location permission to locate this device."
                    )
                    .setPositiveButton("OK", null)
                    .show()
            }
        }

    private fun requestLocation() {

        val fineGranted =
            ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_FINE_LOCATION
            ) == PackageManager.PERMISSION_GRANTED

        val coarseGranted =
            ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_COARSE_LOCATION
            ) == PackageManager.PERMISSION_GRANTED

        if (fineGranted || coarseGranted) {
            showMyLocation()
        } else {

            locationPermission.launch(
                arrayOf(
                    Manifest.permission.ACCESS_FINE_LOCATION,
                    Manifest.permission.ACCESS_COARSE_LOCATION
                )
            )
        }
    }

    private fun showMyLocation() {

        val locator =
            GpsLocator(this)

        val location =
            locator.getBestLastKnownLocation()

        if (location == null) {

            AlertDialog.Builder(this)
                .setTitle("Location unavailable")
                .setMessage(
                    "Nitron could not find a recent device location. Make sure Location is turned on and try again."
                )
                .setPositiveButton("OK", null)
                .show()

            return
        }

        val latitude =
            location.latitude

        val longitude =
            location.longitude

        val accuracy =
            location.accuracy

        // Start with safe defaults.
        var country = "Unknown"
        var region = "Unknown"
        var county = "Unknown"
        var city = "Unknown"
        var place = "Unknown"

        try {

            if (Geocoder.isPresent()) {

                @Suppress("DEPRECATION")
                val geocoder =
                    Geocoder(
                        this,
                        Locale.getDefault()
                    )

                @Suppress("DEPRECATION")
                val addresses =
                    geocoder.getFromLocation(
                        latitude,
                        longitude,
                        1
                    )

                if (!addresses.isNullOrEmpty()) {

                    val address =
                        addresses[0]

                    country =
                        address.countryName
                            ?: "Unknown"

                    region =
                        address.adminArea
                            ?: "Unknown"

                    county =
                        address.subAdminArea
                            ?: address.adminArea
                            ?: "Unknown"

                    city =
                        address.locality
                            ?: address.subAdminArea
                            ?: address.adminArea
                            ?: "Unknown"

                    place =
                        address.getAddressLine(0)
                            ?: "Unknown"
                }
            }

        } catch (_: Exception) {
            // Coordinates remain usable even if
            // reverse geocoding is unavailable.
        }

        val result =
            """
            📍 NITRON DEVICE LOCATION

            🌍 Country:
            $country

            🗺️ Region:
            $region

            🏙️ County:
            $county

            📌 City / Place:
            $city

            🏠 Address:
            $place

            🌐 Latitude:
            $latitude

            🌐 Longitude:
            $longitude

            🎯 Accuracy:
            ±${accuracy.toInt()} meters
            """.trimIndent()

        AlertDialog.Builder(this)
            .setTitle("My Location")
            .setMessage(result)
            .setPositiveButton("OK", null)
            .show()
    }


    // =========================================================
    // IMAGE PICKER
    // =========================================================

    private val photoPicker =
        registerForActivityResult(
            ActivityResultContracts.GetContent()
        ) { uri ->

            if (uri == null) {
                return@registerForActivityResult
            }

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

                                if (count == -1) {
                                    break
                                }

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
                        ?.takeIf {
                            it.isNotBlank()
                        }
                        ?: "picture.jpg"

                welcomeText.visibility =
                    View.GONE

                addMessage(
                    Message(
                        "📷 Learning image: $filename",
                        true
                    )
                )

                messageList.smoothScrollToPosition(
                    messageAdapter.itemCount - 1
                )

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

                        messageList.smoothScrollToPosition(
                            messageAdapter.itemCount - 1
                        )
                    }
                }

            } catch (e: Exception) {

                runOnUiThread {

                    addMessage(
                        Message(
                            "Could not read image: ${e.message}",
                            false
                        )
                    )

                    messageList.smoothScrollToPosition(
                        messageAdapter.itemCount - 1
                    )
                }
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
    // UI
    // =========================================================

    private lateinit var drawerLayout: DrawerLayout
    private lateinit var messageInput: EditText
    private lateinit var welcomeText: TextView
    private lateinit var messageList: RecyclerView
    private lateinit var messageAdapter: MessageAdapter
    private lateinit var chatManager: ChatManager
    private lateinit var googleSignInClient: GoogleSignInClient
    private lateinit var firebaseAuth: FirebaseAuth
    private lateinit var signInButtonView: TextView
    private lateinit var sideMenu: LinearLayout
    private val recentSessionViews = mutableListOf<View>()


    // IMPORTANT:
    // This adds to the adapter AND saves the message.
    // It does NOT recursively call itself.
    private fun addMessage(
        message: Message
    ) {

        messageAdapter.addMessage(message)

        com.nitron.bubble.chat.ChatHistoryStore.add(
            message
        )
    }


    // =========================================================
    // ACTIVITY
    // =========================================================

    override fun onCreate(
        savedInstanceState: Bundle?
    ) {

        super.onCreate(savedInstanceState)

        applySavedTheme()

        setContentView(
            R.layout.activity_main
        )

        // =====================================================
        // ADMOB TEST BANNER
        // =====================================================

        MobileAds.initialize(this)

        firebaseAuth = FirebaseAuth.getInstance()

        val googleSignInOptions =
            GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
                .requestIdToken("288294300264-qcb76rdmkc56knip3jq8h0f658sgft6m.apps.googleusercontent.com")
                .requestEmail()
                .build()

        googleSignInClient = GoogleSignIn.getClient(this, googleSignInOptions)

        val adView = findViewById<AdView>(R.id.adView)
        val adRequest = AdRequest.Builder().build()
        adView.loadAd(adRequest)

        drawerLayout =
            findViewById(R.id.drawerLayout)

        sideMenu =
            findViewById(R.id.sideMenu)

        messageInput =
            findViewById(R.id.messageInput)

        welcomeText =
            findViewById(R.id.welcomeText)

        updateWelcomeGreeting()

        messageList =
            findViewById(R.id.messageList)

        messageAdapter =
            MessageAdapter()

        messageList.layoutManager =
            LinearLayoutManager(this)

        messageList.adapter =
            messageAdapter

        com.nitron.bubble.chat.ChatHistoryStore.init(this)
        com.nitron.bubble.chat.ChatSessionStore.init(this)

        for (
            pastMessage
            in com.nitron.bubble.chat.ChatHistoryStore.getAll()
        ) {

            messageAdapter.addMessage(
                pastMessage
            )
        }


        // =====================================================
        // CHAT MANAGER
        // =====================================================

        chatManager =
            ChatManager()

        chatManager.setListener(
            object :
                ChatManager.ChatListener {

                override fun onReply(
                    reply: String
                ) {

                    runOnUiThread {

                        val (cleanText, imageUrl) =
                            com.nitron.bubble.TermuxBridge.extractImage(reply)

                        addMessage(
                            Message(
                                cleanText,
                                false,
                                imageUri = imageUrl
                            )
                        )

                        messageList.smoothScrollToPosition(
                            messageAdapter.itemCount - 1
                        )
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

        sendButton.visibility =
            View.GONE


        // =====================================================
        // TEXT INPUT
        // =====================================================

        messageInput.addTextChangedListener(
            object : android.text.TextWatcher {

                override fun beforeTextChanged(
                    s: CharSequence?,
                    start: Int,
                    count: Int,
                    after: Int
                ) {}

                override fun onTextChanged(
                    s: CharSequence?,
                    start: Int,
                    before: Int,
                    count: Int
                ) {}

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


        // =====================================================
        // VOICE MODE
        // =====================================================

        voiceModeButton.setOnClickListener {

            startActivity(
                Intent(
                    this,
                    VoiceModeActivity::class.java
                )
            )
        }


        // =====================================================
        // DOWN ARROW
        // =====================================================

        findViewById<ImageButton>(
            R.id.downArrowButton
        ).setOnClickListener {

            if (messageAdapter.itemCount > 0) {

                messageList.smoothScrollToPosition(
                    messageAdapter.itemCount - 1
                )
            }
        }


        // =====================================================
        // MICROPHONE
        // =====================================================

        micButton.setOnClickListener {

            if (isRecordingVoice) {
                stopVoiceInput()
            } else {
                requestMicrophonePermission()
            }
        }


        // =====================================================
        // IMAGE ATTACHMENT
        // =====================================================

        attachButton.setOnClickListener {

            photoPicker.launch(
                "image/*"
            )
        }


        // =====================================================
        // SIDE MENU
        // =====================================================

        menuButton.setOnClickListener {

            drawerLayout.openDrawer(
                android.view.Gravity.START
            )
        }


        // =====================================================
        // NEW CHAT
        // =====================================================

        editButton.setOnClickListener {
            performNewChat()
        }

        val newChatButton =
            findViewById<TextView>(R.id.newChatButton)

        newChatButton.setOnClickListener {
            performNewChat()
        }


        // =====================================================
        // CLOSE / CLEAR
        // =====================================================

        closeButton.setOnClickListener {

            if (isRecordingVoice) {
                stopVoiceInput()
            }

            messageInput.setText("")

            messageInput.clearFocus()

            messageInput.hint =
                "Message Nitron"
        }


        // =====================================================
        // SEND
        // =====================================================

        sendButton.setOnClickListener {

            if (isRecordingVoice) {
                stopVoiceInput()
            }

            val text =
                messageInput.text
                    .toString()
                    .trim()

            if (text.isNotEmpty()) {

                welcomeText.visibility =
                    View.GONE

                addMessage(
                    Message(
                        text,
                        true
                    )
                )

                messageList.smoothScrollToPosition(
                    messageAdapter.itemCount - 1
                )

                messageInput.setText("")

                chatManager.sendMessage(text)
            }
        }


        // =====================================================
        // DRAWER: PROJECTS
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


        // =====================================================
        // DRAWER: LIBRARY
        // =====================================================

        findViewById<TextView>(
            R.id.libraryButton
        ).setOnClickListener {

            drawerLayout.closeDrawers()

            welcomeText.text =
                "Library"

            welcomeText.visibility =
                View.VISIBLE

            Handler(Looper.getMainLooper()).postDelayed({
                welcomeText.visibility = View.GONE
            }, 2000)
        }


        // =====================================================
        // DRAWER: IMAGES
        // =====================================================

        findViewById<TextView>(
            R.id.imagesButton
        ).setOnClickListener {

            drawerLayout.closeDrawers()

            welcomeText.text =
                "Images"

            welcomeText.visibility =
                View.VISIBLE

            Handler(Looper.getMainLooper()).postDelayed({
                welcomeText.visibility = View.GONE
            }, 2000)
        }


        // =====================================================
        // DRAWER: RECENT
        // =====================================================

        findViewById<TextView>(
            R.id.recentButton
        ).setOnClickListener {

            toggleRecentChats()
        }


        // =====================================================
        // DRAWER: SETTINGS
        // =====================================================

        findViewById<TextView>(
            R.id.settingsButton
        ).setOnClickListener {

            drawerLayout.closeDrawers()

            startActivity(
                Intent(
                    this,
                    SettingsActivity::class.java
                )
            )
        }


        // =====================================================
        // SIGN IN WITH GOOGLE
        // =====================================================

        signInButtonView = findViewById(R.id.signInButton)

        updateSignInButtonText()

        signInButtonView.setOnClickListener {

            drawerLayout.closeDrawers()

            if (firebaseAuth.currentUser == null) {
                signInWithGoogle()
            } else {

                firebaseAuth.signOut()
                googleSignInClient.signOut()
                updateSignInButtonText()
                updateWelcomeGreeting()

                addMessage(
                    Message(
                        "Signed out.",
                        false
                    )
                )
            }
        }


        // =====================================================
        // BACK BUTTON
        // =====================================================

        onBackPressedDispatcher.addCallback(
            this,
            object :
                OnBackPressedCallback(true) {

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
    // KEYBOARD / WINDOW INSETS
    // =========================================================

    private fun toggleRecentChats() {

        if (recentSessionViews.isNotEmpty()) {
            for (v in recentSessionViews) {
                sideMenu.removeView(v)
            }
            recentSessionViews.clear()
            return
        }

        val sessions = com.nitron.bubble.chat.ChatSessionStore.getSessions()
        val recentIndex = sideMenu.indexOfChild(findViewById(R.id.recentButton))

        if (sessions.isEmpty()) {
            val emptyView = TextView(this).apply {
                text = "    No saved chats yet"
                textSize = 14f
                alpha = 0.6f
                setPadding(24, 24, 12, 24)
            }
            sideMenu.addView(emptyView, recentIndex + 1)
            recentSessionViews.add(emptyView)
            return
        }

        var insertAt = recentIndex + 1

        for (session in sessions) {

            val sessionView = TextView(this).apply {
                text = "    ${session.title}"
                textSize = 14f
                setPadding(24, 24, 12, 24)
                isClickable = true
                isFocusable = true
            }

            sessionView.setOnClickListener {
                loadSession(session.id)
            }

            sideMenu.addView(sessionView, insertAt)
            recentSessionViews.add(sessionView)
            insertAt++
        }
    }

    private fun loadSession(id: String) {

        if (firebaseAuth.currentUser != null) {
            com.nitron.bubble.chat.ChatSessionStore.archiveCurrentChat(this)
        }

        val messages = com.nitron.bubble.chat.ChatSessionStore.loadSession(this, id)

        messageAdapter.clearMessages()

        if (messages != null) {

            for (m in messages) {
                messageAdapter.addMessage(m)
            }

            welcomeText.visibility = View.GONE

        } else {

            updateWelcomeGreeting()
            welcomeText.visibility = View.VISIBLE
        }

        for (v in recentSessionViews) {
            sideMenu.removeView(v)
        }
        recentSessionViews.clear()

        drawerLayout.closeDrawers()
    }

    private fun performNewChat() {

        stopVoiceInput()
        messageInput.setText("")

        if (firebaseAuth.currentUser != null) {
            com.nitron.bubble.chat.ChatSessionStore.archiveCurrentChat(this)
        }

        messageAdapter.clearMessages()

        com.nitron.bubble.chat.ChatHistoryStore.clear()

        updateWelcomeGreeting()

        welcomeText.visibility =
            View.VISIBLE

        drawerLayout.closeDrawers()
    }

    private fun setupKeyboardInsets() {

        if (
            android.os.Build.VERSION.SDK_INT >= 30
        ) {

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
