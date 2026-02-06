import subprocess
from pathlib import Path
import re
import time

BASE = Path(__file__).resolve().parent
HASHCAT_DIR = BASE / "hashcat-7.1.2"
HASHCAT_EXE = HASHCAT_DIR / "hashcat.exe"
out_file = HASHCAT_DIR / "cracked.txt"

hash_map = {
    "md5": "0",
    "sha256": "1400",
    "bcrypt": "3200"
}

def crack(hash, hashtype):
    if out_file.exists():
        out_file.unlink()

    cmd = [
        HASHCAT_EXE,
        "-m", hashtype,                  # hash type (MD5 example)
        "-a", "3",                  # attack mode
        hash,
        "?a?a?a?a?a?a",
        "--increment",
        "--potfile-disable",
        "-o", str(out_file),
        "--quiet"
    ]

    time_start = time.perf_counter()

    subprocess.run(
        cmd,
        cwd=HASHCAT_DIR
    )

    time_end = time.perf_counter()
    elapsed = time_end - time_start

    if out_file.exists() and out_file.stat().st_size > 0:
        line = out_file.read_text().strip()
        _, password = line.split(":", 1)
        return password, elapsed

    return None, None