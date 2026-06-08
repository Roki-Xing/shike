#!/usr/bin/env python3
"""Validate Android image preprocessing is real and release-gated."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    """Read a UTF-8 project file.

    Args:
        relative: File path under the Shike root.

    Returns:
        File content, or an empty string when the file is absent.
    """

    path = ROOT / relative
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def contains_all(text: str, tokens: tuple[str, ...]) -> bool:
    """Return whether every required token appears in text.

    Args:
        text: Source text to inspect.
        tokens: Tokens required by the contract.

    Returns:
        True when every token appears at least once.
    """

    return all(token in text for token in tokens)


def contains_any(text: str, tokens: tuple[str, ...]) -> bool:
    """Return whether any forbidden token appears in text.

    Args:
        text: Source text to inspect.
        tokens: Tokens forbidden by the contract.

    Returns:
        True when at least one token appears.
    """

    return any(token in text for token in tokens)


def main() -> int:
    """Run Android image preprocessing checks.

    Returns:
        Process exit code.
    """

    policy = read("android-mvp/app/src/main/java/cn/shike/app/data/ImagePreprocessPolicy.kt")
    preprocessor = read("android-mvp/app/src/main/java/cn/shike/app/data/ImagePayloadPreprocessor.kt")
    thumbnail_cache = read("android-mvp/app/src/main/java/cn/shike/app/data/ImageThumbnailCache.kt")
    main_activity = read("android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt")
    policy_test = read("android-mvp/app/src/test/java/cn/shike/app/data/ImagePreprocessPolicyTest.kt")
    thumbnail_cache_test = read("android-mvp/app/src/test/java/cn/shike/app/data/ImageThumbnailCacheTest.kt")
    docs = "\n".join(
        read(path)
        for path in [
            "README.md",
            "docs/current-validation-status.md",
            "docs/android-mvp-implementation.md",
            "materials/device-demo-checklist.md",
        ]
    )

    checks = [
        (
            "image_preprocess_policy_exists",
            contains_all(
                policy,
                (
                    "object ImagePreprocessPolicy",
                    "const val MAX_EDGE = 1600",
                    "const val JPEG_QUALITY = 82",
                    'const val OUTPUT_MIME = "image/jpeg"',
                    "const val EXIF_NORMAL = 1",
                    "const val EXIF_ROTATE_90 = 6",
                    "const val EXIF_ROTATE_180 = 3",
                    "const val EXIF_ROTATE_270 = 8",
                ),
            ),
            "ImagePreprocessPolicy.kt constants",
        ),
        (
            "image_preprocess_policy_limits_decode_size",
            contains_all(
                policy,
                (
                    "fun sampleSizeFor(",
                    "while (width / sample > maxEdge || height / sample > maxEdge)",
                    "sample *= 2",
                ),
            ),
            "sampleSizeFor",
        ),
        (
            "image_preprocess_policy_tracks_rotation_and_digest",
            contains_all(
                policy,
                (
                    "fun outputDimensionsFor(",
                    "EXIF_ROTATE_90, EXIF_ROTATE_270",
                    "ImageDimensions(width = height, height = width)",
                    "fun sha256Hex(bytes: ByteArray): String",
                    'MessageDigest.getInstance("SHA-256")',
                    'joinToString("") { "%02x".format(it) }',
                ),
            ),
            "rotation + sha256",
        ),
        (
            "image_preprocess_policy_detects_input_mime",
            contains_all(
                policy,
                (
                    "fun mimeForBytes(bytes: ByteArray): String?",
                    '"image/jpeg"',
                    '"image/png"',
                    '"image/webp"',
                    "'R'.code.toByte()",
                    "'W'.code.toByte()",
                ),
            ),
            "magic-byte MIME detection",
        ),
        (
            "image_preprocess_policy_sizes_thumbnail_cache",
            contains_all(
                policy,
                (
                    "const val THUMBNAIL_MAX_EDGE = 360",
                    'const val THUMBNAIL_CACHE_DIR = "shike-image-thumbnails"',
                    "fun thumbnailDimensionsFor(",
                    "maxEdge: Int = THUMBNAIL_MAX_EDGE",
                    "roundToInt().coerceAtLeast(1)",
                    "fun thumbnailFileNameFor(sha256: String): String",
                ),
            ),
            "thumbnail sizing + cache name policy",
        ),
        (
            "image_preprocess_policy_crops_screenshot_chrome",
            contains_all(
                policy,
                (
                    "data class ImageChromeCrop",
                    "enum class ImagePreprocessSource",
                    "SCREENSHOT",
                    "PHOTO_PICKER",
                    "CAMERA",
                    "fun chromeCropFor(",
                    "source != ImagePreprocessSource.SCREENSHOT",
                    "height * 6 / 100",
                    "height * 5 / 100",
                ),
            ),
            "UI chrome crop policy",
        ),
        (
            "image_payload_preprocessor_decodes_bounds_first",
            contains_all(
                preprocessor,
                (
                    "object ImagePayloadPreprocessor",
                    "fun fromBytes(",
                    "bytes: ByteArray",
                    "BitmapFactory.Options().apply { inJustDecodeBounds = true }",
                    "BitmapFactory.decodeByteArray(bytes, 0, bytes.size, bounds)",
                    "ImagePreprocessPolicy.sampleSizeFor(bounds.outWidth, bounds.outHeight)",
                ),
            ),
            "bounds decode",
        ),
        (
            "image_payload_preprocessor_rejects_non_image_bytes_before_decode",
            contains_all(
                preprocessor,
                (
                    "ImagePreprocessPolicy.mimeForBytes(bytes) == null",
                    "return null",
                    "BitmapFactory.Options().apply { inJustDecodeBounds = true }",
                ),
            )
            and preprocessor.find("ImagePreprocessPolicy.mimeForBytes(bytes) == null")
            < preprocessor.find("BitmapFactory.Options().apply { inJustDecodeBounds = true }"),
            "non-image byte rejection",
        ),
        (
            "image_payload_preprocessor_normalizes_and_compresses",
            contains_all(
                preprocessor,
                (
                    "ExifInterface(ByteArrayInputStream(bytes))",
                    "Matrix().apply { postRotate(rotation) }",
                    "Bitmap.createBitmap(",
                    "Bitmap.CompressFormat.JPEG",
                    "ImagePreprocessPolicy.JPEG_QUALITY",
                    "Base64.NO_WRAP",
                    'dataUrl = "data:image/jpeg;base64,$encoded"',
                    "ImagePreprocessPolicy.sha256Hex(jpegBytes)",
                ),
            ),
            "EXIF + JPEG + data URL",
        ),
        (
            "image_payload_preprocessor_applies_source_aware_chrome_crop",
            contains_all(
                preprocessor,
                (
                    "source: ImagePreprocessSource",
                    "ImagePreprocessPolicy.chromeCropFor(",
                    "cropChromeIfNeeded(normalized, source)",
                    "Bitmap.createBitmap(",
                    "crop.outputDimensions.width",
                    "crop.outputDimensions.height",
                ),
            ),
            "source-aware chrome crop",
        ),
        (
            "image_payload_preprocessor_caches_private_thumbnail",
            contains_all(
                preprocessor,
                (
                    "data class ImagePreprocessResult",
                    "val thumbnailUri: String?",
                    "fun fromBytesWithThumbnail(",
                    "thumbnailCacheRoot: File? = null",
                    "buildThumbnailBytes(cropped)",
                    "ImageThumbnailCache.cacheThumbnailBytes(cacheRoot, sha256, thumbnailBytes)",
                    "Bitmap.createScaledBitmap(bitmap, dimensions.width, dimensions.height, true)",
                ),
            )
            and contains_all(
                thumbnail_cache,
                (
                    "object ImageThumbnailCache",
                    "fun cacheThumbnailBytes(",
                    "File(cacheRoot, ImagePreprocessPolicy.THUMBNAIL_CACHE_DIR)",
                    "file.writeBytes(jpegBytes)",
                    "file.toURI().toString()",
                ),
            ),
            "private thumbnail cache",
        ),
        (
            "main_activity_delegates_image_payload_building",
            contains_all(
                main_activity,
                (
                    "import cn.shike.app.data.ImagePayloadPreprocessor",
                    "import cn.shike.app.data.ImagePreprocessSource",
                    "private fun buildImagePayloadFromUri(uriText: String, sourceType: String): BackendImagePayload?",
                    "ImagePayloadPreprocessor.fromBytesWithThumbnail(",
                    "thumbnailCacheRoot = cacheDir",
                    "private fun imagePreprocessSourceFromBackendSource(sourceType: String): ImagePreprocessSource",
                    '"screenshot_share", "recent_screenshot_assist" -> ImagePreprocessSource.SCREENSHOT',
                    "private fun buildImagePayloadFromBitmap(bitmap: Bitmap): BackendImagePayload?",
                    "ImagePayloadPreprocessor.fromBitmapWithThumbnail(",
                ),
            )
            and not contains_any(
                main_activity,
                (
                    "BitmapFactory.decodeByteArray",
                    "Base64.encodeToString",
                    "MessageDigest.getInstance",
                    "imageSampleSize",
                ),
            ),
            "MainActivity.kt delegation",
        ),
        (
            "image_preprocess_policy_unit_test_exists",
            contains_all(
                policy_test,
                (
                    "class ImagePreprocessPolicyTest",
                    "sampleSizeFor_limitsLongEdgeToConfiguredMaximum",
                    "outputDimensionsFor_swapsWidthAndHeightForRotatedExifOrientations",
                    "outputMimeAndDigest_matchBackendImageContract",
                    "thumbnailDimensionsFor_limitsLongEdgeWithoutUpscalingSmallImages",
                    "mimeForBytes_detectsSupportedImageFormatsByMagicBytes",
                    "mimeForBytes_rejectsNonImageBytes",
                    "chromeCropFor_cropsTallScreenshotChromeWithoutChangingWidth",
                    "chromeCropFor_doesNotCropCameraImages",
                    "chromeCropFor_keepsSmallScreenshotsUsable",
                ),
            )
            and policy_test.count("@Test") == 9,
            "ImagePreprocessPolicyTest.kt",
        ),
        (
            "image_thumbnail_cache_unit_test_exists",
            contains_all(
                thumbnail_cache_test,
                (
                    "class ImageThumbnailCacheTest",
                    "cacheThumbnailBytes_persistsPrivateDigestNamedJpeg",
                    "cacheThumbnailBytes_reusesExistingFileForSameDigest",
                    "TemporaryFolder",
                ),
            )
            and thumbnail_cache_test.count("@Test") == 2,
            "ImageThumbnailCacheTest.kt",
        ),
        (
            "android_image_preprocess_gate_documented",
            contains_all(
                docs,
                (
                    "validate_android_image_preprocess.py",
                    "ANDROID_IMAGE_PREPROCESS_METRIC 15/15",
                    "ImagePayloadPreprocessor",
                    "ImageThumbnailCache",
                    "EXIF",
                    "MIME",
                    "UI chrome",
                    "SHA-256",
                ),
            ),
            "README/status/android docs/checklist",
        ),
    ]

    passed = sum(1 for _, ok, _ in checks if ok)
    for name, ok, evidence in checks:
        print(f"{'PASS' if ok else 'FAIL'}\t{name}\t{evidence}")
    print(f"ANDROID_IMAGE_PREPROCESS_METRIC\t{passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
