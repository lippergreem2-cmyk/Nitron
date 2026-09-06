package com.nitron.bubble

import android.content.Context
import java.io.File
import java.util.zip.ZipEntry
import java.util.zip.ZipOutputStream

object NitronSelfTransfer {

    /**
     * Creates a portable Nitron package containing the currently
     * installed APK and basic package metadata.
     */
    fun prepareTransferPackage(context: Context): File {

        val sourceApk = File(
            context.applicationInfo.sourceDir
        )

        if (!sourceApk.exists()) {
            throw IllegalStateException(
                "Nitron's installed APK could not be found."
            )
        }

        val transferDirectory = File(
            context.cacheDir,
            "nitron_transfer"
        )

        if (!transferDirectory.exists()) {
            transferDirectory.mkdirs()
        }

        val packageFile = File(
            transferDirectory,
            "Nitron-transfer.zip"
        )

        ZipOutputStream(
            packageFile.outputStream()
        ).use { zip ->

            // APK
            zip.putNextEntry(
                ZipEntry("Nitron.apk")
            )

            sourceApk.inputStream().use { input ->
                input.copyTo(zip)
            }

            zip.closeEntry()

            // Copy metadata
            val metadata = """
                {
                  "name": "Nitron",
                  "package": "${context.packageName}",
                  "version": "${context.packageManager
                    .getPackageInfo(context.packageName, 0).versionName}",
                  "type": "Nitron portable copy",
                  "sync_protocol": 1
                }
            """.trimIndent()

            zip.putNextEntry(
                ZipEntry("nitron.json")
            )

            zip.write(
                metadata.toByteArray(Charsets.UTF_8)
            )

            zip.closeEntry()
        }

        return packageFile
    }
}
