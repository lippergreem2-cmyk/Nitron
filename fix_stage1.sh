#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "=== NITRON STAGE 1 ==="

cp app/src/main/java/com/nitron/bubble/NitronImageView.kt \
   app/src/main/java/com/nitron/bubble/NitronImageView.kt.before_stage1 2>/dev/null || true

cp app/src/main/java/com/nitron/bubble/MainActivity.kt \
   app/src/main/java/com/nitron/bubble/MainActivity.kt.before_stage1 2>/dev/null || true

cp app/src/main/res/layout/message_item.xml \
   app/src/main/res/layout/message_item.xml.before_stage1 2>/dev/null || true

cat > app/src/main/java/com/nitron/bubble/NitronImageView.kt <<'KOT'
package com.nitron.bubble

import android.content.Context
import android.graphics.Canvas
import android.graphics.Matrix
import android.graphics.drawable.Drawable
import android.net.Uri
import android.util.AttributeSet
import android.view.MotionEvent
import android.view.ScaleGestureDetector
import android.view.View

class NitronImageView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null
) : View(context, attrs) {

    private var image: Drawable? = null
    private var scale = 1f
    private var offsetX = 0f
    private var offsetY = 0f
    private var lastX = 0f
    private var lastY = 0f

    private val matrix = Matrix()

    private val scaleDetector =
        ScaleGestureDetector(
            context,
            object : ScaleGestureDetector.SimpleOnScaleGestureListener() {
                override fun onScale(detector: ScaleGestureDetector): Boolean {
                    scale *= detector.scaleFactor
                    scale = scale.coerceIn(1f, 5f)
                    invalidate()
                    return true
                }
            }
        )

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)

        val drawable = image ?: return

        val iw = drawable.intrinsicWidth.coerceAtLeast(1)
        val ih = drawable.intrinsicHeight.coerceAtLeast(1)

        val fit = minOf(
            width.toFloat() / iw,
            height.toFloat() / ih
        )

        val drawW = iw * fit
        val drawH = ih * fit

        val left = (width - drawW) / 2f
        val top = (height - drawH) / 2f

        matrix.reset()
        matrix.postScale(fit * scale, fit * scale)
        matrix.postTranslate(
            left + offsetX,
            top + offsetY
        )

        canvas.save()
        canvas.concat(matrix)

        drawable.setBounds(0, 0, iw, ih)
        drawable.draw(canvas)

        canvas.restore()
    }

    override fun onTouchEvent(event: MotionEvent): Boolean {
        scaleDetector.onTouchEvent(event)

        when (event.actionMasked) {

            MotionEvent.ACTION_DOWN -> {
                lastX = event.x
                lastY = event.y
                return true
            }

            MotionEvent.ACTION_MOVE -> {
                if (event.pointerCount == 1) {
                    offsetX += event.x - lastX
                    offsetY += event.y - lastY

                    lastX = event.x
                    lastY = event.y

                    invalidate()
                }

                return true
            }

            MotionEvent.ACTION_UP,
            MotionEvent.ACTION_CANCEL -> {
                return true
            }
        }

        return true
    }

    override fun setImageDrawable(drawable: Drawable?) {
        image = drawable
        resetZoom()
    }

    fun setImageBitmap(bitmap: android.graphics.Bitmap?) {
        image = bitmap?.let {
            android.graphics.drawable.BitmapDrawable(resources, it)
        }
        resetZoom()
    }

    override fun setImageURI(uri: Uri?) {
        if (uri == null) {
            image = null
            invalidate()
            return
        }

        try {
            image = context.contentResolver.getDrawable(uri)
            resetZoom()
        } catch (_: Exception) {
            image = null
            invalidate()
        }
    }

    fun resetZoom() {
        scale = 1f
        offsetX = 0f
        offsetY = 0f
        invalidate()
    }
}
KOT

echo "Image view fixed."

python - <<'PY'
from pathlib import Path

p = Path("app/src/main/res/layout/message_item.xml")
s = p.read_text()

start = s.find('<ImageView')
if start == -1:
    start = s.find('<com.nitron.bubble.NitronImageView')

if start != -1:
    end = s.find('/>', start)

    if end != -1:
        block = s[start:end+2]

        if 'android:id="@+id/messageImage"' in block:
            block2 = block.replace(
                '<ImageView',
                '<com.nitron.bubble.NitronImageView',
                1
            )
            s = s[:start] + block2 + s[end+2:]
            p.write_text(s)
            print("messageImage fixed.")
        else:
            print("messageImage already uses custom view or was not changed.")
    else:
        raise SystemExit("Could not locate end of image view.")
else:
    raise SystemExit("Could not locate image view.")

p = Path("app/src/main/java/com/nitron/bubble/MainActivity.kt")
s = p.read_text()

old = '''Message(
                        "📷 Learning image: $filename",
                        true
                    )'''

new = '''Message(
                        "📷 Sent image: $filename",
                        true,
                        imageUri = uri.toString()
                    )'''

if new in s:
    print("MainActivity image code already fixed.")
elif old in s:
    s = s.replace(old, new, 1)
    p.write_text(s)
    print("MainActivity image code fixed.")
else:
    print("MainActivity image block not changed.")

PY

echo
echo "=== VERIFY ==="

grep -n "class NitronImageView" \
app/src/main/java/com/nitron/bubble/NitronImageView.kt

grep -n "NitronImageView" \
app/src/main/res/layout/message_item.xml

grep -n "imageUri = uri.toString()" \
app/src/main/java/com/nitron/bubble/MainActivity.kt

echo
echo "=== BUILD ==="

gradle assembleDebug

echo
echo "=== COPY APK ==="

cp app/build/outputs/apk/debug/app-debug.apk \
~/storage/downloads/Nitron-debug.apk

echo
echo "================================"
echo "NITRON BUILD COMPLETE"
echo "~/storage/downloads/Nitron-debug.apk"
echo "================================"
