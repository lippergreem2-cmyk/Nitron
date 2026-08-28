package com.nitron.bubble

import android.Manifest
import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.location.Address
import android.location.Geocoder
import android.location.Location
import android.location.LocationListener
import android.location.LocationManager
import android.net.Uri
import android.os.Bundle
import android.provider.Settings
import android.view.Gravity
import android.widget.Button
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import androidx.core.app.ActivityCompat
import java.util.Locale
import java.util.concurrent.Executors

class LocationTestActivity : Activity() {

    companion object {
        private const val LOCATION_REQUEST = 1001
        private const val LOCATION_UPDATE = 1002
    }

    private lateinit var result: TextView
    private lateinit var mapButton: Button

    private var currentLocation: Location? = null
    private var locationManager: LocationManager? = null

    private val executor = Executors.newSingleThreadExecutor()

    private val locationListener = object : LocationListener {

        override fun onLocationChanged(location: Location) {
            currentLocation = location

            locationManager?.removeUpdates(this)

            showLocation(location)
        }

        override fun onProviderEnabled(provider: String) {}

        override fun onProviderDisabled(provider: String) {}

        @Deprecated("Deprecated in Android API")
        override fun onStatusChanged(
            provider: String?,
            status: Int,
            extras: Bundle?
        ) {}
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        buildInterface()

        requestLocation()
    }

    private fun buildInterface() {

        result = TextView(this).apply {
            text = """
                📍 NITRON LOCATION

                Getting your device location...
            """.trimIndent()

            textSize = 17f
            setPadding(30, 30, 30, 30)
        }

        mapButton = Button(this).apply {
            text = "🗺️ OPEN EXACT LOCATION"
            isEnabled = false

            setOnClickListener {
                openMap()
            }
        }

        val refreshButton = Button(this).apply {
            text = "🔄 REFRESH LOCATION"

            setOnClickListener {
                requestLocation()
            }
        }

        val backButton = Button(this).apply {
            text = "← BACK"

            setOnClickListener {
                finish()
            }
        }

        val layout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER_HORIZONTAL
            setPadding(20, 30, 20, 30)

            addView(
                result,
                LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.MATCH_PARENT,
                    LinearLayout.LayoutParams.WRAP_CONTENT
                )
            )

            addView(
                mapButton,
                LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.MATCH_PARENT,
                    LinearLayout.LayoutParams.WRAP_CONTENT
                )
            )

            addView(
                refreshButton,
                LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.MATCH_PARENT,
                    LinearLayout.LayoutParams.WRAP_CONTENT
                )
            )

            addView(
                backButton,
                LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.MATCH_PARENT,
                    LinearLayout.LayoutParams.WRAP_CONTENT
                )
            )
        }

        val scrollView = ScrollView(this)
        scrollView.addView(layout)

        setContentView(scrollView)
    }

    private fun requestLocation() {

        if (
            ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_FINE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED &&
            ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_COARSE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED
        ) {

            ActivityCompat.requestPermissions(
                this,
                arrayOf(
                    Manifest.permission.ACCESS_FINE_LOCATION,
                    Manifest.permission.ACCESS_COARSE_LOCATION
                ),
                LOCATION_REQUEST
            )

            return
        }

        getLocation()
    }

    private fun getLocation() {

        result.text = """
            📍 NITRON LOCATION

            Acquiring GPS location...

            Please make sure Android Location
            is enabled.
        """.trimIndent()

        mapButton.isEnabled = false

        locationManager =
            getSystemService(LOCATION_SERVICE) as LocationManager

        try {

            val gpsEnabled =
                locationManager?.isProviderEnabled(
                    LocationManager.GPS_PROVIDER
                ) == true

            val networkEnabled =
                locationManager?.isProviderEnabled(
                    LocationManager.NETWORK_PROVIDER
                ) == true

            if (!gpsEnabled && !networkEnabled) {

                result.text = """
                    ❌ LOCATION IS OFF

                    Turn on Android Location and
                    press Refresh Location.
                """.trimIndent()

                return
            }

            locationManager?.removeUpdates(locationListener)

            var requested = false

            if (gpsEnabled) {

                locationManager?.requestLocationUpdates(
                    LocationManager.GPS_PROVIDER,
                    1000L,
                    1f,
                    locationListener
                )

                requested = true
            }

            if (networkEnabled) {

                locationManager?.requestLocationUpdates(
                    LocationManager.NETWORK_PROVIDER,
                    1000L,
                    1f,
                    locationListener
                )

                requested = true
            }

            if (!requested) {
                showNoLocation()
            }

        } catch (securityException: SecurityException) {

            result.text = """
                ❌ LOCATION PERMISSION ERROR

                Android did not grant Nitron
                permission to access location.
            """.trimIndent()
        }
    }

    private fun showLocation(location: Location) {

        val latitude = location.latitude
        val longitude = location.longitude
        val accuracy = location.accuracy

        result.text = """
            📍 CURRENT DEVICE LOCATION

            Latitude:
            $latitude

            Longitude:
            $longitude

            🎯 GPS Accuracy:
            ${"%.1f".format(Locale.US, accuracy)} meters

            🔎 Finding address...
        """.trimIndent()

        mapButton.isEnabled = true

        executor.execute {

            val address = reverseGeocode(
                latitude,
                longitude
            )

            runOnUiThread {

                if (isFinishing) {
                    return@runOnUiThread
                }

                showLocationResult(
                    location,
                    address
                )
            }
        }
    }

    private fun reverseGeocode(
        latitude: Double,
        longitude: Double
    ): Address? {

        return try {

            val geocoder =
                Geocoder(
                    this,
                    Locale.getDefault()
                )

            @Suppress("DEPRECATION")
            geocoder.getFromLocation(
                latitude,
                longitude,
                1
            )?.firstOrNull()

        } catch (e: Exception) {
            null
        }
    }

    private fun showLocationResult(
        location: Location,
        address: Address?
    ) {

        val latitude = location.latitude
        val longitude = location.longitude

        val country =
            address?.countryName ?: "Unavailable"

        val county =
            address?.subAdminArea
                ?: address?.adminArea
                ?: "Unavailable"

        val city =
            address?.locality
                ?: address?.subLocality
                ?: address?.subAdminArea
                ?: "Unavailable"

        val place =
            address?.getAddressLine(0)
                ?: "Address unavailable"

        result.text = """
            📍 CURRENT DEVICE LOCATION

            🌐 Latitude:
            $latitude

            🌐 Longitude:
            $longitude

            🎯 Accuracy:
            ${"%.1f".format(Locale.US, location.accuracy)} meters

            🏠 Place:
            $place

            🏙️ Town / City:
            $city

            🏛️ County / Region:
            $county

            🌍 Country:
            $country

            ℹ️ The address comes from
            reverse geocoding and may not
            exactly match a building name.
        """.trimIndent()
    }

    private fun showNoLocation() {

        result.text = """
            ❌ LOCATION UNAVAILABLE

            Nitron could not obtain a GPS
            location from this device.

            Try moving somewhere with a
            clearer GPS signal and press
            Refresh Location.
        """.trimIndent()
    }

    private fun openMap() {

        val location = currentLocation ?: return

        val latitude = location.latitude
        val longitude = location.longitude

        val geoUri =
            Uri.parse(
                "geo:$latitude,$longitude?q=$latitude,$longitude(Nitron)"
            )

        val intent = Intent(
            Intent.ACTION_VIEW,
            geoUri
        )

        try {

            startActivity(intent)

        } catch (e: Exception) {

            val webMap =
                Uri.parse(
                    "https://www.openstreetmap.org/" +
                    "?mlat=$latitude" +
                    "&mlon=$longitude" +
                    "#map=19/$latitude/$longitude"
                )

            startActivity(
                Intent(
                    Intent.ACTION_VIEW,
                    webMap
                )
            )
        }
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

        if (requestCode == LOCATION_REQUEST) {

            val granted =
                grantResults.any {
                    it == PackageManager.PERMISSION_GRANTED
                }

            if (granted) {

                getLocation()

            } else {

                result.text = """
                    ❌ LOCATION PERMISSION DENIED

                    Nitron needs location permission
                    to determine this device's GPS
                    position.

                    You can enable it in Android
                    Settings.
                """.trimIndent()
            }
        }
    }

    override fun onDestroy() {

        locationManager?.removeUpdates(
            locationListener
        )

        executor.shutdownNow()

        super.onDestroy()
    }
}
