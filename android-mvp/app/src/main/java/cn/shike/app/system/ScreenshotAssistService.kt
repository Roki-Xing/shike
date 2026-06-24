package cn.shike.app.system

import android.app.Service
import android.content.Context
import android.content.Intent
import android.os.Handler
import android.os.IBinder
import android.os.Looper
import androidx.core.app.NotificationCompat
import androidx.core.content.ContextCompat
import cn.shike.app.data.ScreenshotCandidate
import cn.shike.app.data.recordScreenshotAssistNotified
import cn.shike.app.data.shouldNotifyScreenshotCandidate
import java.util.concurrent.Executors

private const val SCREENSHOT_ASSIST_SERVICE_ID = 2701
private const val ACTION_START_SCREENSHOT_ASSIST = "cn.shike.app.action.START_SCREENSHOT_ASSIST"
private const val ACTION_STOP_SCREENSHOT_ASSIST = "cn.shike.app.action.STOP_SCREENSHOT_ASSIST"
private const val HEARTBEAT_INTERVAL_MS = 10_000L

class ScreenshotAssistService : Service() {
    private val handler = Handler(Looper.getMainLooper())
    private val queryExecutor = Executors.newSingleThreadExecutor()
    private var observer: ScreenshotObserver? = null
    private val heartbeatRunnable = object : Runnable {
        override fun run() {
            recordScreenshotAssistHeartbeat(
                context = this@ScreenshotAssistService,
                observerOwner = "service",
                observerRegistered = observer != null,
            )
            handler.postDelayed(this, HEARTBEAT_INTERVAL_MS)
        }
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        if (intent?.action == ACTION_STOP_SCREENSHOT_ASSIST || !hasScreenshotMediaPermission(this)) {
            stopAssist(if (intent?.action == ACTION_STOP_SCREENSHOT_ASSIST) "USER_DISABLED" else "PERMISSION_REVOKED")
            return START_NOT_STICKY
        }
        createScreenshotAssistNotificationChannel(this)
        if (!startForegroundSafely()) {
            stopAssist("START_FAILED")
            return START_NOT_STICKY
        }
        registerObserver()
        return START_NOT_STICKY
    }

    override fun onDestroy() {
        stopAssist("SYSTEM_STOPPED")
        queryExecutor.shutdownNow()
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null

    private fun registerObserver() {
        if (observer != null) return
        observer = ScreenshotObserver(contentResolver, handler, queryExecutor, ::onCandidate).also { it.register() }
        recordScreenshotAssistHeartbeat(this, observerOwner = "service", observerRegistered = true)
        handler.removeCallbacks(heartbeatRunnable)
        handler.postDelayed(heartbeatRunnable, HEARTBEAT_INTERVAL_MS)
    }

    private fun onCandidate(candidate: ScreenshotCandidate) {
        if (!shouldNotifyScreenshotCandidate(this, candidate)) return
        recordScreenshotAssistNotified(this, candidate)
        recordScreenshotAssistDetected(this, candidate.createdAtMillis)
        showScreenshotDetectedNotification(this, candidate)
    }

    override fun onTimeout(startId: Int, fgsType: Int) {
        stopAssist("FGS_TIMEOUT")
    }

    private fun stopAssist(reason: String) {
        handler.removeCallbacks(heartbeatRunnable)
        observer?.unregister()
        observer = null
        recordScreenshotAssistStopped(this, reason)
        runCatching { stopForeground(STOP_FOREGROUND_REMOVE) }
        stopSelf()
    }

    private fun startForegroundSafely(): Boolean =
        runCatching {
            startForeground(SCREENSHOT_ASSIST_SERVICE_ID, foregroundNotification())
        }.isSuccess

    private fun foregroundNotification() =
        NotificationCompat.Builder(this, SCREENSHOT_ASSIST_CHANNEL_ID)
            .setSmallIcon(android.R.drawable.ic_menu_upload)
            .setContentTitle("截图助手已开启")
            .setContentText("检测到新截图后会通知你是否交给拾刻。")
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .setOngoing(true)
            .build()
}

fun startScreenshotAssistService(context: Context) {
    val intent = Intent(context, ScreenshotAssistService::class.java).setAction(ACTION_START_SCREENSHOT_ASSIST)
    runCatching { ContextCompat.startForegroundService(context, intent) }
}

fun stopScreenshotAssistService(context: Context) {
    runCatching {
        context.startService(Intent(context, ScreenshotAssistService::class.java).setAction(ACTION_STOP_SCREENSHOT_ASSIST))
    }
}
