package com.nitron.bubble

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.hardware.usb.UsbManager
import android.os.Build
import androidx.core.content.ContextCompat

object DeviceTransferManager {

    enum class DeviceType {
        BLUETOOTH,
        USB
    }

    data class TransferDevice(
        val name: String,
        val type: DeviceType,
        val address: String? = null,
        val id: String = ""
    )

    /**
     * Returns paired Bluetooth devices that Nitron can access.
     *
     * Android 12+ requires BLUETOOTH_CONNECT at runtime.
     */
    fun getPairedBluetoothDevices(
        context: Context
    ): List<TransferDevice> {

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            if (
                ContextCompat.checkSelfPermission(
                    context,
                    Manifest.permission.BLUETOOTH_CONNECT
                ) != PackageManager.PERMISSION_GRANTED
            ) {
                return emptyList()
            }
        }

        val bluetoothManager =
            context.getSystemService(Context.BLUETOOTH_SERVICE)
                as? android.bluetooth.BluetoothManager
                ?: return emptyList()

        val adapter = bluetoothManager.adapter
            ?: return emptyList()

        return try {
            adapter.bondedDevices
                .map { device ->
                    TransferDevice(
                        name = device.name ?: "Bluetooth device",
                        type = DeviceType.BLUETOOTH,
                        address = device.address,
                        id = "bluetooth:${device.address}"
                    )
                }
                .sortedBy { it.name.lowercase() }
        } catch (_: SecurityException) {
            emptyList()
        }
    }

    /**
     * Returns USB devices currently attached to the Android phone.
     *
     * Note:
     * A normal PC connected by USB usually acts as the USB host,
     * so it will not necessarily appear here. Android's normal
     * phone-to-PC cable transfer is handled by the system's MTP
     * connection rather than UsbManager.
     */
    fun getAttachedUsbDevices(
        context: Context
    ): List<TransferDevice> {

        val usbManager =
            context.getSystemService(Context.USB_SERVICE)
                as? UsbManager
                ?: return emptyList()

        return usbManager.deviceList.values
            .map { device ->
                val product =
                    device.productName?.takeIf { it.isNotBlank() }

                val manufacturer =
                    device.manufacturerName?.takeIf { it.isNotBlank() }

                val displayName = when {
                    product != null && manufacturer != null ->
                        "$manufacturer $product"

                    product != null ->
                        product

                    manufacturer != null ->
                        manufacturer

                    else ->
                        "USB device"
                }

                TransferDevice(
                    name = displayName,
                    type = DeviceType.USB,
                    address = device.deviceName,
                    id = "usb:${device.deviceId}"
                )
            }
            .sortedBy { it.name.lowercase() }
    }

    /**
     * Returns all devices Nitron can currently discover.
     */
    fun getAvailableDevices(
        context: Context
    ): List<TransferDevice> {

        val devices = mutableListOf<TransferDevice>()

        devices += getPairedBluetoothDevices(context)
        devices += getAttachedUsbDevices(context)

        return devices
    }
}
