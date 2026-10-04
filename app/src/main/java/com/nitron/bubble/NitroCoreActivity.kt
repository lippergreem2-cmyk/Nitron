package com.nitron.bubble

import android.app.Activity
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.graphics.Color
import android.graphics.Typeface
import android.view.Gravity
import android.widget.*
import android.content.SharedPreferences
import java.util.Locale

class NitroCoreActivity : Activity() {

    private val blue = Color.rgb(40, 150, 255)
    private val cyan = Color.CYAN
    private val darkBlue = Color.rgb(3, 12, 28)
    private val panelBlue = Color.rgb(8, 35, 70)
    private val white = Color.WHITE

    private val handler = Handler(Looper.getMainLooper())

    private var elapsedSeconds = 0
    private var running = false
    private var currentMode = ""
    private var quoteIndex = 0

    private lateinit var timerText: TextView
    private lateinit var statusText: TextView
    private lateinit var quoteText: TextView

    private val usedQuotes = mutableSetOf<String>()

    private lateinit var prefs: SharedPreferences

    private var playerLevel = 1
    private var playerXp = 0
    private var sessionsCompleted = 0
    private var streak = 0
    private var lastTrainingDay = ""

    private var questMode = ""
    private var questCompleted = false
    private var questDay = ""

    private val questModes = listOf(
        "FIGHTING",
        "BODY FITNESS",
        "SPEED",
        "REFLEX"
    )

    private fun loadQuest() {
        questMode = prefs.getString("quest_mode", "") ?: ""
        questCompleted = prefs.getBoolean("quest_completed", false)
        questDay = prefs.getString("quest_day", "") ?: ""

        val today = java.text.SimpleDateFormat(
            "yyyy-MM-dd",
            java.util.Locale.US
        ).format(java.util.Date())

        if (questDay != today) {
            questMode = questModes[
                java.util.Random().nextInt(questModes.size)
            ]
            questCompleted = false
            questDay = today

            prefs.edit()
                .putString("quest_mode", questMode)
                .putBoolean("quest_completed", false)
                .putString("quest_day", today)
                .apply()
        }
    }

    private fun dailyQuestText(): String {
        loadQuest()

        return """
            DAILY QUEST

            TARGET
            $questMode

            OBJECTIVE
            Complete one safe $questMode session.

            REWARD
            +50 XP

            STATUS
            ${if (questCompleted) "COMPLETE" else "AVAILABLE"}
        """.trimIndent()
    }

    private fun completeDailyQuest(): String {
        loadQuest()

        if (questCompleted) {
            return "SYSTEM: DAILY QUEST ALREADY COMPLETE"
        }

        questCompleted = true

        prefs.edit()
            .putBoolean("quest_completed", true)
            .apply()

        val message = addXp(50)

        return """
            QUEST COMPLETE

            DAILY MISSION CLEARED

            $message

            SYSTEM:
            Another mission has been added to your record.
        """.trimIndent()
    }

    private fun loadProgress() {
        prefs = getSharedPreferences("nitrocore_progress", MODE_PRIVATE)

        playerLevel = prefs.getInt("level", 1)
        playerXp = prefs.getInt("xp", 0)
        sessionsCompleted = prefs.getInt("sessions", 0)
        streak = prefs.getInt("streak", 0)
        lastTrainingDay = prefs.getString("last_day", "") ?: ""
    }

    private fun saveProgress() {
        prefs.edit()
            .putInt("level", playerLevel)
            .putInt("xp", playerXp)
            .putInt("sessions", sessionsCompleted)
            .putInt("streak", streak)
            .putString("last_day", lastTrainingDay)
            .apply()
    }

    private fun xpRequired(): Int {
        return playerLevel * 100
    }

    private fun addXp(amount: Int): String {
        playerXp += amount

        var levelUp = false

        while (playerXp >= xpRequired()) {
            playerXp -= xpRequired()
            playerLevel++
            levelUp = true
        }

        saveProgress()

        return if (levelUp) {
            "SYSTEM LEVEL UP\n\nLEVEL $playerLevel\n\n+${amount} XP\n\nNew level unlocked."
        } else {
            "+$amount XP"
        }
    }

    private fun completeTraining(): String {
        val today = java.text.SimpleDateFormat(
            "yyyy-MM-dd",
            java.util.Locale.US
        ).format(java.util.Date())

        sessionsCompleted++

        if (lastTrainingDay != today) {
            streak++
            lastTrainingDay = today
        }

        val reward = when (currentMode) {
            "FIGHTING" -> 35
            "BODY FITNESS" -> 40
            "SPEED" -> 35
            "REFLEX" -> 35
            else -> 25
        }

        val xpMessage = addXp(reward)

        saveProgress()

        return "SESSION COMPLETE\n\n$xpMessage\n\n" +
                "Sessions: $sessionsCompleted\n" +
                "Streak: $streak"
    }

    private fun progressText(): String {
        return """
            SYSTEM STATUS

            LEVEL $playerLevel

            XP $playerXp / ${xpRequired()}

            SESSIONS $sessionsCompleted

            STREAK $streak
        """.trimIndent()
    }

    private val quotes = listOf(
        "Growth begins when comfort ends.",
        "The next level is built one session at a time.",
        "Do not chase speed before you control the movement.",
        "A failed attempt is data. Use it.",
        "Your progress does not disappear because today was difficult.",
        "Control first. Power later.",
        "One clean repetition is worth more than ten careless ones.",
        "A hunter learns from every mission.",
        "Every quest completed changes the player.",
        "You do not need to be perfect. You need to keep learning.",
        "When the path becomes difficult, return to the basics.",
        "Discipline is built through small decisions.",
        "The System rewards consistency.",
        "Your current level is not your final level.",
        "Slow progress is still progress.",
        "Rest is part of becoming stronger.",
        "Technique is your foundation.",
        "Focus on the movement in front of you.",
        "One step. One breath. One repetition.",
        "The difficult moment will pass.",
        "Do not measure yourself against another player.",
        "Your only mission is to improve safely.",
        "A stronger version of you is built gradually.",
        "Adapt. Recover. Return.",
        "The final minute is still only one minute.",
        "If the exercise feels too difficult, reduce the intensity.",
        "Stopping because you are unwell is not failure.",
        "Listen to your body. Train with intelligence.",
        "Every session teaches something.",
        "The System records effort, not perfection.",
        "A mistake is an instruction waiting to be understood.",
        "Precision creates confidence.",
        "Your foundation determines your future.",
        "Patience is a training skill.",
        "Consistency defeats inconsistency.",
        "Focus beats distraction.",
        "The quest is simple: improve one thing today.",
        "You are allowed to reset and try again.",
        "A new attempt is a new opportunity to learn.",
        "Progress has many forms.",
        "Strong habits create strong results.",
        "The journey is measured in sessions, not seconds.",
        "Your level rises when your habits improve.",
        "Master the basics before seeking difficulty.",
        "A calm mind moves better.",
        "Reaction begins with attention.",
        "Speed without control is wasted movement.",
        "Balance creates better movement.",
        "Recovery prepares the next quest.",
        "Complete today's mission. Tomorrow has its own.",
        "The System is not asking for perfection.",
        "Keep your movements controlled.",
        "Breathe. Reset. Continue if you feel well.",
        "Your effort today becomes experience tomorrow.",
        "Every completed repetition is information.",
        "Training is adaptation, not punishment.",
        "The strongest strategy is sustainable progress.",
        "You can lower the difficulty and still complete the quest.",
        "The next attempt can be better than the last.",
        "Stay focused on your own progression.",
        "One session cannot define your journey.",
        "The System has detected progress.",
        "Quest objective: controlled movement.",
        "Quest objective: consistent effort.",
        "Quest objective: safe progression.",
        "Quest objective: finish with good technique.",
        "Leveling up starts with showing up.",
        "Your journey continues after this session.",
        "Recover like a strategist.",
        "Train like a learner.",
        "Move like every repetition has a purpose.",
        "Focus is a skill. Practice it.",
        "Reaction improves through repeated practice.",
        "Coordination grows through controlled repetition.",
        "Strength grows through patient training.",
        "Speed grows when technique becomes efficient.",
        "The System recognizes another completed mission.",
        "Another session added to your journey.",
        "The difficult part is temporary. Your learning remains.",
        "Do not rush the process.",
        "Build the foundation first.",
        "Today is another page in your training story.",
        "Your next level starts with today's choices.",
        "Adaptation takes time.",
        "Consistency gives progress somewhere to grow.",
        "The mission is progress, not perfection.",
        "Reset your posture. Reset your focus.",
        "Quality before quantity.",
        "Control the movement.",
        "Keep the rhythm steady.",
        "Use the easiest safe version when necessary.",
        "You can pause and recover.",
        "The System does not punish recovery.",
        "A smart player knows when to reduce intensity.",
        "Train today so tomorrow can be better.",
        "Your progress belongs to you.",
        "Every safe session is a successful lesson.",
        "The next quest awaits.",
        "SYSTEM: Potential detected.",
        "SYSTEM: Training adaptation detected.",
        "SYSTEM: Focus level rising.",
        "SYSTEM: Movement control improving.",
        "SYSTEM: Coordination practice registered.",
        "SYSTEM: Session progress confirmed.",
        "SYSTEM: Quest momentum maintained.",
        "SYSTEM: Another step toward the next level.",
        "SYSTEM: Continue with control.",
        "SYSTEM: Recover when necessary.",
        "SYSTEM: Mission progress is still active.",
        "SYSTEM: Your training history is growing.",
        "SYSTEM: Consistency bonus approaching.",
        "SYSTEM: Keep building your foundation.",
        "SYSTEM: No shortcut detected. Progress is being earned.",
        "SYSTEM: Training knowledge acquired.",
        "SYSTEM: Experience gained through repetition.",
        "SYSTEM: Adaptation requires patience.",
        "SYSTEM: New attempt available.",
        "SYSTEM: Progress does not require perfection."
    )

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        showTerms()
    }

    private fun showTerms() {
        val root = baseLayout()

        addTitle(root, "NITROCORE", "TRAINING SYSTEM")

        val terms = text(
            """
            Before starting NitroCore:

            • Train at a safe pace.
            • Stop if you feel pain, dizziness, or unwell.
            • Use a safe training area.
            • Fighting mode is non-contact conditioning.
            • Rest and recovery are part of training.
            • Camera tracking requires permission.
            • NitroCore is not a replacement for professional coaching.

            You can end a session at any time.
            """.trimIndent(),
            16f,
            white
        )

        val accept = button("ACCEPT & CONTINUE", blue)

        accept.setOnClickListener {
            showDashboard()
        }

        root.addView(terms)
        root.addView(accept)

        setContentView(root)
    }

    private fun showDashboard() {
        val root = baseLayout()

        addTitle(root, "NITRON // CORE", "TRAINING SYSTEM")

        addMode(root, "FIGHTING", "Non-contact conditioning") {
            startTraining("FIGHTING")
        }

        addMode(root, "BODY FITNESS", "Strength and mobility") {
            startTraining("BODY FITNESS")
        }

        addMode(root, "SPEED", "Movement and coordination") {
            startTraining("SPEED")
        }

        addMode(root, "REFLEX", "Reaction and coordination") {
            startTraining("REFLEX")
        }

        val questButton = button(
            "DAILY QUEST",
            panelBlue
        )

        questButton.setOnClickListener {
            showQuest()
        }

        root.addView(questButton)

        val system = text(
            "\n" + progressText(),
            20f,
            white
        )

        system.gravity = Gravity.CENTER
        root.addView(system)

        setContentView(root)
    }

    private fun showQuest() {
        val root = baseLayout()

        addTitle(root, "NITROCORE", "DAILY QUEST")

        val quest = text(
            dailyQuestText(),
            20f,
            white
        )

        quest.gravity = Gravity.CENTER

        val complete = button(
            "CLAIM QUEST XP",
            blue
        )

        complete.isEnabled = !questCompleted

        complete.setOnClickListener {
            val result = completeDailyQuest()

            Toast.makeText(
                this,
                result,
                Toast.LENGTH_LONG
            ).show()

            showQuest()
        }

        val back = button(
            "BACK",
            panelBlue
        )

        back.setOnClickListener {
            showDashboard()
        }

        root.addView(quest)
        root.addView(complete)
        root.addView(back)

        setContentView(root)
    }

    private fun startTraining(mode: String) {
        stopTimer()

        currentMode = mode
        elapsedSeconds = 0
        quoteIndex = 0
        usedQuotes.clear()

        val root = baseLayout()

        addTitle(root, "NITROCORE", mode)

        timerText = text("00:00", 52f, white)
        timerText.gravity = Gravity.CENTER

        statusText = text(
            "READY",
            18f,
            cyan
        )
        statusText.gravity = Gravity.CENTER

        quoteText = text(
            nextQuote(),
            18f,
            white
        )
        quoteText.gravity = Gravity.CENTER

        val start = button("START SESSION", blue)
        val pause = button("PAUSE", panelBlue)
        val motivation = button("SYSTEM ADVICE", panelBlue)
        val end = button("END SESSION", Color.DKGRAY)

        start.setOnClickListener {
            running = true
            start.isEnabled = false
            statusText.text = "SESSION ACTIVE"
            startTimer()
        }

        pause.setOnClickListener {
            if (running) {
                running = false
                statusText.text = "PAUSED — RECOVER"
            } else {
                running = true
                statusText.text = "SESSION ACTIVE"
                startTimer()
            }
        }

        motivation.setOnClickListener {
            quoteText.text = nextQuote()
        }

        // Early-session System message.
        quoteText.text = "SYSTEM ADVICE\n\n" +
                "Mission accepted. Begin with controlled movement."

        end.setOnClickListener {
            stopTimer()

            if (elapsedSeconds > 0) {
                val result = completeTraining()

                Toast.makeText(
                    this,
                    result,
                    Toast.LENGTH_LONG
                ).show()
            }

            showDashboard()
        }

        root.addView(timerText)
        root.addView(statusText)
        root.addView(quoteText)
        root.addView(start)
        root.addView(pause)
        root.addView(motivation)
        root.addView(end)

        setContentView(root)
    }

    private fun startTimer() {
        handler.postDelayed(timerRunnable, 1000)
    }

    private val timerRunnable = object : Runnable {
        override fun run() {
            if (!running) return

            elapsedSeconds++

            val minutes = elapsedSeconds / 60
            val seconds = elapsedSeconds % 60

            timerText.text = String.format(
                Locale.US,
                "%02d:%02d",
                minutes,
                seconds
            )

            // Change advice periodically without repeating.
            if (elapsedSeconds % 30 == 0) {
                quoteText.text = nextQuote()
            }

            if (elapsedSeconds == 60) {
                quoteText.text =
                    "SYSTEM ADVICE\n\n" +
                    "One minute completed. Keep the movement controlled."
            }

            if (elapsedSeconds == 120) {
                quoteText.text =
                    "SYSTEM ADVICE\n\n" +
                    "If fatigue is rising, reduce intensity and recover."
            }

            handler.postDelayed(this, 1000)
        }
    }

    private fun stopTimer() {
        running = false
        handler.removeCallbacks(timerRunnable)
    }

    private fun nextQuote(): String {
        if (usedQuotes.size >= quotes.size) {
            usedQuotes.clear()
        }

        var quote: String

        do {
            quote = quotes[quoteIndex % quotes.size]
            quoteIndex++
        } while (usedQuotes.contains(quote))

        usedQuotes.add(quote)

        return "SYSTEM ADVICE\n\n$quote"
    }

    private fun addMode(
        root: LinearLayout,
        title: String,
        description: String,
        action: () -> Unit
    ) {
        val button = button(
            "$title\n$description",
            panelBlue
        )

        button.textSize = 17f
        button.setOnClickListener {
            action()
        }

        root.addView(button)
    }

    private fun addTitle(
        root: LinearLayout,
        title: String,
        subtitle: String
    ) {
        val titleView = text(title, 30f, blue)
        titleView.setTypeface(null, Typeface.BOLD)
        titleView.gravity = Gravity.CENTER

        val subtitleView = text(subtitle, 15f, cyan)
        subtitleView.gravity = Gravity.CENTER

        root.addView(titleView)
        root.addView(subtitleView)
    }

    private fun button(
        label: String,
        background: Int
    ): Button {
        val b = Button(this)

        b.text = label
        b.setTextColor(white)
        b.setBackgroundColor(background)
        b.setPadding(20, 20, 20, 20)

        val params = LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.MATCH_PARENT,
            LinearLayout.LayoutParams.WRAP_CONTENT
        )

        params.setMargins(0, 8, 0, 8)

        b.layoutParams = params

        return b
    }

    private fun baseLayout(): LinearLayout {
        val root = LinearLayout(this)

        root.orientation = LinearLayout.VERTICAL
        root.gravity = Gravity.CENTER_HORIZONTAL
        root.setPadding(28, 40, 28, 28)
        root.setBackgroundColor(darkBlue)

        return root
    }

    private fun text(
        value: String,
        size: Float,
        color: Int
    ): TextView {
        val view = TextView(this)

        view.text = value
        view.textSize = size
        view.setTextColor(color)
        view.setPadding(0, 10, 0, 10)

        return view
    }

    override fun onDestroy() {
        stopTimer()
        super.onDestroy()
    }
}
