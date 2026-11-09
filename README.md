# APKBully 🛡️

**APKBully** is a fast, automated Android APK decompiler and secret leak scanner. It decompiles APKs using **JADX** and scans the extracted code and resources for credentials, API tokens, and secrets using **BetterLeaks**.

---

## ✨ Features

- **Automated Tool Setup (`setup`)**:
  - Automatically verifies and sets up the Java Runtime Environment (JRE). If root/sudo is not available, APKBully seamlessly downloads and configures a standalone portable OpenJDK 17 runtime in user-space.
  - Downloads and verifies **BetterLeaks** (`v2.0.0-rc.7`).
  - Downloads and configures **JADX** (`v1.5.6`).
- **Full APK Scan (`scan`)**:
  - Validates the target APK file.
  - Decompiles both code and XML resources using JADX.
  - Scans decompiled sources for exposed keys and secrets.
- **Direct Directory Scan (`direct-scan`)**:
  - Directly scans existing decompiled source trees, skipping decompilation.
- **Live Terminal Animations**:
  - Displays dynamic spinners and download progress bars powered by Python `while` loops.
- **Structured Findings & JSON Output**:
  - Displays formatted console findings including rule names, descriptions, file locations, line numbers, and redacted secrets.
  - Validates `-o / --output` to ensure `.json` extension (automatically falls back to timestamped `output_<hhmmss>.json` if invalid or omitted).

---

## 🚀 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/TushN101/APKBully.git
   cd APKBully
   ```

2. **Run Environment Setup**:
   ```bash
   python3 apkbully.py setup
   ```
   *This initializes `~/.apkbully/` and downloads all required binaries (JRE, BetterLeaks, JADX).*

---

## 📖 Usage

### 1. Full APK Scan
Decompiles the specified APK and scans the extracted codebase for secret leaks:
```bash
# Default timestamped JSON report (e.g., output_182254.json)
python3 apkbully.py scan -i path/to/app.apk

# Custom JSON output report
python3 apkbully.py scan -i path/to/app.apk -o findings.json
```

### 2. Direct Scan on Decompiled Code
Directly scans an already decompiled folder:
```bash
python3 apkbully.py direct-scan -i path/to/decompiled_src -o findings.json
```

### 3. Force Re-setup
To force re-downloading and re-extracting dependencies:
```bash
python3 apkbully.py setup --force
```

---

## 📂 Project Architecture

```
APKBully/
├── apkbully.py                  # Main CLI entrypoint
├── requirements.txt             # Python dependencies
├── utils/
│   ├── config.py                # Paths, URLs, and binary finders
│   ├── animation.py             # Python while-loop animations & progress
│   ├── setup.py                 # Setup orchestration and state marker
│   ├── betterleaks_setup.py     # BetterLeaks downloader and extractor
│   ├── jadx_setup.py            # JADX downloader and extractor
│   ├── jre_installer.py         # JRE manager (Apt + Portable OpenJDK fallback)
│   ├── apk_decompiler.py        # JADX APK decompilation runner
│   └── apk_scanner.py           # BetterLeaks scanner & result formatter
```
