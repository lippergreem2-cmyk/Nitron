package com.nitron.bubble

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.location.Location
import android.location.LocationManager
import androidx.core.content.ContextCompat

class GpsLocator(private val context: Context) {

    fun getBestLastKnownLocation(): Location? {

        val fine =
            ContextCompat.checkSelfPermission(
                context,
                Manifest.permission.ACCESS_FINE_LOCATION
            ) == PackageManager.PERMISSION_GRANTED

        val coarse =
            ContextCompat.checkSelfPermission(
                context,
                Manifest.permission.ACCESS_COARSE_LOCATION
            ) == PackageManager.PERMISSION_GRANTED

        if (!fine && !coarse) {
            return null
        }

        val manager =
            context.getSystemService(
                Context.LOCATION_SERVICE
            ) as LocationManager

        var best: Location? = null

        for (provider in manager.getProviders(true)) {

            try {

                val location =
                    manager.getLastKnownLocation(provider)

                if (location != null) {

                    if (
                        best == null ||
                        location.accuracy < best.accuracy
                    ) {
                        best = location
                    }
                }

            } catch (_: SecurityException) {
                // Permission may have changed while querying.
            }
        }

        return best
    }
}
