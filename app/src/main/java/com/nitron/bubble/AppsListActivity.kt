package com.nitron.bubble

import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.provider.Settings
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.RecyclerView

class AppsListActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.apps_list)

        val isHomeLaunch = intent?.categories?.contains(Intent.CATEGORY_HOME) == true

        val backButton = findViewById<android.widget.TextView>(R.id.appsBack)
        if (isHomeLaunch) {
            backButton.visibility = android.view.View.GONE
        } else {
            backButton.setOnClickListener { finish() }
        }

        val recyclerView = findViewById<RecyclerView>(R.id.appsRecyclerView)
        recyclerView.layoutManager = GridLayoutManager(this, 4)

        val pm = packageManager
        val installedApps = pm.getInstalledApplications(PackageManager.GET_META_DATA)
            .filter { app ->
                pm.getLaunchIntentForPackage(app.packageName) != null
            }
            .sortedBy { it.loadLabel(pm).toString().lowercase() }

        recyclerView.adapter = AppListAdapter(installedApps, pm) { app ->
            val launchIntent = pm.getLaunchIntentForPackage(app.packageName)
            if (launchIntent != null) {
                startActivity(launchIntent)
            }
        }

        // Make sure the floating Nitron bubble is showing on top of this screen
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.M || Settings.canDrawOverlays(this)) {
            if (!BubbleService.isRunning) {
                startService(Intent(this, BubbleService::class.java))
            }
        }
    }
}
