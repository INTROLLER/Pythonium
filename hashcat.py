import subprocess
from pathlib import Path
import re
import time

BASE = Path(__file__).resolve().parent
HASHCAT_DIR = BASE / "hashcat-7.1.2"
HASHCAT_EXE = HASHCAT_DIR / "hashcat.exe"

hash_map = {
    "md5": "0",
    "sha256": "1400",
    "bcrypt": "3200"
}

def crack(hash, hashtype):
    cmd = [
        HASHCAT_EXE,
        "-m", hashtype,                  # hash type (MD5 example)
        "-a", "3",                  # attack mode
        hash,
        "?a?a?a?a?a?a",
        "--increment",
        "--potfile-disable",
        "--status",
        "--machine-readable"
    ]

    time_start = time.perf_counter()

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=HASHCAT_DIR
    )

    time_end = time.perf_counter()
    elapsed = time_end - time_start

    # Extract PROGRESS (current and total)
    clean = result.stdout.strip()
    clean = re.sub(r"\s+", " ", clean)
    m = re.search(rf"{re.escape(hash)}:(\S+)", clean)
    if m:
        print("Fully cracked! Time elapsed:", elapsed)
        password = m.group(1)
        return ([password, elapsed])
    else:
        print("Not fully cracked, skipping.")