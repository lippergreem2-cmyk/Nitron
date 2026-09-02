package com.nitron.bubble

import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.app.AppCompatDelegate
import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.location.Geocoder
import android.net.Uri
import android.provider.Settings as AndroidSettings
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AlertDialog
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.nitron.bubble.BubbleService
import com.nitron.bubble.GpsLocator
import java.util.Locale

class SettingsActivity : AppCompatActivity() {

    private val locationPermission =
        registerForActivityResult(
            ActivityResultContracts.RequestMultiplePermissions()
        ) { permissions ->

            val fine = permissions[Manifest.permission.ACCESS_FINE_LOCATION] == true
            val coarse = permissions[Manifest.permission.ACCESS_COARSE_LOCATION] == true

            if (fine || coarse) {
                showMyLocation()
            } else {
                AlertDialog.Builder(this)
                    .setTitle("Location permission")
                    .setMessage("Nitron needs location permission to locate this device.")
                    .setPositiveButton("OK", null)
                    .show()
            }
        }

    private fun requestLocation() {

        val fineGranted = ContextCompat.checkSelfPermission(
            this, Manifest.permission.ACCESS_FINE_LOCATION
        ) == PackageManager.PERMISSION_GRANTED

        val coarseGranted = ContextCompat.checkSelfPermission(
            this, Manifest.permission.ACCESS_COARSE_LOCATION
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

        val locator = GpsLocator(this)
        val location = locator.getBestLastKnownLocation()

        if (location == null) {
            AlertDialog.Builder(this)
                .setTitle("Location unavailable")
                .setMessage("Nitron could not find a recent device location. Make sure Location is turned on and try again.")
                .setPositiveButton("OK", null)
                .show()
            return
        }

        val latitude = location.latitude
        val longitude = location.longitude
        val accuracy = location.accuracy

        var country = "Unknown"
        var region = "Unknown"
        var county = "Unknown"
        var city = "Unknown"
        var place = "Unknown"

        try {
            if (Geocoder.isPresent()) {
                @Suppress("DEPRECATION")
                val geocoder = Geocoder(this, Locale.getDefault())
                @Suppress("DEPRECATION")
                val addresses = geocoder.getFromLocation(latitude, longitude, 1)
                if (!addresses.isNullOrEmpty()) {
                    val address = addresses[0]
                    country = address.countryName ?: "Unknown"
                    region = address.adminArea ?: "Unknown"
                    county = address.subAdminArea ?: address.adminArea ?: "Unknown"
                    city = address.locality ?: address.subAdminArea ?: address.adminArea ?: "Unknown"
                    place = address.getAddressLine(0) ?: "Unknown"
                }
            }
        } catch (_: Exception) {
        }

        val result = """
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

        findViewById<TextView>(R.id.myLocationSetting).setOnClickListener {
            requestLocation()
        }

        findViewById<TextView>(R.id.startBubbleSetting).setOnClickListener {
            if (!AndroidSettings.canDrawOverlays(this)) {
                startActivity(
                    Intent(
                        AndroidSettings.ACTION_MANAGE_OVERLAY_PERMISSION,
                        Uri.parse("package:$packageName")
                    )
                )
            } else {
                startService(Intent(this, BubbleService::class.java))
            }
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
