"""utils/betterleaks_setup.py

Downloads and sets up BetterLeaks scanner binary.
"""

import os
import stat
import subprocess
import tarfile
from pathlib import Path
from utils.config import folder, installerFolder, betterLeakFolder, betterLeaksBin, betterLeaksUrl
from utils.animation import download_with_progress, Spinner

fn = "utils/betterleaks_setup.py"


def blSanityCheck() -> bool:
    """Check if base directory exists."""
    try:
        if folder.is_dir() and installerFolder.is_dir() and betterLeakFolder.is_dir():
            print(f"[✓] {fn}: Required folders exist.")
            return True
        else:
            print(f"[✗] {fn}: Base directories missing. Running directory setup...")
            folder.mkdir(parents=True, exist_ok=True)
            installerFolder.mkdir(parents=True, exist_ok=True)
            betterLeakFolder.mkdir(parents=True, exist_ok=True)
            return True
    except Exception as e:
        print(f"[✗] {fn} Error during sanity check: {e}")
        return False


def blDownload() -> bool:
    """Download BetterLeaks release archive with animated progress."""
    try:
        installer_path = installerFolder / "betterleaks.tar.gz"
        print(f"[*] Downloading BetterLeaks from: {betterLeaksUrl}")
        return download_with_progress(
            betterLeaksUrl,
            installer_path,
            description="Downloading BetterLeaks"
        )
    except Exception as e:
        print(f"[✗] {fn} Download error: {e}")
        return False


def blSetup() -> bool:
    """Extract BetterLeaks archive and set executable permissions."""
    source = installerFolder / "betterleaks.tar.gz"
    if not source.exists():
        print(f"[✗] {fn}: Installer archive not found at {source}")
        return False

    try:
        with Spinner("Extracting BetterLeaks archive..."):
            with tarfile.open(source, "r:gz") as tar:
                tar.extractall(path=betterLeakFolder)

        # Ensure executable permissions on betterleaks binary
        if betterLeaksBin.exists():
            current_mode = betterLeaksBin.stat().st_mode
            betterLeaksBin.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            
            # Quick verification
            res = subprocess.run([str(betterLeaksBin), "version"], capture_output=True, text=True)
            if res.returncode == 0:
                print(f"[✓] BetterLeaks verified: {res.stdout.strip()}")
                return True
            else:
                print(f"[✗] BetterLeaks verification failed: {res.stderr.strip()}")
                return False
        else:
            print(f"[✗] {fn}: Binary not found after extraction at {betterLeaksBin}")
            return False

    except Exception as e:
        print(f"[✗] {fn} Extraction error: {e}")
        return False
