"""utils/jre_installer.py

Ensures Java Runtime Environment (JRE) is available for JADX.
Checks system Java first, tries apt if sudo is available, and falls back to
downloading a portable OpenJDK JRE 17 binary for non-root / standalone setups.
"""

import os
import shutil
import stat
import subprocess
import tarfile
from pathlib import Path
from utils.config import folder, installerFolder, jreFolder, jreJavaBin, jreUrl, get_java_executable
from utils.animation import download_with_progress, Spinner

fn = "utils/jre_installer.py"


def check_java() -> bool:
    """Check if a working Java runtime is available."""
    java_bin = get_java_executable()
    try:
        res = subprocess.run([java_bin, "-version"], capture_output=True, text=True)
        if res.returncode == 0:
            first_line = (res.stderr or res.stdout).splitlines()[0]
            print(f"[✓] Java runtime detected ({java_bin}): {first_line}")
            return True
    except Exception:
        pass
    return False


def _try_apt_install() -> bool:
    """Attempt system package manager install if sudo is available without password."""
    try:
        # Check if passwordless sudo is available
        check_sudo = subprocess.run(["sudo", "-n", "true"], capture_output=True)
        if check_sudo.returncode == 0:
            print("[*] Installing default-jre via apt...")
            res = subprocess.run(
                ["sudo", "-n", "apt-get", "install", "-y", "default-jre"],
                capture_output=True,
                text=True
            )
            if res.returncode == 0 and check_java():
                print("[✓] Successfully installed default-jre via apt.")
                return True
    except Exception:
        pass
    return False


def _download_portable_jre() -> bool:
    """Download and set up portable OpenJDK Temurin JRE 17."""
    print("[*] Setting up portable OpenJDK 17 runtime (no root privileges required)...")
    installer_path = installerFolder / "jre17.tar.gz"
    
    if not download_with_progress(jreUrl, installer_path, description="Downloading OpenJDK 17 JRE"):
        return False

    try:
        with Spinner("Extracting OpenJDK runtime..."):
            jreFolder.mkdir(parents=True, exist_ok=True)
            with tarfile.open(installer_path, "r:gz") as tar:
                members = tar.getmembers()
                # Find common top-level directory (e.g. jdk-17.0.21+9-jre/)
                top_prefix = ""
                first_names = [m.name for m in members if "/" in m.name]
                if first_names:
                    top_prefix = first_names[0].split("/")[0] + "/"

                for member in members:
                    if top_prefix and member.name.startswith(top_prefix):
                        member.name = member.name[len(top_prefix):]
                    if member.name:
                        tar.extract(member, path=jreFolder)

        # Mark all files in bin/ as executable
        bin_dir = jreFolder / "bin"
        if bin_dir.exists():
            for f in bin_dir.iterdir():
                if f.is_file():
                    f.chmod(f.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

        if jreJavaBin.exists():
            res = subprocess.run([str(jreJavaBin), "-version"], capture_output=True, text=True)
            if res.returncode == 0:
                first_line = (res.stderr or res.stdout).splitlines()[0]
                print(f"[✓] Portable JRE verified ({jreJavaBin}): {first_line}")
                return True

        print(f"[✗] Failed to verify portable JRE binary at {jreJavaBin}")
        return False

    except Exception as e:
        print(f"[✗] JRE extraction error: {e}")
        return False


def install_jre() -> bool:
    """Main entrypoint to ensure JRE is installed and working."""
    if check_java():
        return True

    # Try apt if root/sudo is accessible
    if _try_apt_install():
        return True

    # Otherwise fallback to portable Temurin JRE
    return _download_portable_jre()
