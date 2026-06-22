package cn.shike.app

data class BuildProvenance(
    val versionLabel: String,
    val shortGitSha: String,
    val buildTimeUtc: String,
) {
    val displayVersion: String
        get() = "版本 $versionLabel · 构建 $shortGitSha"
}

fun currentBuildProvenance(): BuildProvenance =
    BuildProvenance(
        versionLabel = BuildConfig.VERSION_LABEL,
        shortGitSha = BuildConfig.SHORT_GIT_SHA,
        buildTimeUtc = BuildConfig.BUILD_TIME_UTC,
    )
