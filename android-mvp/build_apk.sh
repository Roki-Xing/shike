#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLS_ROOT="${HOME}/.local/share/shike-android-tools"
ANDROID_HOME="${TOOLS_ROOT}/android-sdk"
GRADLE_HOME="${TOOLS_ROOT}/gradle-8.10.2"
LOCAL_JAVA_HOME="${TOOLS_ROOT}/jdk-local/usr/lib/jvm/java-21-openjdk-amd64"
CMDLINE_ZIP="${TOOLS_ROOT}/commandlinetools-linux-11076708_latest.zip"
GRADLE_ZIP="${TOOLS_ROOT}/gradle-8.10.2-bin.zip"
REPORT="${ROOT}/build-report.md"

mkdir -p "${TOOLS_ROOT}" "${ANDROID_HOME}/cmdline-tools"

{
  echo "# Android MVP 构建报告"
  echo
  echo "- 时间: $(date -Iseconds)"
  echo "- 工程: ${ROOT}"
  echo
} > "${REPORT}"

if [ ! -d "${ANDROID_HOME}/cmdline-tools/latest" ]; then
  if [ ! -f "${CMDLINE_ZIP}" ]; then
    curl -L --fail -o "${CMDLINE_ZIP}" "https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip"
  fi
  rm -rf "${ANDROID_HOME}/cmdline-tools/latest" "${ANDROID_HOME}/cmdline-tools/cmdline-tools"
  unzip -q "${CMDLINE_ZIP}" -d "${ANDROID_HOME}/cmdline-tools"
  mv "${ANDROID_HOME}/cmdline-tools/cmdline-tools" "${ANDROID_HOME}/cmdline-tools/latest"
fi

if [ ! -d "${GRADLE_HOME}" ]; then
  if [ ! -f "${GRADLE_ZIP}" ]; then
    curl -L --fail -o "${GRADLE_ZIP}" "https://services.gradle.org/distributions/gradle-8.10.2-bin.zip"
  fi
  unzip -q "${GRADLE_ZIP}" -d "${TOOLS_ROOT}"
fi

export ANDROID_HOME
export ANDROID_SDK_ROOT="${ANDROID_HOME}"
if [ -x "${LOCAL_JAVA_HOME}/bin/javac" ]; then
  export JAVA_HOME="${LOCAL_JAVA_HOME}"
fi
export PATH="${JAVA_HOME:-}/bin:${GRADLE_HOME}/bin:${ANDROID_HOME}/cmdline-tools/latest/bin:${ANDROID_HOME}/platform-tools:${PATH}"

yes | sdkmanager --licenses >/tmp/shike-sdk-licenses.log || true
sdkmanager "platform-tools" "platforms;android-35" "build-tools;35.0.0" >/tmp/shike-sdk-install.log

cd "${ROOT}"
gradle --no-daemon :app:assembleDebug >/tmp/shike-gradle-build.log

APK="${ROOT}/app/build/outputs/apk/debug/app-debug.apk"
if [ ! -s "${APK}" ]; then
  echo "APK not found: ${APK}" >&2
  exit 1
fi

{
  echo "- Android SDK: ${ANDROID_HOME}"
  echo "- Gradle: ${GRADLE_HOME}"
  echo "- JAVA_HOME: ${JAVA_HOME:-system}"
  echo "- APK: ${APK}"
  echo "- 状态: 通过"
} >> "${REPORT}"

echo "${APK}"
