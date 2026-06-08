package cn.shike.app

import android.Manifest
import android.graphics.Bitmap
import androidx.activity.result.PickVisualMediaRequest
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.platform.LocalContext
import cn.shike.app.system.hasCameraPermission

data class CaptureLaunchers(
    val launchCamera: () -> Unit,
    val launchGallery: () -> Unit,
)

@Composable
fun rememberCaptureLaunchers(
    onCameraPreview: (Bitmap) -> Unit,
    onCameraUnavailable: () -> Unit,
    onCameraPermissionDenied: () -> Unit,
    onGalleryImage: (String) -> Unit,
    onGalleryUnavailable: () -> Unit,
): CaptureLaunchers {
    val context = LocalContext.current
    val cameraLauncher = rememberLauncherForActivityResult(
        ActivityResultContracts.TakePicturePreview()
    ) { bitmap ->
        if (bitmap != null) {
            onCameraPreview(bitmap)
        } else {
            onCameraUnavailable()
        }
    }
    val cameraPermissionLauncher = rememberLauncherForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { granted ->
        if (granted) {
            cameraLauncher.launch(null)
        } else {
            onCameraPermissionDenied()
        }
    }
    val galleryLauncher = rememberLauncherForActivityResult(
        ActivityResultContracts.PickVisualMedia()
    ) { uri ->
        if (uri != null) {
            onGalleryImage(uri.toString())
        } else {
            onGalleryUnavailable()
        }
    }

    return remember(context, cameraLauncher, cameraPermissionLauncher, galleryLauncher) {
        CaptureLaunchers(
            launchCamera = {
                if (hasCameraPermission(context)) {
                    cameraLauncher.launch(null)
                } else {
                    cameraPermissionLauncher.launch(Manifest.permission.CAMERA)
                }
            },
            launchGallery = {
                galleryLauncher.launch(
                    PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly)
                )
            },
        )
    }
}
