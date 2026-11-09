#!/usr/bin/env python3
"""APKBully - Automated APK decompilation and secret scanner."""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

from utils.setup import setupFolders, setupTools
from utils.apk_decompiler import decompile_apk
from utils.apk_scanner import scan_directory

BANNER = r"""
    ___    ____  __ __ ____        ____      
   /   |  / __ \/ //_// __ )__  __/ / /_  __ 
  / /| | / /_/ / ,<  / __  / / / / / / / / / 
 / ___ |/ ____/ /| |/ /_/ / /_/ / / / /_/ /  
/_/  |_/_/   /_/ |_/_____/\__,_/_/_/\__, /   
                                   /____/    
   APK Decompiler & Secret Leak Scanner
"""


def get_default_output_path() -> Path:
    """Generate default output path with current timestamp (hhmmss)."""
    timestamp = datetime.now().strftime("%H%M%S")
    return Path.cwd() / f"output_{timestamp}.json"


def resolve_output_path(user_output: str | None) -> Path:
    """Validate and resolve output path.

    If output was specified, verify it has a .json extension.
    If not, inform the user and fall back to the default timestamped json file.
    """
    default_path = get_default_output_path()

    if not user_output:
        return default_path

    out_path = Path(user_output)
    if out_path.suffix.lower() != ".json":
        print(
            f"[!] Warning: Specified output '{user_output}' does not end with '.json'. "
            f"Ignoring custom output and using default: {default_path.name}"
        )
        return default_path

    return out_path.resolve()


def main():
    print(BANNER)
    parser = argparse.ArgumentParser(
        description="APKBully: Automated APK decompilation and secret leak scanner.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python3 apkbully.py setup
  python3 apkbully.py scan -i app.apk
  python3 apkbully.py scan -i app.apk -o findings.json
  python3 apkbully.py direct-scan -i /path/to/decompiled_src -o results.json
        """
    )
    parser.add_argument(
        "option",
        choices=["setup", "scan", "direct-scan"],
        help="Action to perform: 'setup' to install dependencies, 'scan' to decompile and scan an APK, or 'direct-scan' to scan an already decompiled folder."
    )
    parser.add_argument(
        "-i", "--input",
        dest="input",
        help="Point to *.apk file (for scan) or decompiled code base directory (for direct-scan)"
    )
    parser.add_argument(
        "-o", "--output",
        dest="output",
        default=None,
        help="Path to output JSON report (e.g. results.json). Must end in .json; defaults to output_<hhmmss>.json"
    )
    parser.add_argument(
        "-f", "--force",
        dest="force",
        action="store_true",
        help="Force re-setup even if already configured"
    )

    args = parser.parse_args()

    # Option 1: SETUP
    if args.option == "setup":
        print("[*] Running APKBully environment and tool setup...")
        if setupFolders() and setupTools(force=args.force):
            print("[✓] Setup completed successfully!")
            sys.exit(0)
        else:
            print("[err] An error occurred during setup. Please check the logs above.")
            sys.exit(1)

    # Option 2: SCAN or DIRECT-SCAN
    elif args.option in ("scan", "direct-scan"):
        # Validate that input argument was provided
        if not args.input:
            print(f"[err] Error: Input (-i / --input) is required for '{args.option}'.")
            print("Usage: python3 apkbully.py " + args.option + " -i <path>")
            sys.exit(1)

        input_path = Path(args.input).resolve()
        if not input_path.exists():
            print(f"[err] Error: Specified input does not exist: {input_path}")
            sys.exit(1)

        # Resolve output destination
        final_output = resolve_output_path(args.output)
        print(f"[*] Target output report: {final_output}")

        src_to_scan: Path | None = None

        if args.option == "scan":
            # Input must be an APK file
            if not input_path.is_file():
                print(f"[err] Error: Input for 'scan' must be an APK file: {input_path}")
                sys.exit(1)

            print(f"[*] Starting decompilation of APK: {input_path.name}")
            decompiled_dir = decompile_apk(input_path)
            if not decompiled_dir:
                print("[err] Decompilation step failed. Aborting scan.")
                sys.exit(1)

            src_to_scan = decompiled_dir

        elif args.option == "direct-scan":
            # Input must be a directory containing source / decompiled files
            if not input_path.is_dir():
                print(f"[err] Error: Input for 'direct-scan' must be a directory: {input_path}")
                sys.exit(1)

            print(f"[*] Direct scan selected. Skipping decompilation.")
            src_to_scan = input_path

        # Run BetterLeaks scanner on src_to_scan
        print(f"[*] Initiating secret detection on: {src_to_scan}")
        scan_results = scan_directory(src_to_scan, output_json_path=final_output)

        if scan_results is None:
            print("[err] Secret scanning encountered an error.")
            sys.exit(1)

        print(f"[✓] Scan process finished successfully!")
        sys.exit(0)

    else:
        print(f"[err] Unknown option '{args.option}' was passed. Check --help menu.")
        sys.exit(1)


if __name__ == '__main__':
    main()
