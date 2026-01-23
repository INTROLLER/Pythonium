import subprocess
from pathlib import Path
import re

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
        "-a", "3",                  # attack mode (dictionary)
        hash,
        "?a?a?a?a?a",
        "--increment",
        "--potfile-disable",
        "--status",
        "--machine-readable"
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=HASHCAT_DIR
    )

    exec_match = re.search(r'EXEC_RUNTIME\s+([\d\.]+)', result.stdout)
    exec_runtime = float(exec_match.group(1)) if exec_match else None

    # Extract PROGRESS (current and total)
    progress_match = re.search(r'PROGRESS\s+(\d+)\s+(\d+)', result.stdout)
    if progress_match:
        current, total = map(int, progress_match.groups())
        if current == total:
            print("Fully cracked! EXEC_RUNTIME:", exec_runtime)
        else:
            print("Not fully cracked, skipping.")
    else:
        print("PROGRESS info not found")

    return (result, exec_runtime)