"""utils/animation.py

Terminal animations and progress feedback using Python while loops.
Provides:
  - Spinner: Threaded spinner context manager / controller with while loop
  - download_with_progress: Streaming HTTP download with animated progress while loop
  - run_process_with_spinner: Subprocess execution with live animated while loop
"""

import itertools
import os
import sys
import time
import threading
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional, Tuple, Dict, Any


class Spinner:
    """A terminal loading spinner using a Python while loop."""

    FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def __init__(self, message: str = "Loading"):
        self.message = message
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._start_time = 0.0

    def _spin(self) -> None:
        idx = 0
        while self._running:
            elapsed = time.time() - self._start_time
            frame = self.FRAMES[idx % len(self.FRAMES)]
            line = f"\r\033[K\033[36m{frame}\033[0m {self.message} \033[90m({elapsed:.1f}s)\033[0m"
            sys.stdout.write(line)
            sys.stdout.flush()
            time.sleep(0.08)
            idx += 1

    def start(self) -> "Spinner":
        if not self._running:
            self._running = True
            self._start_time = time.time()
            self._thread = threading.Thread(target=self._spin, daemon=True)
            self._thread.start()
        return self

    def stop(self, success: bool = True, final_message: Optional[str] = None) -> None:
        if self._running:
            self._running = False
            if self._thread and self._thread.is_alive():
                self._thread.join(timeout=0.3)
            elapsed = time.time() - self._start_time
            symbol = "\033[92m[✓]\033[0m" if success else "\033[91m[✗]\033[0m"
            msg = final_message or self.message
            sys.stdout.write(f"\r\033[K{symbol} {msg} \033[90m({elapsed:.1f}s)\033[0m\n")
            sys.stdout.flush()

    def update_message(self, new_message: str) -> None:
        self.message = new_message

    def __enter__(self) -> "Spinner":
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.stop(success=(exc_type is None))


def format_bytes(bytes_count: float) -> str:
    """Format bytes to human readable string (KB, MB, GB)."""
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_count < 1024.0 or unit == "GB":
            return f"{bytes_count:.1f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.1f} B"


def download_with_progress(url: str, dest_path: Path, description: str = "Downloading") -> bool:
    """Download a remote file showing an animated progress bar using a Python while loop."""
    dest_path = Path(dest_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = dest_path.with_suffix(dest_path.suffix + ".part")

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "APKBully/1.0 (Linux x86_64)"}
    )

    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    idx = 0
    start_time = time.time()

    try:
        with urllib.request.urlopen(req, timeout=60) as response, open(temp_path, "wb") as out_file:
            total_size_header = response.headers.get("Content-Length")
            total_size = int(total_size_header) if total_size_header else 0
            downloaded = 0
            block_size = 64 * 1024  # 64 KB chunks

            # Python while loop for streaming and displaying download animation
            while True:
                chunk = response.read(block_size)
                if not chunk:
                    break
                out_file.write(chunk)
                downloaded += len(chunk)
                idx += 1

                elapsed = time.time() - start_time
                speed = downloaded / elapsed if elapsed > 0 else 0
                frame = frames[idx % len(frames)]

                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    status_line = (
                        f"\r\033[K\033[36m{frame}\033[0m {description} "
                        f"[{format_bytes(downloaded)} / {format_bytes(total_size)}] "
                        f"\033[33m{percent:.1f}%\033[0m "
                        f"\033[90m({format_bytes(speed)}/s)\033[0m"
                    )
                else:
                    status_line = (
                        f"\r\033[K\033[36m{frame}\033[0m {description} "
                        f"[{format_bytes(downloaded)}] "
                        f"\033[90m({format_bytes(speed)}/s)\033[0m"
                    )

                sys.stdout.write(status_line)
                sys.stdout.flush()

        temp_path.replace(dest_path)
        total_time = time.time() - start_time
        sys.stdout.write(
            f"\r\033[K\033[92m[✓]\033[0m {description} "
            f"completed ({format_bytes(dest_path.stat().st_size)} in {total_time:.1f}s)\n"
        )
        sys.stdout.flush()
        return True

    except Exception as e:
        if temp_path.exists():
            temp_path.unlink()
        sys.stdout.write(f"\r\033[K\033[91m[✗]\033[0m {description} failed: {e}\n")
        sys.stdout.flush()
        return False


def run_process_with_spinner(
    cmd: list,
    description: str = "Processing",
    env: Optional[Dict[str, str]] = None,
    cwd: Optional[str] = None
) -> Tuple[int, str, str]:
    """Execute a subprocess while displaying an animated spinner using a Python while loop."""
    import subprocess

    start_time = time.time()
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    idx = 0

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
            cwd=cwd
        )

        # Python while loop to show animated progress until subprocess finishes
        while proc.poll() is None:
            elapsed = time.time() - start_time
            frame = frames[idx % len(frames)]
            sys.stdout.write(
                f"\r\033[K\033[36m{frame}\033[0m {description}... \033[90m({elapsed:.1f}s)\033[0m"
            )
            sys.stdout.flush()
            time.sleep(0.08)
            idx += 1

        stdout, stderr = proc.communicate()
        elapsed = time.time() - start_time

        if proc.returncode == 0:
            sys.stdout.write(
                f"\r\033[K\033[92m[✓]\033[0m {description} finished \033[90m({elapsed:.1f}s)\033[0m\n"
            )
        else:
            sys.stdout.write(
                f"\r\033[K\033[93m[!]\033[0m {description} completed with code {proc.returncode} \033[90m({elapsed:.1f}s)\033[0m\n"
            )
        sys.stdout.flush()
        return proc.returncode, stdout, stderr

    except Exception as e:
        sys.stdout.write(f"\r\033[K\033[91m[✗]\033[0m {description} encountered error: {e}\n")
        sys.stdout.flush()
        return -1, "", str(e)
