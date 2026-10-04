package com.nitron.bubble

import android.accessibilityservice.AccessibilityService
import android.accessibilityservice.GestureDescription
import android.graphics.Path
import android.view.accessibility.AccessibilityEvent
import android.view.accessibility.AccessibilityNodeInfo

class NitronAccessibilityService : AccessibilityService() {

    companion object {
        @Volatile
        var instance: NitronAccessibilityService? = null
            private set

        fun isEnabled(): Boolean = instance != null
    }

    override fun onServiceConnected() {
        super.onServiceConnected()
        instance = this
    }

    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        // Nitron can observe supported accessibility-visible UI here.
        // Commands will be routed here later.
    }

    override fun onInterrupt() {
        // Android interrupted the accessibility service.
    }

    override fun onDestroy() {
        if (instance === this) {
            instance = null
        }
        super.onDestroy()
    }

    fun getActiveWindowRoot(): AccessibilityNodeInfo? {
        return rootInActiveWindow
    }

    fun clickText(text: String): Boolean {
        val root = rootInActiveWindow ?: return false

        val nodes = root.findAccessibilityNodeInfosByText(text)

        for (node in nodes) {
            if (node.isClickable && node.performAction(
                    AccessibilityNodeInfo.ACTION_CLICK
                )
            ) {
                return true
            }

            var parent = node.parent
            while (parent != null) {
                if (parent.isClickable &&
                    parent.performAction(
                        AccessibilityNodeInfo.ACTION_CLICK
                    )
                ) {
                    return true
                }
                parent = parent.parent
            }
        }

        return false
    }

    fun typeText(text: String): Boolean {
        val root = rootInActiveWindow ?: return false
        val focused = root.findFocus(
            AccessibilityNodeInfo.FOCUS_INPUT
        ) ?: return false

        if (!focused.isEditable) return false

        val arguments = android.os.Bundle()

        arguments.putCharSequence(
            AccessibilityNodeInfo.ACTION_ARGUMENT_SET_TEXT_CHARSEQUENCE,
            text
        )

        return focused.performAction(
            AccessibilityNodeInfo.ACTION_SET_TEXT,
            arguments
        )
    }

    fun scrollForward(): Boolean {
        val root = rootInActiveWindow ?: return false

        return findScrollable(root)?.performAction(
            AccessibilityNodeInfo.ACTION_SCROLL_FORWARD
        ) == true
    }

    fun scrollBackward(): Boolean {
        val root = rootInActiveWindow ?: return false

        return findScrollable(root)?.performAction(
            AccessibilityNodeInfo.ACTION_SCROLL_BACKWARD
        ) == true
    }

    fun pressBack(): Boolean {
        return performGlobalAction(
            GLOBAL_ACTION_BACK
        )
    }

    fun goHome(): Boolean {
        return performGlobalAction(
            GLOBAL_ACTION_HOME
        )
    }

    fun openRecents(): Boolean {
        return performGlobalAction(
            GLOBAL_ACTION_RECENTS
        )
    }

    fun tap(x: Float, y: Float): Boolean {
        val path = Path()
        path.moveTo(x, y)

        val gesture = GestureDescription.Builder()
            .addStroke(
                GestureDescription.StrokeDescription(
                    path,
                    0,
                    80
                )
            )
            .build()

        return dispatchGesture(
            gesture,
            null,
            null
        )
    }

    private fun findScrollable(
        node: AccessibilityNodeInfo
    ): AccessibilityNodeInfo? {

        if (node.isScrollable) {
            return node
        }

        for (i in 0 until node.childCount) {
            val child = node.getChild(i) ?: continue

            val result = findScrollable(child)

            if (result != null) {
                return result
            }
        }

        return null
    }
}
