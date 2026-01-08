# Ghauri Android App - Build Instructions

This document provides instructions on how to build the Ghauri SQL Injection Tool as an Android APK using Kivy and Buildozer.

## 🚀 Quick Start: Automated Builds

**NEW:** The APK is now built automatically via GitHub Actions!

### Download Pre-built APK

1. Go to the [Actions tab](../../actions/workflows/build-apk.yml)
2. Click on the latest successful workflow run
3. Scroll to **Artifacts** section
4. Download `ghauri-android-apk`
5. Extract and install the APK on your Android device

**Build time:** ~20-30 minutes (with cache) | **Artifact retention:** 30 days

### Automated Build Triggers

The APK builds automatically when:
- Code is pushed to `main`, `master`, `develop`, or `copilot/*` branches
- Pull requests are created/updated
- Manually triggered via workflow dispatch

---

## Overview

The Ghauri Android app is a mobile version of the Ghauri SQL injection detection and exploitation tool. It provides a user-friendly graphical interface for security professionals to test web applications for SQL injection vulnerabilities directly from their Android devices.

---

## Manual Build (Local)

If you want to build the APK locally instead of using automated builds:

### Prerequisites

### For Building the APK

1. **Linux Environment** (Ubuntu 20.04 or later recommended)
   - Buildozer currently works best on Linux
   - Windows users can use WSL2 (Windows Subsystem for Linux)
   - macOS users may encounter issues; Linux VM recommended

2. **Python 3.7 or higher**
   ```bash
   python3 --version
   ```

3. **System Dependencies**
   ```bash
   sudo apt update
   sudo apt install -y python3-pip build-essential git python3-dev \
       ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev \
       libsdl2-ttf-dev libportmidi-dev libswscale-dev \
       libavformat-dev libavcodec-dev zlib1g-dev \
       libgstreamer1.0-dev gstreamer1.0-plugins-base \
       gstreamer1.0-plugins-good openjdk-11-jdk \
       autoconf libtool pkg-config cmake ninja-build \
       ccache
   ```

4. **Install Cython**
   ```bash
   pip3 install --upgrade Cython==0.29.33
   ```

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/r0oth3x49/ghauri.git
   cd ghauri
   ```

2. **Install Python dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

## Building the APK

### Using Buildozer (Recommended)

1. **Initialize Buildozer** (if starting fresh)
   ```bash
   buildozer init
   ```
   Note: This project already includes a `buildozer.spec` file, so this step is optional.

2. **Build the APK for Android**
   ```bash
   buildozer android debug
   ```
   
   This command will:
   - Download Android SDK and NDK (first time only)
   - Download and compile Python for Android
   - Install all required dependencies
   - Build the APK file
   
   The first build may take 30-60 minutes depending on your system.

3. **Find the APK**
   After successful build, the APK will be located at:
   ```
   bin/ghauri-1.4.3-arm64-v8a-debug.apk
   ```

4. **Build for Release** (optional)
   ```bash
   buildozer android release
   ```
   
   Note: You'll need to sign the release APK with a keystore.

### Building for Specific Architecture

To build for a specific Android architecture:

```bash
# For ARM 64-bit (recommended for modern devices)
buildozer android debug

# The buildozer.spec is configured to build for both:
# - arm64-v8a (64-bit ARM)
# - armeabi-v7a (32-bit ARM)
```

### Troubleshooting Build Issues

1. **Java Version Issues**
   ```bash
   # Ensure Java 11 is being used
   sudo update-alternatives --config java
   ```

2. **Clean Build**
   If you encounter errors:
   ```bash
   buildozer android clean
   buildozer android debug
   ```

3. **Insufficient Memory**
   Buildozer requires significant RAM. If building fails:
   - Close other applications
   - Increase swap space
   - Use a machine with at least 8GB RAM

4. **NDK/SDK Download Issues**
   If automatic downloads fail:
   ```bash
   # Clear buildozer cache
   rm -rf ~/.buildozer
   # Try again
   buildozer android debug
   ```

## Installing the APK on Android Device

### Via USB (ADB)

1. **Enable Developer Options** on your Android device
   - Go to Settings > About Phone
   - Tap "Build Number" 7 times
   
2. **Enable USB Debugging**
   - Go to Settings > Developer Options
   - Enable "USB Debugging"

3. **Install ADB** (if not already installed)
   ```bash
   sudo apt install android-tools-adb
   ```

4. **Connect device and install**
   ```bash
   adb devices  # Verify device is connected
   adb install bin/ghauri-1.4.3-arm64-v8a-debug.apk
   ```

### Via File Transfer

1. Copy the APK file to your Android device
2. Use a file manager to locate the APK
3. Tap the APK to install (you may need to enable "Install from Unknown Sources")

## Using the Ghauri Android App

### App Features

The app includes three main tabs:

1. **Basic Tab**
   - Enter target URL
   - Configure POST data, cookies
   - Select DBMS type
   - Choose injection technique
   - Select action (test injection, enumerate databases, etc.)

2. **Advanced Tab**
   - Custom User-Agent
   - Proxy configuration
   - Timeout and delay settings
   - Test level (1-3)
   - Thread count
   - Batch mode and random agent options

3. **Results Tab**
   - View scan results and output
   - Clear results button

### Basic Usage

1. **Test for SQL Injection**
   - Enter target URL: `http://example.com/page.php?id=1`
   - Select "Test Injection" action
   - Tap "Run Scan"

2. **Enumerate Databases**
   - After successful injection detection
   - Select "List Databases" action
   - Tap "Run Scan"

3. **Dump Table Data**
   - Select "Dump Data" action
   - Enter database name
   - Enter table name
   - (Optional) Enter columns
   - Tap "Run Scan"

### Important Notes

- **Network Permissions**: The app requires internet access to perform scans
- **Legal Usage**: Only test systems you have permission to test
- **Battery Usage**: SQL injection testing can be CPU-intensive
- **Background Execution**: Long scans should be completed with the app in foreground

## App Permissions

The app requests the following Android permissions:
- `INTERNET` - Required for making HTTP/HTTPS requests
- `ACCESS_NETWORK_STATE` - To check network connectivity
- `ACCESS_WIFI_STATE` - To check WiFi status

## Development and Debugging

### Running in Development Mode

For testing during development:

```bash
# Deploy to connected device
buildozer android deploy run

# View logs
buildozer android logcat
```

### Debugging

To see Python errors and debug output:
```bash
adb logcat | grep python
```

## Configuration

The `buildozer.spec` file contains all build configuration:

- **App name and version**: Lines 4-25
- **Requirements**: Line 48
- **Permissions**: Line 84
- **Android API levels**: Lines 87-92
- **Architecture**: Line 233

Edit these settings as needed for your deployment.

## Known Limitations

1. **Session Files**: Session storage is limited on Android
2. **File Upload**: Request file loading (`-r` option) not fully supported in GUI
3. **Performance**: May be slower than desktop version due to mobile hardware
4. **Multi-target**: Bulk file scanning (`-m` option) not implemented in GUI

## Security Considerations

- Store the app securely on your device
- Do not grant the app unnecessary permissions
- Use responsibly and ethically
- Keep the app updated for security patches

## Support and Contributing

For issues, feature requests, or contributions:
- GitHub: https://github.com/r0oth3x49/ghauri
- Report bugs in the Issues section
- Submit pull requests for improvements

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Legal Disclaimer

Usage of Ghauri for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state, and federal laws. The developer assumes no liability and is not responsible for any misuse or damage caused by this program.

## Credits

- **Original Author**: Nasir Khan (r0ot h3x49)
- **Framework**: Kivy for Python
- **Build Tool**: Buildozer
- **Android Support**: Python-for-Android (p4a)
