package com.nitron.bubble
import android.app.AlertDialog

import android.app.Activity
import android.content.pm.ActivityInfo
import android.content.Intent
import android.webkit.WebView
import android.webkit.WebViewClient
import android.view.WindowManager
import androidx.media3.common.C
import androidx.media3.common.MediaItem
import androidx.media3.common.Tracks
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.exoplayer.trackselection.DefaultTrackSelector
import androidx.media3.ui.PlayerView
import android.os.Bundle
import android.graphics.Color
import android.graphics.Typeface
import android.view.Gravity
import android.view.View
import android.widget.*
import org.json.JSONArray
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import kotlin.concurrent.thread

class AnimeActivity : Activity() {

    private val bg = Color.rgb(7, 8, 12)
    private val card = Color.rgb(22, 24, 32)
    private val white = Color.WHITE
    private val gray = Color.rgb(170, 174, 185)
    private val blue = Color.rgb(45, 140, 255)

    private var animeData = JSONArray()
    private val myList = mutableListOf<JSONObject>()

    private lateinit var content: LinearLayout

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        showHome()
    }

    private fun baseScreen(): LinearLayout {
        val root = LinearLayout(this)
        root.orientation = LinearLayout.VERTICAL
        root.setBackgroundColor(bg)

        content = LinearLayout(this)
        content.orientation = LinearLayout.VERTICAL
        content.setPadding(20, 35, 20, 100)

        val scroll = ScrollView(this)
        scroll.addView(content)

        root.addView(
            scroll,
            LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                0,
                1f
            )
        )

        root.addView(createBottomBar())

        return root
    }

    private fun showHome() {
        val root = baseScreen()

        val title = TextView(this).apply {
            text = "NITROBOX"
            textSize = 30f
            typeface = Typeface.DEFAULT_BOLD
            setTextColor(white)
        }

        val subtitle = TextView(this).apply {
            text = "Anime. Discover. Watch."
            textSize = 15f
            setTextColor(gray)
            setPadding(0, 4, 0, 24)
        }

        content.addView(title)
        content.addView(subtitle)

        addFeatured()

        addSection("🔥 Trending")
        addSection("⭐ Popular")
        addSection("🆕 Recently Added")

        setContentView(root)
        loadAnime()
    }

    private fun addFeatured() {
        val hero = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.BOTTOM
            setPadding(25, 25, 25, 25)
            setBackgroundColor(Color.rgb(25, 30, 48))
        }

        val label = TextView(this).apply {
            text = "FEATURED"
            textSize = 13f
            setTextColor(blue)
            typeface = Typeface.DEFAULT_BOLD
        }

        val title = TextView(this).apply {
            text = "BLEACH"
            textSize = 32f
            setTextColor(white)
            typeface = Typeface.DEFAULT_BOLD
        }

        val description = TextView(this).apply {
            text = "Ichigo Kurosaki becomes a Soul Reaper."
            textSize = 14f
            setTextColor(gray)
        }

        val watch = Button(this).apply {
            text = "▶  WATCH NOW"
            setOnClickListener {
                openAnimeById(1)
            }
        }

        hero.addView(label)
        hero.addView(title)
        hero.addView(description)
        hero.addView(watch)

        content.addView(
            hero,
            LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                330
            ).apply {
                setMargins(0, 0, 0, 25)
            }
        )
    }

    private fun addSection(title: String) {
        val heading = TextView(this).apply {
            text = title
            textSize = 21f
            typeface = Typeface.DEFAULT_BOLD
            setTextColor(white)
            setPadding(0, 12, 0, 14)
        }

        content.addView(heading)

        val row = HorizontalScrollView(this).apply {
            isHorizontalScrollBarEnabled = false
        }

        val container = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
        }

        row.addView(container)

        content.addView(
            row,
            LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                235
            )
        )

        row.tag = container
    }

    private fun loadAnime() {
        thread {
            try {
                val connection =
                    URL(
    getSharedPreferences("nitron_server", MODE_PRIVATE)
        .getString("server_url", "http://127.0.0.1:8000")
        ?.trim()
        ?.trimEnd('/')
        .let { "$it/anime" }
)
                        .openConnection() as HttpURLConnection

                connection.requestMethod = "GET"
                connection.connectTimeout = 5000
                connection.readTimeout = 5000

                val response = connection.inputStream
                    .bufferedReader()
                    .use { it.readText() }

                connection.disconnect()

                val json = JSONObject(response)
                animeData = json.getJSONArray("anime")

                runOnUiThread {
                    populateRows()
                }

            } catch (e: Exception) {
                runOnUiThread {
                    Toast.makeText(
                        this,
                        "Nitrobox API offline",
                        Toast.LENGTH_LONG
                    ).show()
                }
            }
        }
    }

    private fun populateRows() {
        val rows = mutableListOf<LinearLayout>()

        for (i in 0 until content.childCount) {
            val view = content.getChildAt(i)

            if (view is HorizontalScrollView) {
                val container = view.tag as? LinearLayout
                if (container != null) {
                    rows.add(container)
                }
            }
        }

        for (row in rows) {
            row.removeAllViews()

            for (i in 0 until animeData.length()) {
                val item = animeData.getJSONObject(i)
                row.addView(createAnimeCard(item))
            }
        }
    }

    private fun createAnimeCard(item: JSONObject): TextView {
        return TextView(this).apply {
            text = item.getString("title")
            textSize = 17f
            gravity = Gravity.CENTER
            typeface = Typeface.DEFAULT_BOLD
            setTextColor(white)
            setBackgroundColor(card)
            setPadding(12, 12, 12, 12)

            setOnClickListener {
                openAnime(item)
            }

            layoutParams = LinearLayout.LayoutParams(
                165,
                210
            ).apply {
                setMargins(0, 0, 14, 0)
            }
        }
    }

    private fun openAnimeById(id: Int) {
        thread {
            try {
                val response =
                    URL(
    getSharedPreferences("nitron_server", MODE_PRIVATE)
        .getString("server_url", "http://127.0.0.1:8000")
        ?.trim()
        ?.trimEnd('/')
        .let { "$it/anime/$id" }
)
                        .openStream()
                        .bufferedReader()
                        .use { it.readText() }

                val item = JSONObject(response).getJSONObject("anime")

                runOnUiThread {
                    openAnime(item)
                }

            } catch (e: Exception) {
                runOnUiThread {
                    Toast.makeText(
                        this,
                        "Unable to load anime",
                        Toast.LENGTH_SHORT
                    ).show()
                }
            }
        }
    }

    private fun openAnime(item: JSONObject) {
        val root = baseScreen()

        val back = Button(this).apply {
            text = "← Back"
            setOnClickListener {
                showHome()
            }
        }

        val title = TextView(this).apply {
            text = item.getString("title")
            textSize = 30f
            typeface = Typeface.DEFAULT_BOLD
            setTextColor(white)
            setPadding(0, 20, 0, 10)
        }

        val description = TextView(this).apply {
            text = item.getString("description")
            textSize = 16f
            setTextColor(gray)
        }

        val genres = TextView(this).apply {
            text = "\n" + item.getJSONArray("genres").join(" • ")
            textSize = 14f
            setTextColor(blue)
        }

        val watch = Button(this).apply {
            text = "▶  WATCH"
            setOnClickListener {
                openEpisodes(item)
            }
        }

        val add = Button(this).apply {
            text = if (isInMyList(item)) "✓  IN MY LIST" else "＋  MY LIST"

            setOnClickListener {
                if (isInMyList(item)) {
                    removeFromMyList(item)
                    text = "＋  MY LIST"
                } else {
                    myList.add(item)
                    text = "✓  IN MY LIST"
                    Toast.makeText(
                        this@AnimeActivity,
                        "${item.getString("title")} added to My List",
                        Toast.LENGTH_SHORT
                    ).show()
                }
            }
        }

        content.addView(back)
        content.addView(title)
        content.addView(description)
        content.addView(genres)
        content.addView(watch)
        content.addView(add)

        setContentView(root)
    }

    private fun openEpisodes(item: JSONObject) {
        val root = baseScreen()

        val back = Button(this).apply {
            text = "← Back"
            setOnClickListener {
                openAnime(item)
            }
        }

        val title = TextView(this).apply {
            text = item.optString("title", "Anime")
            textSize = 28f
            typeface = Typeface.DEFAULT_BOLD
            setTextColor(white)
            setPadding(0, 12, 0, 4)
        }

        val info = TextView(this).apply {
            text = "${item.optInt("episodeCount", 0)} episodes"
            textSize = 14f
            setTextColor(gray)
            setPadding(0, 0, 0, 16)
        }

        content.addView(back)
        content.addView(title)
        content.addView(info)

        val seasonBar = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            setPadding(0, 0, 0, 16)
        }

        val season1 = Button(this).apply {
            text = "Season 1"
            isAllCaps = false
        }

        val tybw = Button(this).apply {
            text = "Thousand-Year Blood War"
            isAllCaps = false
        }

        seasonBar.addView(
            season1,
            LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.WRAP_CONTENT,
                52
            ).apply {
                setMargins(0, 0, 8, 0)
            }
        )

        if (item.optString("title", "").equals("Bleach", ignoreCase = true)) {
            seasonBar.addView(
                tybw,
                LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.WRAP_CONTENT,
                    52
                )
            )
        }

        content.addView(seasonBar)

        val episodeContainer = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
        }

        content.addView(episodeContainer)

        // Nitron API stores episodes inside seasons[].episodes[].
        // Flatten them into one array for the existing episode UI.
        val episodes = JSONArray()

        item.optJSONArray("seasons")?.let { seasons ->
            for (s in 0 until seasons.length()) {
                val season = seasons.optJSONObject(s) ?: continue
                val seasonEpisodes = season.optJSONArray("episodes") ?: continue

                for (e in 0 until seasonEpisodes.length()) {
                    seasonEpisodes.optJSONObject(e)?.let { episodes.put(it) }
                }
            }
        }

        // Also support a legacy/top-level episodes array if one exists.
        item.optJSONArray("episodes")?.let { legacyEpisodes ->
            for (e in 0 until legacyEpisodes.length()) {
                legacyEpisodes.optJSONObject(e)?.let { episodes.put(it) }
            }
        }

        fun renderEpisodes(start: Int, end: Int, seasonName: String) {
            episodeContainer.removeAllViews()

            val heading = TextView(this).apply {
                text = seasonName
                textSize = 21f
                typeface = Typeface.DEFAULT_BOLD
                setTextColor(white)
                setPadding(0, 8, 0, 12)
            }

            episodeContainer.addView(heading)

            var found = false

            for (i in 0 until episodes.length()) {
                val episode = episodes.getJSONObject(i)
                val number = episode.optInt("number", i + 1)

                if (number < start || number > end) continue

                found = true

                val episodeTitle = episode.optString(
                    "title",
                    "Episode $number"
                )

                val videoUrl = episode.optString(
                    "videoUrl",
                    ""
                ).trim()

                val card = LinearLayout(this).apply {
                    orientation = LinearLayout.HORIZONTAL
                    gravity = Gravity.CENTER_VERTICAL
                    setPadding(16, 12, 16, 12)

                    setBackgroundColor(
                        if (videoUrl.isNotBlank()) {
                            Color.rgb(28, 29, 36)
                        } else {
                            Color.rgb(18, 19, 23)
                        }
                    )

                    setOnClickListener {
                        openEpisode(item, episode)
                    }
                }

                val numberView = TextView(this).apply {
                    text = String.format("%03d", number)
                    textSize = 18f
                    typeface = Typeface.DEFAULT_BOLD
                    setTextColor(white)
                    gravity = Gravity.CENTER
                }

                val details = LinearLayout(this).apply {
                    orientation = LinearLayout.VERTICAL
                }

                val nameView = TextView(this).apply {
                    text = episodeTitle
                    textSize = 16f
                    typeface = Typeface.DEFAULT_BOLD
                    setTextColor(white)
                }

                val statusView = TextView(this).apply {
                    text = if (videoUrl.isNotBlank()) {
                        "Available  •  ▶ Watch"
                    } else {
                        "Video unavailable"
                    }
                    textSize = 13f
                    setTextColor(gray)
                }

                details.addView(nameView)
                details.addView(statusView)

                val play = TextView(this).apply {
                    text = if (videoUrl.isNotBlank()) "▶" else "○"
                    textSize = 22f
                    setTextColor(white)
                    gravity = Gravity.CENTER
                }

                card.addView(
                    numberView,
                    LinearLayout.LayoutParams(64, 72)
                )

                card.addView(
                    details,
                    LinearLayout.LayoutParams(
                        0,
                        LinearLayout.LayoutParams.WRAP_CONTENT,
                        1f
                    ).apply {
                        setMargins(12, 0, 8, 0)
                    }
                )

                card.addView(
                    play,
                    LinearLayout.LayoutParams(52, 72)
                )

                episodeContainer.addView(
                    card,
                    LinearLayout.LayoutParams(
                        LinearLayout.LayoutParams.MATCH_PARENT,
                        76
                    ).apply {
                        setMargins(0, 0, 0, 8)
                    }
                )
            }

            if (!found) {
                val empty = TextView(this).apply {
                    text = "No episodes configured for this season yet."
                    textSize = 16f
                    setTextColor(gray)
                    setPadding(0, 20, 0, 20)
                }

                episodeContainer.addView(empty)
            }
        }

        val total = episodes.length()

        renderEpisodes(
            1,
            if (total > 0) total else 0,
            "Season 1"
        )

        season1.setOnClickListener {
            renderEpisodes(
                1,
                if (total > 0) total else 0,
                "Season 1"
            )
        }

        tybw.setOnClickListener {
            renderEpisodes(
                1,
                1000,
                "Bleach — Thousand-Year Blood War"
            )
        }

        setContentView(root)
    }

    private fun openEpisode(
        anime: JSONObject,
        episode: JSONObject
    ) {
        val videoUrl = episode.optString(
            "videoUrl",
            ""
        ).trim()

        if (videoUrl.isBlank()) {
            val watchUrl = episode.optString(
                "watchUrl",
                anime.optString("watchUrl", "")
            ).trim()

            Toast.makeText(
                this,
                "No direct video stream is configured for this episode.",
                Toast.LENGTH_LONG
            ).show()

            if (watchUrl.isNotBlank()) {
                openAuthorizedWatchPage(
                    anime,
                    episode,
                    watchUrl
                )
            }

            return
        }

        openNativePlayer(
            anime,
            episode,
            videoUrl
        )
    }

    private fun openNativePlayer(
        anime: JSONObject,
        episode: JSONObject,
        videoUrl: String
    ) {
        window.addFlags(
            WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON
        )

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundColor(Color.BLACK)
        }

        val trackSelector = DefaultTrackSelector(this)

        val player = ExoPlayer.Builder(this)
            .setTrackSelector(trackSelector)
            .build()

        val topBar = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            setBackgroundColor(Color.rgb(12, 13, 18))
        }

        val back = Button(this).apply {
            text = "←"
            setOnClickListener {
                player.release()
                window.clearFlags(
                    WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON
                )
                openEpisodes(anime)
            }
        }

        val title = TextView(this).apply {
            text = "  ${episode.optString("title", "Episode")}"
            textSize = 17f
            typeface = Typeface.DEFAULT_BOLD
            setTextColor(Color.WHITE)
            gravity = Gravity.CENTER_VERTICAL
        }

        val rotate = Button(this).apply {
            text = "↻"
            textSize = 20f
            contentDescription = "Rotate"
            setOnClickListener {
                requestedOrientation =
                    if (resources.configuration.orientation ==
                        android.content.res.Configuration.ORIENTATION_PORTRAIT
                    ) {
                        ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE
                    } else {
                        ActivityInfo.SCREEN_ORIENTATION_PORTRAIT
                    }
            }
        }

        val audio = Button(this).apply {
            text = "AUDIO"
            textSize = 10f
            setOnClickListener {
                showAudioDialog(player, trackSelector)
            }
        }

        val subtitles = Button(this).apply {
            text = "CC"
            textSize = 11f
            setOnClickListener {
                showSubtitleDialog(player, trackSelector)
            }
        }

        topBar.addView(
            back,
            LinearLayout.LayoutParams(54, 60)
        )

        topBar.addView(
            title,
            LinearLayout.LayoutParams(
                0,
                60,
                1f
            )
        )

        topBar.addView(
            audio,
            LinearLayout.LayoutParams(68, 60)
        )

        topBar.addView(
            subtitles,
            LinearLayout.LayoutParams(52, 60)
        )

        topBar.addView(
            rotate,
            LinearLayout.LayoutParams(58, 60)
        )

        val playerView = PlayerView(this).apply {
            useController = true
            setBackgroundColor(Color.BLACK)
            controllerShowTimeoutMs = 3000
        }

        playerView.player = player

        player.setMediaItem(
            MediaItem.fromUri(videoUrl)
        )

        player.prepare()
        player.playWhenReady = true

        root.addView(
            topBar,
            LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                60
            )
        )

        root.addView(
            playerView,
            LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                0,
                1f
            )
        )

        setContentView(root)

        playerView.tag = player
    }

    private fun showAudioDialog(
        player: ExoPlayer,
        selector: DefaultTrackSelector
    ) {
        val languages = mutableListOf<String>()
        val labels = mutableListOf<String>()

        for (group in player.currentTracks.groups) {
            if (group.type != C.TRACK_TYPE_AUDIO) continue

            for (i in 0 until group.length) {
                if (!group.isTrackSupported(i)) continue

                val format = group.getTrackFormat(i)
                val language = format.language?.takeIf {
                    it.isNotBlank() && it != "und"
                } ?: "Unknown"

                if (!languages.contains(language)) {
                    languages.add(language)
                    labels.add(
                        format.label ?: language
                    )
                }
            }
        }

        if (languages.isEmpty()) {
            Toast.makeText(
                this,
                "No alternate audio languages are provided by this video.",
                Toast.LENGTH_SHORT
            ).show()
            return
        }

        AlertDialog.Builder(this)
            .setTitle("Audio language")
            .setItems(labels.toTypedArray()) { _, which ->
                selector.parameters =
                    selector.parameters
                        .buildUpon()
                        .setPreferredAudioLanguage(languages[which])
                        .setTrackTypeDisabled(
                            C.TRACK_TYPE_AUDIO,
                            false
                        )
                        .build()
            }
            .show()
    }

    private fun showSubtitleDialog(
        player: ExoPlayer,
        selector: DefaultTrackSelector
    ) {
        val languages = mutableListOf<String>()
        val labels = mutableListOf<String>()

        for (group in player.currentTracks.groups) {
            if (group.type != C.TRACK_TYPE_TEXT) continue

            for (i in 0 until group.length) {
                if (!group.isTrackSupported(i)) continue

                val format = group.getTrackFormat(i)
                val language = format.language?.takeIf {
                    it.isNotBlank() && it != "und"
                } ?: "Unknown"

                if (!languages.contains(language)) {
                    languages.add(language)
                    labels.add(
                        format.label ?: language
                    )
                }
            }
        }

        val options = mutableListOf("Off")
        options.addAll(labels)

        AlertDialog.Builder(this)
            .setTitle("Subtitles")
            .setItems(options.toTypedArray()) { _, which ->
                val builder = selector.parameters.buildUpon()

                if (which == 0) {
                    builder
                        .setTrackTypeDisabled(
                            C.TRACK_TYPE_TEXT,
                            true
                        )
                        .setPreferredTextLanguage(null)
                } else {
                    builder
                        .setTrackTypeDisabled(
                            C.TRACK_TYPE_TEXT,
                            false
                        )
                        .setPreferredTextLanguage(
                            languages[which - 1]
                        )
                }

                selector.parameters = builder.build()
            }
            .show()
    }

    private fun openAuthorizedWatchPage(
        anime: JSONObject,
        episode: JSONObject,
        watchUrl: String
    ) {
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundColor(Color.BLACK)
        }

        val topBar = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            setBackgroundColor(Color.rgb(12, 13, 18))
        }

        val back = Button(this).apply {
            text = "←"
            setOnClickListener {
                openEpisodes(anime)
            }
        }

        val title = TextView(this).apply {
            text = "  ${episode.optString("title", "Episode")}"
            textSize = 18f
            typeface = Typeface.DEFAULT_BOLD
            setTextColor(Color.WHITE)
            gravity = Gravity.CENTER_VERTICAL
        }

        topBar.addView(
            back,
            LinearLayout.LayoutParams(
                60,
                LinearLayout.LayoutParams.MATCH_PARENT
            )
        )

        topBar.addView(
            title,
            LinearLayout.LayoutParams(
                0,
                LinearLayout.LayoutParams.MATCH_PARENT,
                1f
            )
        )

        val webView = WebView(this)

        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true
        webView.settings.mediaPlaybackRequiresUserGesture = false
        webView.settings.allowFileAccess = false
        webView.settings.allowContentAccess = true
        webView.webViewClient = WebViewClient()

        webView.loadUrl(watchUrl)

        root.addView(
            topBar,
            LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                60
            )
        )

        root.addView(
            webView,
            LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                0,
                1f
            )
        )

        setContentView(root)
    }

    private fun openVideo(item: JSONObject) {
        val watchUrl = item.optString("watchUrl", "").trim()

        if (watchUrl.isBlank()) {
            Toast.makeText(
                this,
                "No authorized watch page configured.",
                Toast.LENGTH_LONG
            ).show()
            return
        }

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundColor(Color.BLACK)
        }

        val topBar = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            setBackgroundColor(Color.rgb(12, 13, 18))
        }

        val back = Button(this).apply {
            text = "←"
            setOnClickListener {
                openAnime(item)
            }
        }

        val title = TextView(this).apply {
            text = "  ${item.optString("title", "Anime")}"
            textSize = 18f
            typeface = Typeface.DEFAULT_BOLD
            setTextColor(Color.WHITE)
            gravity = Gravity.CENTER_VERTICAL
        }

        topBar.addView(
            back,
            LinearLayout.LayoutParams(
                60,
                LinearLayout.LayoutParams.MATCH_PARENT
            )
        )

        topBar.addView(
            title,
            LinearLayout.LayoutParams(
                0,
                LinearLayout.LayoutParams.MATCH_PARENT,
                1f
            )
        )

        val webView = WebView(this)

        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true
        webView.settings.mediaPlaybackRequiresUserGesture = false
        webView.settings.allowFileAccess = false
        webView.settings.allowContentAccess = true

        webView.webViewClient = WebViewClient()

        webView.loadUrl(watchUrl)

        root.addView(
            topBar,
            LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                60
            )
        )

        root.addView(
            webView,
            LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                0,
                1f
            )
        )

        setContentView(root)
    }

    private fun showSearch() {
        val root = baseScreen()

        val title = TextView(this).apply {
            text = "Search Anime"
            textSize = 28f
            typeface = Typeface.DEFAULT_BOLD
            setTextColor(white)
        }

        val input = EditText(this).apply {
            hint = "Search anime..."
            setTextColor(white)
            setHintTextColor(gray)
        }

        val results = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
        }

        val searchButton = Button(this).apply {
            text = "SEARCH"
            setOnClickListener {
                results.removeAllViews()

                val query = input.text
                    .toString()
                    .trim()
                    .lowercase()

                for (i in 0 until animeData.length()) {
                    val item = animeData.getJSONObject(i)

                    if (
                        item.getString("title")
                            .lowercase()
                            .contains(query)
                    ) {
                        val result = Button(this@AnimeActivity).apply {
                            text = item.getString("title")
                            setOnClickListener {
                                openAnime(item)
                            }
                        }

                        results.addView(result)
                    }
                }
            }
        }

        content.addView(title)
        content.addView(input)
        content.addView(searchButton)
        content.addView(results)

        setContentView(root)
    }

    private fun showMyList() {
        val root = baseScreen()

        val title = TextView(this).apply {
            text = "My List"
            textSize = 28f
            typeface = Typeface.DEFAULT_BOLD
            setTextColor(white)
        }

        content.addView(title)

        if (myList.isEmpty()) {
            val empty = TextView(this).apply {
                text = "\nYour list is empty.\n\nOpen an anime and press + MY LIST."
                textSize = 16f
                setTextColor(gray)
            }

            content.addView(empty)
        } else {
            for (item in myList) {
                val button = Button(this).apply {
                    text = item.getString("title")
                    setOnClickListener {
                        openAnime(item)
                    }
                }

                content.addView(button)
            }
        }

        setContentView(root)
    }

    private fun isInMyList(item: JSONObject): Boolean {
        for (saved in myList) {
            if (saved.optInt("id") == item.optInt("id")) {
                return true
            }
        }
        return false
    }

    private fun removeFromMyList(item: JSONObject) {
        myList.removeAll {
            it.optInt("id") == item.optInt("id")
        }
    }

    private fun createBottomBar(): LinearLayout {
        val bar = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER
            setBackgroundColor(Color.rgb(15, 16, 22))
            setPadding(5, 10, 5, 10)
        }

        bar.addView(
            bottomButton("⌂", "Home") {
                showHome()
            }
        )

        bar.addView(
            bottomButton("⌕", "Search") {
                showSearch()
            }
        )

        bar.addView(
            bottomButton("＋", "My List") {
                showMyList()
            }
        )

        return bar
    }

    private fun bottomButton(
        icon: String,
        label: String,
        action: () -> Unit
    ): LinearLayout {
        val box = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER
            setPadding(35, 5, 35, 5)

            setOnClickListener {
                action()
            }
        }

        val iconView = TextView(this).apply {
            text = icon
            textSize = 25f
            gravity = Gravity.CENTER
            setTextColor(white)
        }

        val labelView = TextView(this).apply {
            text = label
            textSize = 12f
            gravity = Gravity.CENTER
            setTextColor(gray)
        }

        box.addView(iconView)
        box.addView(labelView)

        return box
    }
}
