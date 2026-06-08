#!/usr/bin/env python3
"""Validate Shike's user-initiated image upload boundary.

The Android app may upload an image only after the user intentionally selects,
captures, or confirms importing it. Passive screenshot detection and system
share receive paths must create local candidates first.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Check:
    """One validation result."""

    name: str
    ok: bool
    evidence: str


def read(relative: str) -> str:
    """Read a UTF-8 repository file.

    Args:
        relative: Repository-relative path.

    Returns:
        File content, or an empty string when the file is absent.
    """

    path = ROOT / relative
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def function_body(source: str, name: str) -> str:
    """Extract a Kotlin function body by brace matching.

    Args:
        source: Kotlin source text.
        name: Function name to locate.

    Returns:
        Function body including braces, or an empty string if not found.
    """

    match = re.search(rf"\bfun\s+{re.escape(name)}\b", source)
    if not match:
        return ""
    equals_index = source.find("=", match.end())
    brace_index = source.find("{", match.end())
    next_match = re.search(
        r"\n    (?:private\s+|override\s+|internal\s+|public\s+)?fun\s+",
        source[match.end() :],
    )
    next_fun_index = match.end() + next_match.start() if next_match else -1
    if equals_index != -1 and (next_fun_index == -1 or equals_index < next_fun_index):
        end_index = next_fun_index if next_fun_index != -1 else source.find("\n}", match.end())
        return source[match.start() : end_index if end_index != -1 else len(source)]
    if brace_index == -1:
        return ""
    if next_fun_index != -1 and brace_index > next_fun_index:
        return source[match.start() : next_fun_index]
    depth = 0
    for index in range(brace_index, len(source)):
        char = source[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return source[brace_index : index + 1]
    return ""


def property_lambda_body(source: str, property_name: str) -> str:
    """Extract a named Kotlin property lambda body.

    Args:
        source: Kotlin source text.
        property_name: Named argument or property before the lambda.

    Returns:
        Lambda body including braces, or an empty string if not found.
    """

    match = re.search(rf"\b{re.escape(property_name)}\s*=", source)
    if not match:
        return ""
    brace_index = source.find("{", match.end())
    if brace_index == -1:
        return ""
    depth = 0
    for index in range(brace_index, len(source)):
        char = source[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return source[brace_index : index + 1]
    return ""


def no_backend_upload_code(text: str) -> bool:
    """Check that a source block does not construct or call image upload."""

    forbidden = (
        "runBackendAnalysis",
        "callAnalyzeImageApi",
        "buildAnalyzeImageRequestPayload",
        "buildImagePayloadFromUri",
        "buildImagePayloadFromBitmap",
        "buildImagePayloadFromBytes",
        "data:image/jpeg;base64",
        "HttpURLConnection",
        "/v2/analyze-image",
    )
    return all(token not in text for token in forbidden)


def main() -> int:
    """Run the no-default-image-upload validation."""

    app = read("android-mvp/app/src/main/java/cn/shike/app/ShikeApp.kt")
    activity = read("android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt")
    backend_runner = read("android-mvp/app/src/main/java/cn/shike/app/data/BackendAnalysisRunner.kt")
    model_api = read("android-mvp/app/src/main/java/cn/shike/app/data/ModelApiClient.kt")
    local_multimodal = read("android-mvp/app/src/main/java/cn/shike/app/ui/LocalMultimodalStatus.kt")
    analyze_image_test = read("android-mvp/app/src/test/java/cn/shike/app/data/AnalyzeImageApiClientTest.kt")
    share_mapper = read("android-mvp/app/src/main/java/cn/shike/app/data/ShareImportMapper.kt")
    capture_mapper = read("android-mvp/app/src/main/java/cn/shike/app/data/CaptureImportMapper.kt")
    observer = read("android-mvp/app/src/main/java/cn/shike/app/system/ScreenshotObserver.kt")
    notification = read("android-mvp/app/src/main/java/cn/shike/app/system/ScreenshotNotification.kt")
    android_doc = read("docs/android-mvp-implementation.md")
    readme = read("README.md")

    manual_entry = property_lambda_body(app, "onManualInput")
    apply_screenshot_candidate = function_body(app, "applyScreenshotCandidate")
    consume_shared_image = function_body(activity, "consumeSharedImageIntent")
    on_screenshot_candidate = function_body(activity, "onScreenshotCandidate")
    analyze_current_draft = function_body(app, "analyzeCurrentDraftWithBackend")
    analyze_with_backend = function_body(app, "analyzeWithBackend")
    run_backend_analysis = function_body(backend_runner, "runBackendAnalysis")

    checks = [
        Check(
            "share_text_is_local_only",
            "ManualOcrEngine()" in share_mapper
            and "allowCloudEnhancement = false" in share_mapper
            and 'channel == "share"' in capture_mapper
            and "imageCleared" in capture_mapper,
            "ShareImportMapper.kt + CaptureImportMapper.kt",
        ),
        Check(
            "manual_entry_clears_prior_image_uri",
            "selectedSourceMediaStoreUri = null" in manual_entry
            and "capturedBitmap = null" in manual_entry
            and "ImageCleanupStatus.NOT_SUPPORTED" in manual_entry,
            "ShikeApp.kt onManualInput",
        ),
        Check(
            "shared_image_import_only_creates_candidate",
            "pendingScreenshotCandidate = ScreenshotCandidate" in consume_shared_image
            and no_backend_upload_code(consume_shared_image),
            "MainActivity.kt consumeSharedImageIntent",
        ),
        Check(
            "screenshot_observer_only_discovers_candidate",
            "ContentObserver" in observer
            and "MediaStore.Images.Media.EXTERNAL_CONTENT_URI" in observer
            and "ScreenshotCandidate(" in observer
            and no_backend_upload_code(observer),
            "ScreenshotObserver.kt",
        ),
        Check(
            "screenshot_notification_is_user_prompt",
            "拾刻检测到一张新截图" in notification
            and "是否交给拾刻生成行动卡" in notification
            and no_backend_upload_code(notification),
            "ScreenshotNotification.kt",
        ),
        Check(
            "foreground_candidate_import_triggers_user_initiated_analysis",
            "applyScreenshotCandidateSelection" in apply_screenshot_candidate
            and "persistSelection" in apply_screenshot_candidate
            and "analyzeCurrentDraftWithBackend()" in apply_screenshot_candidate,
            "ShikeApp.kt applyScreenshotCandidate",
        ),
        Check(
            "notification_candidate_only_sets_pending_state",
            "pendingScreenshotCandidate = candidate" in on_screenshot_candidate
            and "showScreenshotDetectedNotification" in on_screenshot_candidate
            and no_backend_upload_code(on_screenshot_candidate),
            "MainActivity.kt onScreenshotCandidate",
        ),
        Check(
            "image_payload_provider_is_analyze_action_scoped",
            "analyzeCurrentDraftWithBackend" in app
            and "selectedSourceMediaStoreUri ?: capturedBitmap" in analyze_current_draft
            and "imagePayloadProvider" in analyze_with_backend
            and "onBuildImagePayload(input.imageUri, input.imageSourceType)" in analyze_with_backend
            and "onBuildBitmapPayload(capturedBitmap!!)" in analyze_with_backend,
            "ShikeApp.kt analyzeCurrentDraftWithBackend/analyzeWithBackend",
        ),
        Check(
            "backend_image_payload_is_lazy",
            "imagePayloadProvider?.invoke()" in run_backend_analysis
            and "callAnalyzeImageApi" in run_backend_analysis
            and run_backend_analysis.find("imagePayloadProvider?.invoke()") < run_backend_analysis.find("callAnalyzeImageApi"),
            "BackendAnalysisRunner.kt runBackendAnalysis",
        ),
        Check(
            "v2_payload_requires_explicit_image_payload",
            "fun buildAnalyzeImageRequestPayload" in model_api
            and ".put(\"image\", JSONObject()" in model_api
            and "allowCloudImage: Boolean = true" in model_api
            and ".put(\"allow_cloud_image\", allowCloudImage)" in model_api
            and "/v2/analyze-image" in model_api,
            "ModelApiClient.kt",
        ),
        Check(
            "android_can_disable_cloud_image_upload_for_local_preferred",
            "fun allowCloudImageForPreference" in local_multimodal
            and "preference == LocalMultimodalPreference.CloudFirst" in local_multimodal
            and "allowCloudImageForPreference(localMultimodalPreference)" in analyze_current_draft
            and "val allowCloudImage: Boolean = true" in backend_runner
            and "allowCloudImage = input.allowCloudImage" in run_backend_analysis
            and "buildAnalyzeImageRequestPayload_canDisableCloudImageUpload" in analyze_image_test
            and "allowCloudImage = false" in analyze_image_test
            and "assertFalse(payload.getBoolean(\"allow_cloud_image\"))" in analyze_image_test,
            "LocalMultimodalStatus.kt + ShikeApp.kt + BackendAnalysisRunner.kt + AnalyzeImageApiClientTest.kt",
        ),
        Check(
            "docs_state_user_initiated_image_upload",
            "用户主动选择相册、拍照或确认导入截图后自动请求" in android_doc
            and "被动截图检测仍只生成候选或通知" in android_doc
            and "Android 只调用自有后端且不持有任何 vivo AppKEY" in readme,
            "docs/android-mvp-implementation.md + README.md",
        ),
    ]

    passed = sum(1 for check in checks if check.ok)
    for check in checks:
        status = "PASS" if check.ok else "FAIL"
        print(f"{status}\t{check.name}\t{check.evidence}")
    print(f"NO_DEFAULT_IMAGE_UPLOAD_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
