#!/usr/bin/env python3
"""Validate capture sources keep real source MediaStore URIs for cleanup."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    """Read a UTF-8 project file."""

    path = ROOT / relative
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def main() -> int:
    mapper = read("android-mvp/app/src/main/java/cn/shike/app/data/CaptureImportMapper.kt")
    state = read("android-mvp/app/src/main/java/cn/shike/app/ShikeAppState.kt")
    actions = read("android-mvp/app/src/main/java/cn/shike/app/ShikeAppActions.kt")
    intents = read("android-mvp/app/src/main/java/cn/shike/app/ActivityImportIntents.kt")
    activity = read("android-mvp/app/src/main/java/cn/shike/app/MainActivityLifecycleActions.kt")
    manager = read("android-mvp/app/src/main/java/cn/shike/app/system/SourceImageCleanupManager.kt")
    tests = read("android-mvp/app/src/test/java/cn/shike/app/data/CaptureImportMapperTest.kt")
    cleanup_tests = read("android-mvp/app/src/test/java/cn/shike/app/ShikeAppStateCleanupTest.kt")
    manager_tests = read("android-mvp/app/src/test/java/cn/shike/app/system/SourceImageCleanupManagerTest.kt")
    no_upload_validator = read("validation/validate_no_default_image_upload.py")

    checks = [
        (
            "capture_draft_has_source_media_uri_and_status",
            "val sourceMediaStoreUri" in mapper
            and "val imageCleanupStatus" in mapper
            and "val canDeleteOriginal" in mapper
            and "enum class ImageCleanupStatus" in mapper,
        ),
        (
            "gallery_uses_selected_content_uri_as_source",
            "fun gallerySelectionFromImage" in mapper
            and "sourceMediaStoreUri = label" in state
            and "initialCleanupStatusForSourceUri(label)" in state
            and "isMediaStoreUri(uri)" in state + manager,
        ),
        (
            "screenshot_candidate_uses_notification_media_uri",
            "fun screenshotSelectionFromCandidate" in mapper
            and "candidate.contentUri" in mapper + state
            and "sourceMediaStoreUri = candidate.contentUri" in state,
        ),
        (
            "shared_image_candidate_keeps_source_uri",
            "screenshotCandidateFromSharedImage" in intents
            and "contentUri = uri.toString()" in intents
            and "consumeSharedImageIntent" in activity,
        ),
        (
            "camera_and_manual_are_not_cleanup_sources",
            "captureDraftFromInput_keepsCameraThumbnailOutOfOriginalMediaUri" in tests
            and "assertEquals(null, draft.sourceMediaStoreUri)" in tests
            and "ImageCleanupStatus.NOT_SUPPORTED" in mapper + state
            and "selectedSourceMediaStoreUri = null" in state,
        ),
        (
            "state_preserves_source_uri_through_backend_and_review",
            "persistedImageCleanupStatus" in state
            and "sourceMediaStoreUri = sourceMediaStoreUri" in state
            and "imageCleanupStatus = imageCleanupStatus" in state
            and "updateReviewedItem_preservesSourceImageCleanupStateAfterConfirmation" in cleanup_tests,
        ),
        (
            "backend_image_payload_uses_same_selected_source_uri",
            "input.imageUri != null && input.imageUri == state.selectedSourceMediaStoreUri" in actions
            and "onBuildImagePayload(input.imageUri, input.imageSourceType)" in actions,
        ),
        (
            "tests_cover_media_and_non_media_sources",
            "assertEquals(\"content://media/external/images/media/42\", draft.sourceMediaStoreUri)" in tests
            and "assertEquals(null, draft.sourceMediaStoreUri)" in tests
            and "content://media/external/images/media/99" in tests,
        ),
        (
            "manual_input_clears_stale_image_uri",
            "selectedSourceMediaStoreUri = null" in state
            and "onManualInput = { state.enterManualInput() }" in read("android-mvp/app/src/main/java/cn/shike/app/ShikeScreenHost.kt")
            and "manual_entry_clears_prior_image_uri" in no_upload_validator,
        ),
        (
            "cleanup_manager_rejects_non_media_uris",
            "isMediaStoreUri_acceptsOnlySystemMediaContentUris" in manager_tests
            and "content://com.example.provider/image/42" in manager_tests
            and "file:/private-cache" in manager_tests,
        ),
        (
            "cleanup_manager_rejects_picker_proxy_and_collection_uri",
            "content://media/picker/0/com.android.providers.media.photopicker/media/42" in manager_tests
            and "content://media/external/images/media" in manager_tests
            and "PHOTO_PICKER_PROXY" in manager
            and "STANDARD_MEDIASTORE_ITEM" in manager
            and "Regex(\"^[^/]+/images/media/[0-9]+$\")" in manager,
        ),
    ]

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}")
    print(f"CAPTURE_SOURCE_URI_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
