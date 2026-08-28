package com.nitron.bubble

import android.content.ClipData
import android.content.ClipboardManager
import android.graphics.Typeface
import android.os.Bundle
import android.widget.ImageButton
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity

class FullTextActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_full_text)

        val text = intent.getStringExtra("full_text") ?: ""
        val isCode = intent.getBooleanExtra("is_code", false)

        val textView = findViewById<TextView>(R.id.fullTextView)
        textView.text = text

        if (isCode) {
            textView.typeface = Typeface.MONOSPACE
        }

        findViewById<ImageButton>(R.id.fullTextCloseButton).setOnClickListener {
            finish()
        }

        findViewById<Button>(R.id.fullTextCopyButton).setOnClickListener {
            val clipboard = getSystemService(ClipboardManager::class.java)
            clipboard.setPrimaryClip(ClipData.newPlainText("Nitron message", text))
            Toast.makeText(this, "Copied", Toast.LENGTH_SHORT).show()
        }
    }
}
