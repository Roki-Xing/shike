import java.time.Instant

plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

fun gitOutput(vararg args: String): String =
    providers.exec {
        commandLine("git", *args)
    }.standardOutput.asText.get().trim()

val shortGitSha = runCatching { gitOutput("rev-parse", "--short=7", "HEAD") }.getOrDefault("unknown")
val buildTimeUtc = providers.environmentVariable("SHIKE_BUILD_TIME_UTC")
    .orElse(Instant.now().toString())
    .get()

android {
    namespace = "cn.shike.app"
    compileSdk = 36

    defaultConfig {
        applicationId = "cn.shike.app"
        minSdk = 26
        targetSdk = 36
        versionCode = 1
        versionName = "0.1.0"
        buildConfigField("String", "SHORT_GIT_SHA", "\"$shortGitSha\"")
        buildConfigField("String", "BUILD_TIME_UTC", "\"$buildTimeUtc\"")
        buildConfigField("String", "VERSION_LABEL", "\"$versionName\"")
    }

    buildFeatures {
        compose = true
        buildConfig = true
    }

    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.15"
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.activity:activity-compose:1.9.3")
    implementation("androidx.core:core:1.13.1")
    implementation(platform("androidx.compose:compose-bom:2024.10.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    debugImplementation("androidx.compose.ui:ui-tooling")
    testImplementation("junit:junit:4.13.2")
    testImplementation("org.json:json:20240303")
}
