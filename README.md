# APKBully

**APKBully** is a fast, automated Android APK decompiler and secret scanning tool. It decompiles APKs using **JADX** and scans the extracted source code and resources for exposed credentials, API tokens, and other secrets using **BetterLeaks**.

<p align="left">
  <img src="https://github.com/user-attachments/assets/ded0bf66-d7ca-45bb-899f-17fdd1cad995" alt="APKBully scanning interface" width="800">
</p>

<p align="left">
  <img src="https://github.com/user-attachments/assets/8c741094-f78e-448c-a615-ceb9bcef885f" alt="APKBully scan results" width="800">
</p>

---

## Features

- **Automated Tool Setup (`setup`)**
  - Automatically detects and configures the Java Runtime Environment (JRE).
  - If root or sudo access is unavailable, APKBully downloads and configures a standalone portable OpenJDK 17 runtime in user space.
  - Downloads and verifies BetterLeaks (`v2.0.0-rc.7`).
  - Downloads and configures JADX (`v1.5.6`).

- **Full APK Scan (`scan`)**
  - Validates the target APK file.
  - Decompiles application code and XML resources using JADX.
  - Scans extracted sources and resources for exposed credentials, API keys, and secrets.

- **Direct Directory Scan (`direct-scan`)**
  - Scans existing decompiled source directories without requiring another decompilation step.
    
- **Structured Findings and JSON Output**
  - Displays findings with rule names, descriptions, file locations, line numbers, and redacted secrets.
  - Supports JSON report generation through `-o / --output`.
  - Validates the output file extension and automatically generates a timestamped filename (`output_<hhmmss>.json`) when the output path is omitted or invalid.

---

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/TushN101/APKBully.git
cd APKBully
```

### 2. Initialize the Environment

```bash
python3 apkbully.py setup
```

This initializes `~/.apkbully/` and downloads the required dependencies and binaries, including the JRE, BetterLeaks, and JADX.

---

## Usage

### 1. Full APK Scan

Decompiles the specified APK and scans the extracted codebase for exposed secrets.

```bash
# Generate a timestamped JSON report
python3 apkbully.py scan -i path/to/app.apk

# Specify a custom JSON output file
python3 apkbully.py scan -i path/to/app.apk -o findings.json
```

### 2. Direct Scan on Decompiled Code

Scans an existing decompiled source directory without running JADX again.

```bash
python3 apkbully.py direct-scan -i path/to/decompiled_src -o findings.json
```

### 3. Force Re-setup

Force APKBully to re-download and reconfigure its dependencies.

```bash
python3 apkbully.py setup --force
```
