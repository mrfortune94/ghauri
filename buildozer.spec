[app]

# (str) Title of your application
title = Ghauri SQL Injection Tool

# (str) Package name
package.name = ghauri

# (str) Package domain (needed for android/ios packaging)
package.domain = org.ghauri

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,txt

# (list) List of directory to exclude
source.exclude_dirs = tests, bin, .git, .github, __pycache__

# (str) Application versioning
version = 1.4.3

# (list) Application requirements
# Note: pysocks is required for SOCKS5 proxy support (Orbot/Tor integration)
requirements = python3,kivy,tldextract,colorama,requests,chardet,ua_generator,certifi,urllib3,idna,charset-normalizer,pysocks

# (str) Supported orientation
orientation = portrait

#
# Android specific
#

fullscreen = 0
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE
android.api = 33
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25c

# ✅ Explicit NDK path to avoid permission errors
# Adjust folder name if unzip produces "android-ndk-r25b-linux"
android.ndk_path = /usr/local/lib/android/sdk/ndk/25.2.9519653
# NDK path is auto-detected from ANDROID_NDK_HOME environment variable
# No need to hardcode the path here
#android.ndk_path =
# NDK path will be auto-detected from ANDROID_NDK_HOME environment variable
#android.ndk_path =
# Let buildozer auto-detect NDK path from ANDROID_NDK_HOME
# android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
android.sdk_path = /usr/local/lib/android/sdk

# (str) ANT directory (if empty, it will be automatically downloaded.)
android.ant_path = /usr/bin/ant

android.accept_sdk_license = True

# (str) The Android arch to build for
android.archs = arm64-v8a, armeabi-v7a

android.allow_backup = True
android.copy_libs = 1

#
# Python for android (p4a) specific
#

#p4a.fork = kivy
#p4a.branch = master
# p4a.bootstrap = sdl2

#
# iOS specific
#

ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.7.0

[buildozer]

log_level = 2
warn_on_root = 1
# build_dir = ./.buildozer
# bin_dir = ./bin
