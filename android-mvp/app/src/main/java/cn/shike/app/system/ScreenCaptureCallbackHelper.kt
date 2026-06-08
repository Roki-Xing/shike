package cn.shike.app.system

import android.app.Activity
import android.os.Build

class ScreenCaptureCallbackHelper(
    private val activity: Activity,
    private val onVisibleScreenCaptured: () -> Unit,
) {
    private var callback: Activity.ScreenCaptureCallback? = null

    fun register() {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.UPSIDE_DOWN_CAKE || callback != null) {
            return
        }
        val next = Activity.ScreenCaptureCallback { onVisibleScreenCaptured() }
        activity.registerScreenCaptureCallback(activity.mainExecutor, next)
        callback = next
    }

    fun unregister() {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.UPSIDE_DOWN_CAKE) {
            callback = null
            return
        }
        callback?.let(activity::unregisterScreenCaptureCallback)
        callback = null
    }
}
