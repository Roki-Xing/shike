package cn.shike.app

import android.graphics.Bitmap
import cn.shike.app.data.ScreenshotCandidate
import cn.shike.app.data.cameraSelectionFromPreview
import cn.shike.app.data.gallerySelectionFromImage
import cn.shike.app.data.screenshotSelectionFromCandidate
import cn.shike.app.domain.ShikeItem

fun applyCameraPreviewSelection(
    bitmap: Bitmap,
    persistSelection: (ShikeItem, String) -> Unit,
) = applyCameraPreviewSizeSelection(bitmap.width, bitmap.height, persistSelection)

/**
 * Persist a camera preview selection from dimensions only.
 *
 * Args:
 *     width: Preview bitmap width in pixels.
 *     height: Preview bitmap height in pixels.
 *     persistSelection: Callback that stores the generated item and source.
 */
fun applyCameraPreviewSizeSelection(
    width: Int,
    height: Int,
    persistSelection: (ShikeItem, String) -> Unit,
) {
    val selection = cameraSelectionFromPreview(width, height)
    val item = selection.item
    val source = selection.source
    persistSelection(item, source)
}

fun applyGalleryImageSelection(
    label: String,
    persistSelection: (ShikeItem, String) -> Unit,
) {
    val selection = gallerySelectionFromImage(label)
    val item = selection.item
    val source = selection.source
    persistSelection(item, source)
}

fun applyScreenshotCandidateSelection(
    candidate: ScreenshotCandidate,
    persistSelection: (ShikeItem, String) -> Unit,
) {
    val selection = screenshotSelectionFromCandidate(candidate)
    persistSelection(selection.item, selection.source)
}
