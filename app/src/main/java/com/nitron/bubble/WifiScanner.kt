package com.nitron.bubble

import android.Manifest
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import android.net.wifi.ScanResult
import android.net.wifi.WifiManager
import androidx.core.content.ContextCompat

object WifiScanner {

    fun scan(
        context: Context,
        callback: (String) -> Unit
    ) {
        if (
            ContextCompat.checkSelfPermission(
                context,
                Manifest.permission.ACCESS_FINE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            callback(
                "=== Nitron Wi-Fi Scan ===\n\n" +
                "Location permission is required to scan nearby Wi-Fi networks."
            )
            return
        }

        val appContext = context.applicationContext

        val wifiManager =
            appContext.getSystemService(Context.WIFI_SERVICE) as WifiManager

        val receiver = object : BroadcastReceiver() {

            override fun onReceive(
                receiverContext: Context?,
                intent: Intent?
            ) {
                try {
                    appContext.unregisterReceiver(this)
                } catch (_: Exception) {
                }

                try {
                    if (
                        intent?.action !=
                        WifiManager.SCAN_RESULTS_AVAILABLE_ACTION
                    ) {
                        callback(
                            "=== Nitron Wi-Fi Scan ===\n\n" +
                            "Wi-Fi scan did not return valid results."
                        )
                        return
                    }

                    val results = wifiManager.scanResults

                    callback(format(results))

                } catch (e: SecurityException) {

                    callback(
                        "=== Nitron Wi-Fi Scan ===\n\n" +
                        "Android denied Wi-Fi scan access."
                    )

                } catch (e: Exception) {

                    callback(
                        "=== Nitron Wi-Fi Scan ===\n\n" +
                        "Wi-Fi scan failed: ${e.message}"
                    )
                }
            }
        }

        try {
            ContextCompat.registerReceiver(
                appContext,
                receiver,
                IntentFilter(
                    WifiManager.SCAN_RESULTS_AVAILABLE_ACTION
                ),
                ContextCompat.RECEIVER_NOT_EXPORTED
            )

            val started = wifiManager.startScan()

            if (!started) {
                try {
                    appContext.unregisterReceiver(receiver)
                } catch (_: Exception) {
                }

                callback(
                    "=== Nitron Wi-Fi Scan ===\n\n" +
                    "Android could not start the Wi-Fi scan. Try again."
                )
            }

        } catch (e: SecurityException) {

            try {
                appContext.unregisterReceiver(receiver)
            } catch (_: Exception) {
            }

            callback(
                "=== Nitron Wi-Fi Scan ===\n\n" +
                "Android denied Wi-Fi scan access."
            )

        } catch (e: Exception) {

            try {
                appContext.unregisterReceiver(receiver)
            } catch (_: Exception) {
            }

            callback(
                "=== Nitron Wi-Fi Scan ===\n\n" +
                "Wi-Fi scan failed: ${e.message}"
            )
        }
    }

    private fun format(results: List<ScanResult>): String {

        if (results.isEmpty()) {
            return (
                "=== Nitron Wi-Fi Scan ===\n\n" +
                "No nearby Wi-Fi networks were returned."
            )
        }

        val output = StringBuilder()

        output.append("=== Nitron Wi-Fi Scan ===\n")
        output.append("Networks found: ${results.size}\n\n")

        for (network in results.sortedByDescending { it.level }) {

            val ssid =
                network.SSID.ifBlank { "<hidden>" }

            val bssid =
                network.BSSID.ifBlank { "unavailable" }

            output.append("SSID: $ssid\n")
            output.append("BSSID: $bssid\n")
            output.append("Signal: ${network.level} dBm\n")
            output.append("Frequency: ${network.frequency} MHz\n")
            output.append(
                "Channel: ${frequencyToChannel(network.frequency)}\n"
            )
            output.append(
                "Security: ${network.capabilities}\n\n"
            )
        }

        return output.toString().trim()
    }

    private fun frequencyToChannel(
        frequency: Int
    ): String {

        return when {

            frequency in 2412..2472 ->
                ((frequency - 2407) / 5).toString()

            frequency == 2484 ->
                "14"

            frequency in 5000..5900 ->
                ((frequency - 5000) / 5).toString()

            frequency in 5925..7125 ->
                "6 GHz"

            else ->
                "unknown"
        }
    }
}
