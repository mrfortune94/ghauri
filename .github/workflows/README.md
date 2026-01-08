# GitHub Actions Workflows

## Build Android APK (`build-apk.yml`)

This workflow automatically builds the Ghauri Android APK using Buildozer.

### Triggers

The workflow runs on:

1. **Push to branches:**
   - `main`
   - `master`
   - `develop`
   - Any branch starting with `copilot/`

2. **Pull requests** targeting `main` or `master`

3. **Manual trigger** via workflow_dispatch

### What it does

1. Sets up Ubuntu environment with Python 3.11
2. Installs required system dependencies (SDL2, Java, build tools)
3. Installs Python dependencies (Buildozer, Cython, Kivy, etc.)
4. Builds the APK using `buildozer android debug`
5. Uploads the APK as a workflow artifact (30-day retention)
6. Comments on PRs with build status and APK information

### Caching

The workflow uses GitHub Actions cache for:
- **Pip packages**: Cached based on `requirements.txt`
- **Buildozer directory**: Cached based on `buildozer.spec`

This significantly speeds up subsequent builds (from ~60 minutes to ~20 minutes).

### Build Output

**On Success:**
- APK artifact named `ghauri-android-apk` is uploaded
- APK information is logged (filename, size, architecture)
- PR comment is posted with download instructions

**On Failure:**
- Build logs are uploaded as `buildozer-logs` artifact
- Logs are retained for 7 days for debugging

### Downloading the APK

1. Go to the **Actions** tab in the repository
2. Click on the latest successful workflow run
3. Scroll down to **Artifacts**
4. Download `ghauri-android-apk`
5. Extract the ZIP file to get the APK

### Build Time

- **First build**: ~60-90 minutes (downloads Android SDK/NDK)
- **Subsequent builds**: ~20-30 minutes (uses cache)

### Requirements

The workflow automatically installs:
- Python 3.11
- OpenJDK 17
- Buildozer and dependencies
- Android SDK and NDK (via Buildozer)
- All system libraries (SDL2, FFmpeg, etc.)

### Configuration

The workflow uses the existing configuration files:
- `buildozer.spec` - APK build settings
- `requirements.txt` - Python dependencies
- `main.py` - Application entry point

### Manual Trigger

You can manually trigger the build:

1. Go to **Actions** tab
2. Select **Build Android APK** workflow
3. Click **Run workflow**
4. Select the branch
5. Click **Run workflow** button

### Troubleshooting

If the build fails:

1. Check the workflow logs in the Actions tab
2. Download the `buildozer-logs` artifact for detailed error messages
3. Common issues:
   - Dependency conflicts: Update `requirements.txt`
   - Build timeout: Increase `timeout-minutes` in workflow
   - Cache corruption: Clear cache and rebuild

### Notes

- The APK is built in **debug mode** (unsigned)
- For release builds, you'll need to add signing configuration
- Build artifacts are automatically cleaned up after 30 days
- The workflow only runs when relevant files are changed
