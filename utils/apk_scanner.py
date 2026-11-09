"""utils/apk_scanner.py

Runs BetterLeaks secret scanner on a target codebase directory.
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from utils.config import betterLeaksBin, tempFolder, get_betterleaks_executable
from utils.animation import run_process_with_spinner

fn = "utils/apk_scanner.py"


def format_scan_summary(data: Dict[str, Any]) -> None:
    """Print a clean summary of scan findings to stdout."""
    findings = data.get("findings", [])
    scan_meta = data.get("scan", {})
    num_findings = scan_meta.get("num_findings", len(findings))

    print("\n" + "=" * 70)
    print("                      SCAN RESULTS SUMMARY")
    print("=" * 70)

    if num_findings == 0:
        print("\033[92m[✓] No secrets or leaks detected!\033[0m")
    else:
        print(f"\033[91m[!] Detected {num_findings} potential secret(s) / leak(s)!\033[0m\n")
        for i, item in enumerate(findings, 1):
            rule_id = item.get("rule_id", item.get("rule", "Unknown Rule"))
            desc = item.get("description", "")
            loc = item.get("location", {})
            target = loc.get("path", item.get("target", item.get("file", "Unknown Target")))
            line = loc.get("start_line", item.get("line", "?"))
            confidence = item.get("confidence", "N/A")
            severity = item.get("severity", "N/A")

            match_obj = item.get("match", {})
            if isinstance(match_obj, dict):
                secret = match_obj.get("value", match_obj.get("full", "<redacted>"))
            else:
                secret = item.get("secret", "<redacted>")

            print(f"  [{i}] Rule: \033[1;33m{rule_id}\033[0m")
            if desc:
                print(f"      Description: {desc}")
            print(f"      Location:    {target}:{line}")
            print(f"      Confidence:  {confidence} | Severity: {severity}")
            if secret:
                print(f"      Secret:      \033[31m{secret}\033[0m")
            print("-" * 70)

    # Print scan metrics if available
    if scan_meta:
        bytes_scanned = scan_meta.get("bytes_scanned", 0)
        started = scan_meta.get("started", "")
        finished = scan_meta.get("finished", "")
        print(f"Scanned bytes: {bytes_scanned:,} bytes")
        if started and finished:
            print(f"Scan duration: {started} -> {finished}")
    print("=" * 70 + "\n")


def scan_directory(
    target_dir: str | Path,
    output_json_path: Optional[str | Path] = None
) -> Optional[Dict[str, Any]]:
    """Scan a directory for secrets using BetterLeaks with an animated spinner.

    Args:
        target_dir: Path to directory containing source/decompiled code.
        output_json_path: Optional path where JSON results will be saved.

    Returns:
        Parsed JSON dictionary of findings, or None if scan failed.
    """
    target = Path(target_dir).resolve()
    if not target.exists():
        print(f"[✗] {fn}: Target directory does not exist: {target}")
        return None

    if not target.is_dir():
        print(f"[✗] {fn}: Target is not a directory: {target}")
        return None

    bl_bin = get_betterleaks_executable()
    if not bl_bin.exists() and not shutil.which("betterleaks"):
        print(f"[✗] {fn}: BetterLeaks binary not found at {bl_bin}. Please run 'python3 apkbully.py setup' first.")
        return None

    # Determine output file path
    if output_json_path:
        out_file = Path(output_json_path).resolve()
        out_file.parent.mkdir(parents=True, exist_ok=True)
    else:
        tempFolder.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_file = tempFolder / f"scan_{timestamp}.json"

    cmd = [
        str(bl_bin),
        "filesystem",
        str(target),
        "-o", str(out_file)
    ]

    print(f"[*] Starting BetterLeaks scan on: {target}")
    returncode, stdout, stderr = run_process_with_spinner(
        cmd,
        description=f"Scanning {target.name} for secrets"
    )

    # Note: BetterLeaks returns exit code 0 (no leaks) or 1 (leaks found).
    # Both are successful scans! Any other code is a crash/failure.
    if returncode not in (0, 1):
        print(f"[✗] {fn}: BetterLeaks exited with unexpected error code {returncode}.")
        if stderr:
            print(f"[stderr] {stderr.strip()[:500]}")
        return None

    if not out_file.exists():
        print(f"[✗] {fn}: Expected output JSON was not generated at {out_file}.")
        return None

    try:
        with open(out_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        format_scan_summary(data)
        print(f"[✓] Full scan report written to: {out_file}")
        return data

    except Exception as e:
        print(f"[✗] {fn}: Failed to parse JSON findings from {out_file}: {e}")
        return None
