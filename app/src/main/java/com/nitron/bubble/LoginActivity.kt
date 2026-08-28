package com.nitron.bubble

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class LoginActivity : AppCompatActivity() {

    private val prefsName = "nitron_account"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContentView(R.layout.activity_login)

        val googleButton = findViewById<Button>(R.id.googleLoginButton)
        val appleButton = findViewById<Button>(R.id.appleLoginButton)
        val status = findViewById<TextView>(R.id.loginStatus)

        googleButton.setOnClickListener {
            status.text = "Google sign-in will be connected next."
        }

        appleButton.setOnClickListener {
            status.text = "Apple sign-in will be connected next."
        }
    }
}
