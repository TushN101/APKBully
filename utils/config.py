from pathlib import Path
import os
import shutil

# Base directory for APKBully
folder = Path.home() / ".apkbully"
installerFolder = folder / "installers"
toolsFolder = folder / "tools"
betterLeakFolder = toolsFolder / "betterleak-bin"
jadxFolder = toolsFolder / "jadx-bin"
jreFolder = toolsFolder / "jre-bin"
tempFolder = folder / "temp"
# Backward-compatibility alias for original spelling
tempFodler = tempFolder
markerFile = folder / ".setup_done"

# Download URLs
betterLeaksUrl = "https://github.com/betterleaks/betterleaks/releases/download/v2.0.0-rc.7/betterleaks_2.0.0-rc.7_linux_x64.tar.gz"
jadxUrl = "https://github.com/skylot/jadx/releases/download/v1.5.6/jadx-1.5.6.zip"
jreUrl = "https://api.adoptium.net/v3/binary/latest/17/ga/linux/x64/jre/hotspot/normal/eclipse"

# Tool Binary Paths
betterLeaksBin = betterLeakFolder / "betterleaks"
jadxBin = jadxFolder / "bin" / "jadx"
jreJavaBin = jreFolder / "bin" / "java"


def get_java_executable() -> str:
    """Return path to java executable: system java if available, else portable jreJavaBin."""
    system_java = shutil.which("java")
    if system_java:
        return system_java
    if jreJavaBin.exists() and os.access(jreJavaBin, os.X_OK):
        return str(jreJavaBin)
    return "java"


def get_jadx_executable() -> Path:
    """Return path to jadx executable."""
    system_jadx = shutil.which("jadx")
    if system_jadx:
        return Path(system_jadx)
    return jadxBin


def get_betterleaks_executable() -> Path:
    """Return path to betterleaks executable."""
    system_bl = shutil.which("betterleaks")
    if system_bl:
        return Path(system_bl)
    return betterLeaksBin
