package com.nitron.bubble

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.location.Location
import android.location.LocationManager
import androidx.core.content.ContextCompat

class LocationHelper(private val context: Context) {

    fun getLastLocation(): Location? {
        if (
            ContextCompat.checkSelfPermission(
                context,
                Manifest.permission.ACCESS_FINE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED &&
            ContextCompat.checkSelfPermission(
                context,
                Manifest.permission.ACCESS_COARSE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            return null
        }

        val manager =
            context.getSystemService(Context.LOCATION_SERVICE) as LocationManager

        val gps = manager.getLastKnownLocation(
            LocationManager.GPS_PROVIDER
        )

        val network = manager.getLastKnownLocation(
            LocationManager.NETWORK_PROVIDER
        )

        return when {
            gps != null -> gps
            network != null -> network
            else -> null
        }
    }
}
