"""utils/jadx_setup.py

Downloads and sets up JADX decompiler.
"""

import os
import stat
import zipfile
from pathlib import Path
from utils.config import folder, installerFolder, jadxFolder, jadxBin, jadxUrl
from utils.animation import download_with_progress, Spinner

fn = "utils/jadx_setup.py"


def jadxSanityCheck() -> bool:
    """Check if base directories exist."""
    try:
        if folder.is_dir() and installerFolder.is_dir() and jadxFolder.is_dir():
            print(f"[✓] {fn}: Required folders exist.")
            return True
        else:
            print(f"[✗] {fn}: Base directories missing. Running directory setup...")
            folder.mkdir(parents=True, exist_ok=True)
            installerFolder.mkdir(parents=True, exist_ok=True)
            jadxFolder.mkdir(parents=True, exist_ok=True)
            return True
    except Exception as e:
        print(f"[✗] {fn} Error during sanity check: {e}")
        return False


def jadxDownload() -> bool:
    """Download JADX release zip with animated progress."""
    try:
        installer_path = installerFolder / "jadx-1.5.6.zip"
        print(f"[*] Downloading JADX from: {jadxUrl}")
        return download_with_progress(
            jadxUrl,
            installer_path,
            description="Downloading JADX"
        )
    except Exception as e:
        print(f"[✗] {fn} Download error: {e}")
        return False


def jadxSetup() -> bool:
    """Extract JADX zip and set executable permissions on jadx scripts."""
    source = installerFolder / "jadx-1.5.6.zip"
    if not source.exists():
        print(f"[✗] {fn}: Installer archive not found at {source}")
        return False

    try:
        with Spinner("Extracting JADX archive..."):
            with zipfile.ZipFile(source, "r") as zip_ref:
                zip_ref.extractall(jadxFolder)

        # Set executable bit on scripts in bin/
        bin_dir = jadxFolder / "bin"
        if bin_dir.exists():
            for item in bin_dir.iterdir():
                if item.is_file() and not item.name.endswith(".bat"):
                    item.chmod(item.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

        if jadxBin.exists():
            print(f"[✓] JADX binary located at {jadxBin}")
            return True
        else:
            print(f"[✗] {fn}: JADX binary not found at {jadxBin}")
            return False

    except Exception as e:
        print(f"[✗] {fn} Extraction error: {e}")
        return False
