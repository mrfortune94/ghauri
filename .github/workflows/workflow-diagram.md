# Automated APK Build Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                         TRIGGER EVENTS                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   Push to   │  │     Pull     │  │   Manual Trigger     │  │
│  │   main/     │  │   Request    │  │  (workflow_dispatch) │  │
│  │  master/    │  │              │  │                      │  │
│  │  develop/   │  │              │  │                      │  │
│  │ copilot/*   │  │              │  │                      │  │
│  └──────┬──────┘  └──────┬───────┘  └──────────┬───────────┘  │
│         │                │                     │              │
└─────────┼────────────────┼─────────────────────┼──────────────┘
          │                │                     │
          └────────────────┴─────────────────────┘
                           │
                           ▼
          ┌────────────────────────────────────┐
          │    GitHub Actions Runner (Ubuntu)   │
          └────────────────────────────────────┘
                           │
                           ▼
          ┌────────────────────────────────────┐
          │    1. Checkout Repository          │
          │    2. Setup Python 3.11            │
          │    3. Setup Java 17                │
          └────────────────┬───────────────────┘
                           │
                           ▼
          ┌────────────────────────────────────┐
          │    4. Install System Dependencies  │
          │       - SDL2, FFmpeg, etc.         │
          │       - Build tools                │
          └────────────────┬───────────────────┘
                           │
                           ▼
          ┌────────────────────────────────────┐
          │    5. Restore Cache (if available) │
          │       - Pip packages               │
          │       - Buildozer directory        │
          └────────────────┬───────────────────┘
                           │
                           ▼
          ┌────────────────────────────────────┐
          │    6. Install Python Dependencies  │
          │       - Cython 0.29.33             │
          │       - Buildozer, Kivy, etc.      │
          └────────────────┬───────────────────┘
                           │
                           ▼
          ┌────────────────────────────────────┐
          │    7. Build APK with Buildozer     │
          │       $ buildozer android debug    │
          │       (60-90 min first / 20-30 cached) │
          └────────────────┬───────────────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
     ┌────────────────┐        ┌───────────────┐
     │   SUCCESS ✅   │        │   FAILURE ❌  │
     └────────┬───────┘        └───────┬───────┘
              │                        │
              ▼                        ▼
     ┌────────────────┐        ┌───────────────┐
     │  Upload APK    │        │  Upload Logs  │
     │  Artifact      │        │  Artifact     │
     │  (30 days)     │        │  (7 days)     │
     └────────┬───────┘        └───────────────┘
              │
              ▼
     ┌────────────────┐
     │  Post PR       │
     │  Comment       │
     │  (if PR)       │
     └────────────────┘
              │
              ▼
     ┌────────────────────────────────────┐
     │  APK Available for Download        │
     │  from Actions → Artifacts          │
     └────────────────────────────────────┘
```

## Build Optimization

The workflow uses caching to speed up builds:

```
┌─────────────────────────────────────────────┐
│            FIRST BUILD (no cache)           │
├─────────────────────────────────────────────┤
│  Download SDK/NDK: ~30 min                  │
│  Compile dependencies: ~20 min              │
│  Build APK: ~10 min                         │
├─────────────────────────────────────────────┤
│  TOTAL: 60-90 minutes                       │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│       SUBSEQUENT BUILDS (with cache)        │
├─────────────────────────────────────────────┤
│  Restore cache: ~2 min                      │
│  Verify dependencies: ~3 min                │
│  Build APK: ~15 min                         │
├─────────────────────────────────────────────┤
│  TOTAL: 20-30 minutes                       │
└─────────────────────────────────────────────┘
```

## Artifact Retention

```
APK Artifacts:      ├─────────────────────────────┤ 30 days
Build Logs (fail):  ├──────────┤ 7 days
```

After retention period, artifacts are automatically deleted.
