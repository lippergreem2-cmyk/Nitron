package com.nitron.bubble

import android.app.Activity
import android.os.Bundle
import android.graphics.Color
import android.graphics.Typeface
import android.view.Gravity
import android.view.View
import android.widget.Button
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import android.content.Intent

class LegalActivity : Activity() {

    private val pink = Color.rgb(255, 45, 120)
    private val dark = Color.rgb(10, 10, 14)

    private val termsText = """
NITRON — TERMS AND CONDITIONS

Effective Date: 26 September 2026

Welcome to Nitron. These Terms and Conditions govern your use of the Nitron application and its related services.

By using Nitron, you agree to these Terms. If you do not agree, do not use the application.

1. ABOUT NITRON

Nitron is an AI-powered personal assistant and utility application. Features may include AI conversations, voice interaction, education, search, media features, device-related functions, floating assistant features, and other services added over time.

Features may vary depending on your device and version of Nitron.

2. ACCEPTABLE USE

You agree to use Nitron lawfully and responsibly.

You must not use Nitron to:
• Break applicable laws or regulations.
• Harm, threaten, or harass another person.
• Obtain unauthorized access to systems, accounts, or devices.
• Distribute malicious software or harmful code.
• Circumvent security or safety protections.
• Misuse another person's personal information.
• Use Nitron in a way that could reasonably cause harm.

3. AI-GENERATED INFORMATION

Nitron may use artificial intelligence to generate responses, suggestions, explanations, code, and other content.

AI-generated information can contain errors or outdated information. Important information should be independently verified before being relied upon.

Nitron does not replace qualified professional advice where professional advice is required.

4. VOICE AND DEVICE PERMISSIONS

Certain features may require permissions such as microphone, camera, notification, Bluetooth, location, overlay, or Internet access.

You control Android permissions through your device settings.

5. ACCOUNTS

Some Nitron features may require an account.

You are responsible for protecting your account credentials and for activity performed through your account.

6. PERSONAL DATA

Nitron may process information necessary to provide its features, including information you provide, account information, preferences, and technical information.

Personal data is handled according to applicable privacy and data-protection laws.

Additional information is provided in the Nitron Privacy Policy.

7. CHILDREN

Where applicable law requires parental or guardian involvement or consent for processing a child's personal data, Nitron will follow those requirements.

8. THIRD-PARTY SERVICES

Nitron may use third-party services for authentication, AI processing, hosting, media, or other functionality.

Third-party services may have their own terms and privacy policies.

9. INTELLECTUAL PROPERTY

Nitron software, branding, design, logos, and original materials belong to Nitron or their respective licensors unless otherwise stated.

You may not copy, modify, distribute, or commercially exploit Nitron except where permitted by law or with permission.

10. AVAILABILITY

We aim to keep Nitron available and reliable, but we do not guarantee uninterrupted availability, perfect accuracy, compatibility with every device, or continued availability of every feature.

Features may be updated, changed, suspended, or discontinued.

11. SECURITY

Reasonable measures may be used to protect Nitron and information processed through the service. However, no Internet-connected system can be guaranteed to be completely secure.

12. LIMITATION OF LIABILITY

To the extent permitted by applicable law, Nitron and its developers are not responsible for indirect, incidental, or consequential losses arising from use of the application.

Nothing in these Terms limits liability where such limitation is prohibited by law.

13. CHANGES

These Terms may be updated when Nitron's services, features, or legal requirements change.

Important changes may be communicated through the application or another reasonable method.

14. TERMINATION

You may stop using Nitron at any time.

Access to features may be suspended or terminated when reasonably necessary, including for misuse, security concerns, or legal requirements.

15. GOVERNING LAW

Where applicable, the laws of Kenya will govern these Terms, subject to mandatory legal rights and protections applicable to you.

16. CONTACT

For questions about these Terms or Nitron, use the official contact method provided within the application.

By selecting "I Agree", you acknowledge that you have read and understood these Terms and agree to them.
""".trimIndent()

    private val privacyText = """
NITRON — PRIVACY POLICY

Effective Date: 26 September 2026

This Privacy Policy explains how Nitron may handle information when you use the application.

1. INFORMATION THAT MAY BE PROCESSED

Depending on the features you use, Nitron may process:

• Account and authentication information.
• Information you provide during conversations.
• Preferences and application settings.
• Voice input when you use voice features.
• Images or files when you deliberately use related features.
• Technical information needed for the application to operate.
• Information required by connected services.

2. HOW INFORMATION MAY BE USED

Information may be used to:

• Provide Nitron's requested features.
• Authenticate users.
• Process AI requests.
• Maintain conversations and application functionality.
• Improve reliability and security.
• Respond to support requests.
• Comply with applicable legal requirements.

3. DEVICE PERMISSIONS

Nitron may request Android permissions when a feature requires them.

Examples include microphone, camera, Bluetooth, location, notifications, Internet access, and overlay permissions.

You can review or change permissions through Android Settings.

4. AI SERVICES

Some Nitron requests may be processed by AI services or other technical services required by the application.

Information sent to such services depends on the feature being used and the application's configuration.

5. THIRD-PARTY SERVICES

Nitron may use services such as authentication, hosting, AI, analytics, or other infrastructure providers.

Those providers may process information according to their own policies and applicable agreements.

6. DATA SECURITY

Reasonable safeguards may be used to protect information.

No electronic system can guarantee absolute security.

7. YOUR RIGHTS

Depending on applicable law, you may have rights concerning your personal information, including rights relating to access, correction, objection, restriction, or deletion.

Under applicable Kenyan data-protection law, these rights may be subject to legal limitations and conditions.

8. CHILDREN

Where applicable law requires parental or guardian consent or additional protections for children's personal data, Nitron will follow those requirements.

9. POLICY CHANGES

This Privacy Policy may be updated as Nitron changes.

Important changes may be communicated through the application.

10. CONTACT

For privacy questions or requests concerning personal information, use the official contact method provided within Nitron.

This Privacy Policy should be read together with the Nitron Terms and Conditions.
""".trimIndent()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val required = intent.getBooleanExtra("required", false)

        showDocument(
            title = "Nitron Terms & Privacy",
            required = required
        )
    }

    private fun showDocument(title: String, required: Boolean) {

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundColor(dark)
            setPadding(32, 40, 32, 32)
        }

        val titleView = TextView(this).apply {
            text = title
            textSize = 26f
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
            gravity = Gravity.CENTER
        }

        root.addView(
            titleView,
            LinearLayout.LayoutParams(
                -1,
                LinearLayout.LayoutParams.WRAP_CONTENT
            )
        )

        val tabs = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER
        }

        val termsButton = Button(this).apply {
            text = "Terms"
            setTextColor(Color.WHITE)
            setOnClickListener {
                document.text = termsText
            }
        }

        val privacyButton = Button(this).apply {
            text = "Privacy"
            setTextColor(Color.WHITE)
            setOnClickListener {
                document.text = privacyText
            }
        }

        tabs.addView(
            termsButton,
            LinearLayout.LayoutParams(0, 60, 1f)
        )

        tabs.addView(
            privacyButton,
            LinearLayout.LayoutParams(0, 60, 1f)
        )

        root.addView(tabs)

        val scroll = ScrollView(this)

        document = TextView(this).apply {
            text = termsText
            textSize = 15f
            setTextColor(Color.LTGRAY)
            setPadding(12, 24, 12, 24)
            setLineSpacing(0f, 1.15f)
        }

        scroll.addView(document)

        root.addView(
            scroll,
            LinearLayout.LayoutParams(
                -1,
                0,
                1f
            )
        )

        val agreeButton = Button(this).apply {
            text = if (required) {
                "I Agree & Continue"
            } else {
                "Done"
            }

            setTextColor(Color.WHITE)
            setBackgroundColor(pink)

            setOnClickListener {

                if (required) {
                    getSharedPreferences(
                        "nitron_legal",
                        MODE_PRIVATE
                    )
                        .edit()
                        .putBoolean("terms_accepted", true)
                        .apply()
                }

                finish()
            }
        }

        root.addView(
            agreeButton,
            LinearLayout.LayoutParams(
                -1,
                64
            )
        )

        setContentView(root)
    }

    private lateinit var document: TextView

    override fun onBackPressed() {
        val required = intent.getBooleanExtra("required", false)

        if (required) {
            finishAffinity()
        } else {
            super.onBackPressed()
        }
    }
}
