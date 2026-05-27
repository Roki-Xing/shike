# Android MVP 构建报告

- 时间: 2026-05-25T07:54:11+08:00
- 工程: /home/xing-12_26/projects/codex-workspace/shike/android-mvp
- 验证方式: 直接 Gradle 验证 `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
- APK: /home/xing-12_26/projects/codex-workspace/shike/android-mvp/app/build/outputs/apk/debug/app-debug.apk
- 状态: 通过
- 最新证据: `BUILD SUCCESSFUL in 33s`
- 单元测试: `:app:testDebugUnitTest` 通过，`PrivacyRedactionTest` 报告 2 tests、0 failures、0 errors；`CaptureImportMapperTest` 报告 3 tests、0 failures、0 errors；`ShareImportMapperTest` 报告 4 tests、0 failures、0 errors；`InitialSelectionMapperTest` 报告 3 tests、0 failures、0 errors；`ExecutionResultActionsTest` 报告 3 tests、0 failures、0 errors；`ExecutionResultStateTest` 报告 3 tests、0 failures、0 errors；`ReminderPermissionFallbackTest` 报告 2 tests、0 failures、0 errors；`ReviewStatusMapperTest` 报告 3 tests、0 failures、0 errors；`ReviewActionsTest` 报告 2 tests、0 failures、0 errors；`CaptureResultActionsTest` 报告 2 tests、0 failures、0 errors；`ModelExplanationTest` 报告 3 tests、0 failures、0 errors；`ModelApiClientTest` 报告 5 tests、0 failures、0 errors；`TodayActionItemMapperTest` 报告 3 tests、0 failures、0 errors；`ExecutionActionGateTest` 报告 3 tests、0 failures、0 errors；`InboxWorkbenchTest` 报告 5 tests、0 failures、0 errors；`ReminderPayloadTest` 报告 6 tests、0 failures、0 errors；`BackendAnalysisRunnerTest` 报告 4 tests、0 failures、0 errors；`BackendEndpointActionsTest` 报告 3 tests、0 failures、0 errors；`BackendTriggerActionsTest` 报告 2 tests、0 failures、0 errors；`BackendOutcomeActionsTest` 报告 3 tests、0 failures、0 errors；`SampleActionsTest` 报告 2 tests、0 failures、0 errors；`LocalInboxStoreTest` 报告 4 tests、0 failures、0 errors；`LocalDataClearActionsTest` 报告 3 tests、0 failures、0 errors；`CloudEnhancementActionsTest` 报告 3 tests、0 failures、0 errors；本地单元测试合计 76 tests、0 failures、0 errors
- APK_SHA256: `a9bdea5a67e687ea71c7884d86fb84d722417326385b521a2d8ab8a5c9cd222d`
- 备注: 当前 shell 的系统 `java` 缺少 `javac`，本轮显式设置项目本地 JDK `~/.local/share/shike-android-tools/jdk-local/usr/lib/jvm/java-21-openjdk-amd64` 和项目本地 Gradle `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle` 完成同一 Gradle 任务。
