"""utils/setup.py

Sets up the folder workspace and downloads required tools (BetterLeaks, JADX, JRE).
"""

import os
from datetime import datetime
from pathlib import Path
from utils.config import (
    folder,
    installerFolder,
    toolsFolder,
    betterLeakFolder,
    jadxFolder,
    jreFolder,
    tempFolder,
    markerFile,
    betterLeaksBin,
    jadxBin,
    jreJavaBin,
)
from utils.betterleaks_setup import blSanityCheck, blDownload, blSetup
from utils.jadx_setup import jadxSanityCheck, jadxDownload, jadxSetup
from utils.jre_installer import install_jre, check_java

fn = "utils/setup.py"


def checkAlreadyDone() -> bool:
    """Return True if setup was already performed and tools are in place."""
    if not markerFile.exists():
        return False
    # Verify that the essential binaries are present
    has_bl = betterLeaksBin.exists() and os.access(betterLeaksBin, os.X_OK)
    has_jadx = jadxBin.exists() and os.access(jadxBin, os.X_OK)
    has_java = check_java()
    return has_bl and has_jadx and has_java


def createAlreadyDone() -> None:
    """Create marker file signaling setup completion."""
    try:
        folder.mkdir(parents=True, exist_ok=True)
        with open(markerFile, "w") as f:
            f.write(f"Setup completed on: {datetime.now().isoformat()}\n")
    except Exception as e:
        print(f"[!] Warning: Could not write marker file: {e}")


def setupFolders() -> bool:
    """Create all required workspace and tool directories."""
    try:
        folder.mkdir(parents=True, exist_ok=True)
        installerFolder.mkdir(parents=True, exist_ok=True)
        toolsFolder.mkdir(parents=True, exist_ok=True)
        betterLeakFolder.mkdir(parents=True, exist_ok=True)
        jadxFolder.mkdir(parents=True, exist_ok=True)
        jreFolder.mkdir(parents=True, exist_ok=True)
        tempFolder.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"[✗] {fn} Directory creation error: {e}")
        return False


def setupTools(force: bool = False) -> bool:
    """Download and set up all tools: JRE, BetterLeaks, and JADX."""
    if not force and checkAlreadyDone():
        print("[✓] Setup already done. All tools are installed and verified.")
        return True

    try:
        print("\n=== [1/3] Setting up Java Runtime Environment (JRE) ===")
        if not install_jre():
            print(f"[✗] {fn}: Failed to set up Java Runtime Environment.")
            return False

        print("\n=== [2/3] Setting up BetterLeaks ===")
        if betterLeaksBin.exists() and os.access(betterLeaksBin, os.X_OK) and not force:
            print("[✓] BetterLeaks binary already installed.")
        else:
            if not (blSanityCheck() and blDownload() and blSetup()):
                print(f"[✗] {fn}: An error occurred while installing BetterLeaks.")
                return False

        print("\n=== [3/3] Setting up JADX ===")
        if jadxBin.exists() and os.access(jadxBin, os.X_OK) and not force:
            print("[✓] JADX binary already installed.")
        else:
            if not (jadxSanityCheck() and jadxDownload() and jadxSetup()):
                print(f"[✗] {fn}: An error occurred while installing JADX.")
                return False

        createAlreadyDone()
        print("\n[✓] APKBully setup completed successfully! All dependencies are installed.")
        return True

    except Exception as e:
        print(f"[✗] {fn} Unexpected error during tool setup: {e}")
        return False
