# Automated APK Builds - Quick Reference

## 📦 Download Pre-built APK

The easiest way to get the Ghauri Android APK is to download it from GitHub Actions:

### Step-by-Step:

1. **Go to Actions Tab**
   - Visit: https://github.com/mrfortune94/ghauri/actions/workflows/build-apk.yml
   - Or click "Actions" at the top of the repository

2. **Find Latest Build**
   - Look for the latest workflow run with a ✅ green checkmark
   - Click on the workflow run name

3. **Download APK**
   - Scroll down to the "Artifacts" section
   - Click on `ghauri-android-apk` to download
   - Extract the ZIP file to get the APK

4. **Install on Android**
   - Transfer APK to your Android device
   - Enable "Install from Unknown Sources" in Settings
   - Tap the APK file to install

## 🔄 When Does It Build?

The APK builds automatically when:

- ✅ Code is pushed to `main`, `master`, `develop` branches
- ✅ Code is pushed to any `copilot/*` branch
- ✅ Pull requests are created/updated
- ✅ Manually triggered (see below)

**Only triggers when these files change:**
- `main.py`
- `buildozer.spec`
- `ghauri/**` (any file in ghauri package)
- `requirements.txt`
- `.github/workflows/build-apk.yml`

## ▶️ Manual Trigger

You can manually build the APK even without code changes:

1. Go to **Actions** tab
2. Click **Build Android APK** on the left sidebar
3. Click **Run workflow** button (top right)
4. Select the branch you want to build
5. Click **Run workflow**

The build will start immediately.

## ⏱️ Build Time

- **First build**: ~60-90 minutes (downloads Android SDK/NDK)
- **Subsequent builds**: ~20-30 minutes (uses cached dependencies)

## 📊 Build Status

Check if the build succeeded:

- ✅ **Green checkmark**: Build successful, APK available
- ❌ **Red X**: Build failed, check logs
- 🟡 **Yellow dot**: Build in progress

## 🐛 If Build Fails

1. Click on the failed workflow run
2. Click on the `build-apk` job
3. Expand the failed step to see error details
4. Download `buildozer-logs` artifact for full logs

## 📱 APK Details

**What you get:**
- File: `ghauri-1.4.3-arm64-v8a-debug.apk`
- Size: ~50-80 MB
- Architectures: arm64-v8a, armeabi-v7a (works on most Android devices)
- Signed: Debug signature (for testing only)

## 🔐 Security Note

The APK is built in **debug mode** and signed with a debug key. For production/release:

1. You'll need to set up release signing
2. Create a keystore for signing
3. Configure buildozer.spec with signing details
4. Update workflow to build release APK

## 📝 Artifact Retention

- **APK artifacts**: Kept for 30 days
- **Build logs**: Kept for 7 days (on failure)

After this period, artifacts are automatically deleted. Download before they expire!

## 🎯 Quick Links

- **Latest Builds**: https://github.com/mrfortune94/ghauri/actions/workflows/build-apk.yml
- **Build Guide**: [ANDROID_BUILD.md](ANDROID_BUILD.md)
- **Usage Guide**: [ANDROID_USAGE.md](ANDROID_USAGE.md)
- **Workflow Config**: [.github/workflows/build-apk.yml](.github/workflows/build-apk.yml)

---

**Tip**: Bookmark the Actions page for quick access to new builds!
