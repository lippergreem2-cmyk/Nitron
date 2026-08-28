package com.nitron.bubble

import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.app.AppCompatDelegate

class SettingsActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {

        super.onCreate(savedInstanceState)
        applySavedTheme()
        setContentView(R.layout.settings)

        findViewById<TextView>(R.id.settingsBack).setOnClickListener {
            finish()
        }

        findViewById<TextView>(R.id.systemMode).setOnClickListener {
            setThemeMode("system")
        }

        findViewById<TextView>(R.id.lightMode).setOnClickListener {
            setThemeMode("light")
        }

        findViewById<TextView>(R.id.darkMode).setOnClickListener {
            setThemeMode("dark")
        }
    }

    private fun applySavedTheme() {

        val mode = getSharedPreferences(
            "nitron_settings",
            MODE_PRIVATE
        ).getString("theme", "system")

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

    private fun setThemeMode(mode: String) {

        getSharedPreferences(
            "nitron_settings",
            MODE_PRIVATE
        )
            .edit()
            .putString("theme", mode)
            .apply()

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
}
