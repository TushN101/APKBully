"""utils/apk_decompiler.py

Decompiles an APK using JADX into a destination or temp folder.
"""

import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Optional
from utils.config import jadxBin, tempFolder, jreFolder, get_jadx_executable, get_java_executable
from utils.animation import run_process_with_spinner

fn = "utils/apk_decompiler.py"


def decompile_apk(apk_path: str | Path, output_dir: Optional[str | Path] = None) -> Optional[Path]:
    """Decompile an APK file using JADX with an animated loading spinner.

    Args:
        apk_path: Path to the *.apk file.
        output_dir: Optional destination folder. Defaults to a subfolder in tempFolder.

    Returns:
        Path to the decompiled folder, or None if decompilation failed.
    """
    apk_file = Path(apk_path).resolve()
    if not apk_file.exists():
        print(f"[✗] {fn}: APK file does not exist: {apk_file}")
        return None

    if not apk_file.is_file():
        print(f"[✗] {fn}: Path is not a file: {apk_file}")
        return None

    if not zipfile.is_zipfile(apk_file):
        print(f"[✗] {fn}: Specified file '{apk_file.name}' is not a valid APK or zip archive.")
        return None

    jadx_path = get_jadx_executable()
    if not jadx_path.exists() and not shutil.which("jadx"):
        print(f"[✗] {fn}: JADX binary not found at {jadx_path}. Please run 'python3 apkbully.py setup' first.")
        return None

    # Prepare output directory
    if output_dir:
        out_path = Path(output_dir).resolve()
    else:
        tempFolder.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = tempFolder / f"decompiled_{apk_file.stem}_{timestamp}"

    out_path.mkdir(parents=True, exist_ok=True)

    # Configure environment for JADX (ensure Java is in PATH / JAVA_HOME)
    env = os.environ.copy()
    jre_bin_dir = jreFolder / "bin"
    if jre_bin_dir.exists():
        env["JAVA_HOME"] = str(jreFolder)
        env["PATH"] = f"{jre_bin_dir}:{env.get('PATH', '')}"

    cmd = [
        str(jadx_path),
        "-d", str(out_path),
        str(apk_file),
    ]

    print(f"[*] Decompiling '{apk_file.name}' into: {out_path}")
    returncode, stdout, stderr = run_process_with_spinner(
        cmd,
        description=f"Decompiling {apk_file.name}",
        env=env
    )

    # JADX can return warnings with code 0 or partial with non-zero
    # Check if files were generated in output folder
    has_files = any(out_path.iterdir()) if out_path.exists() else False

    if returncode == 0 or has_files:
        print(f"[✓] Decompilation successful: {out_path}")
        return out_path
    else:
        print(f"[✗] {fn}: Decompilation failed (code {returncode}).")
        if stderr:
            print(f"[stderr] {stderr.strip()[:500]}")
        return None
