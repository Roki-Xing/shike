#!/usr/bin/env python3
"""Validate action execution safety and fallback invariants."""

from __future__ import annotations

from pathlib import Path

from source_tree import read_android_source

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    """Read a UTF-8 project file.

    Args:
        relative: File path under the Shike root.

    Returns:
        File content.
    """

    return (ROOT / relative).read_text(encoding="utf-8")


def main() -> int:
    """Run action execution invariant checks.

    Returns:
        Process exit code.
    """

    android_source = read_android_source(ROOT)
    main_activity = read("android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt")
    planner_controls = read("android-mvp/app/src/main/java/cn/shike/app/ui/ActionPlannerExecutionControls.kt")
    banner_actions = read("android-mvp/app/src/main/java/cn/shike/app/ui/ConfirmBannerActions.kt")
    execution_action_gate = read("android-mvp/app/src/main/java/cn/shike/app/ui/ExecutionActionGate.kt")
    execution_result = read("android-mvp/app/src/main/java/cn/shike/app/ui/ExecutionResult.kt")
    reminder_permission_fallback = read("android-mvp/app/src/main/java/cn/shike/app/ReminderPermissionFallback.kt")
    reminder_scheduler = read("android-mvp/app/src/main/java/cn/shike/app/system/ReminderScheduler.kt")
    reminder_payload = read("android-mvp/app/src/main/java/cn/shike/app/system/ReminderPayload.kt")
    reminder_receiver = read("android-mvp/app/src/main/java/cn/shike/app/system/ReminderReceiver.kt")
    boot_receiver = read("android-mvp/app/src/main/java/cn/shike/app/system/BootReminderReceiver.kt")
    system_actions = read("android-mvp/app/src/main/java/cn/shike/app/system/SystemActions.kt")
    manifest = read("android-mvp/app/src/main/AndroidManifest.xml")
    docs = "\n".join(
        read(path)
        for path in [
            "README.md",
            "docs/current-validation-status.md",
            "docs/optimization-log.md",
        ]
    )

    checks = [
        (
            "action_buttons_require_confirmation",
            "canUseReminder = isConfirmed" in execution_action_gate
            and "enabled = gate.canUseReminder" in planner_controls
            and "enabled = gate.canUseReminder" in banner_actions
            and "先确认字段" in banner_actions,
        ),
        (
            "calendar_requires_time_and_does_not_claim_saved",
            "canUseCalendar = isConfirmed && !missingTime" in execution_action_gate
            and "enabled = gate.canUseCalendar" in planner_controls
            and "enabled = gate.canUseCalendar" in banner_actions
            and "已打开系统新增页" in execution_result
            and "不得假装" not in execution_result,
        ),
        (
            "map_requires_location_and_has_copy_fallback",
            "canUseMap = isConfirmed && !missingLocation" in execution_action_gate
            and "enabled = gate.canUseMap" in planner_controls
            and "enabled = gate.canUseMap" in banner_actions
            and "ClipboardManager" in system_actions
            and "copyMapLocationFallback" in main_activity,
        ),
        (
            "reminder_uses_alarm_manager_scheduler",
            "AlarmManager" in reminder_scheduler
            and "PendingIntent.getBroadcast" in reminder_scheduler
            and "alarmManager.set" in reminder_scheduler,
        ),
        (
            "reminder_exact_alarm_policy_has_fallback",
            "setExactAndAllowWhileIdle" in reminder_scheduler
            and "canScheduleExactAlarms()" in reminder_scheduler
            and "Build.VERSION_CODES.S" in reminder_scheduler
            and "catch (_: SecurityException)" in reminder_scheduler
            and "alarmManager.set(AlarmManager.RTC_WAKEUP" in reminder_scheduler
            and "调度模式" in reminder_payload,
        ),
        (
            "reminder_persists_scheduled_payload",
            "PREFERENCES_NAME" in reminder_scheduler
            and "persistScheduledReminder" in reminder_scheduler
            and "scheduled_reminder_trigger_at_millis" in reminder_scheduler
            and "putLong(KEY_SCHEDULED_TRIGGER" in reminder_scheduler,
        ),
        (
            "reminder_restores_pending_alarm_on_app_start",
            "restoreScheduledReminder" in reminder_scheduler
            and "loadScheduledReminder" in reminder_scheduler
            and "shouldRestoreScheduledReminder(reminder, System.currentTimeMillis())" in reminder_scheduler
            and "fun shouldRestoreScheduledReminder(" in reminder_payload
            and "restoreScheduledReminder(this)" in main_activity,
        ),
        (
            "reminder_recovers_after_device_reboot",
            "android.permission.RECEIVE_BOOT_COMPLETED" in manifest
            and "BootReminderReceiver" in manifest
            and "android.intent.action.BOOT_COMPLETED" in manifest
            and "Intent.ACTION_BOOT_COMPLETED" in boot_receiver
            and "restoreScheduledReminder(context)" in boot_receiver,
        ),
        (
            "reminder_clears_persisted_payload_after_delivery",
            "clearScheduledReminder" in reminder_scheduler
            and "clearScheduledReminder(context)" in reminder_receiver
            and "showReminderNotificationPayload" in reminder_receiver,
        ),
        (
            "local_data_clear_cancels_pending_reminder_alarm",
            "cancelScheduledReminder" in reminder_scheduler
            and "PendingIntent.FLAG_NO_CREATE" in reminder_scheduler
            and "alarmManager.cancel(pendingIntent)" in reminder_scheduler
            and "pendingIntent.cancel()" in reminder_scheduler
            and "cancelScheduledReminder(this)" in main_activity
            and "clearInboxSnapshot(this)" in main_activity
            and "clearBackendBaseUrl(this)" in main_activity,
        ),
        (
            "reminder_receiver_registered_and_posts_payload",
            "ReminderReceiver" in manifest
            and "android:exported=\"false\"" in manifest
            and "showReminderNotificationPayload" in reminder_receiver,
        ),
        (
            "notification_permission_denial_preserves_card",
            "permission_blocked" in reminder_permission_fallback
            and "reminderPermissionFallbackCopyFor" in main_activity
            and "已保留" in reminder_permission_fallback
            and "saveReminderPermissionFallback" in main_activity
            and "saveSnapshot" in main_activity,
        ),
        (
            "execution_result_mentions_scheduled_reminder",
            "已调度" in execution_result and "本地定时提醒" in execution_result,
        ),
        (
            "external_intents_have_fallback_catches",
            "ActivityNotFoundException" in system_actions
            and "SecurityException" in system_actions
            and "startSystemActivitySafely" in main_activity,
        ),
        (
            "product_beta_strict_documents_execution_guard",
            "PRODUCT_BETA_METRIC 30/30" in docs
            and "AlarmManager" in docs
            and "permission_blocked" in docs,
        ),
        (
            "docs_describe_reminder_recovery_guard",
            "ACTION_EXECUTION_METRIC 17/17" in docs
            and "应用启动" in docs
            and "设备重启" in docs
            and "restoreScheduledReminder" in docs,
        ),
        (
            "no_unconfirmed_direct_system_dispatch_from_ui",
            all(
                token not in planner_controls + banner_actions
                for token in ["startActivity", "AlarmManager", "NotificationManager", "ClipboardManager"]
            ),
        ),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"ACTION_EXECUTION_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
