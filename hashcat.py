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
        str(HASHCAT_EXE),
        "-m", hashtype,
        "-a", "3",
        hash,
        "?a?a?a?a?a",
        "--increment",
        "--potfile-disable",
        "--status",
        "--machine-readable",
        "--quiet",
    ]

    proc = subprocess.Popen(
        cmd,
        cwd=HASHCAT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        bufsize=1,
    )

    exec_runtime = None
    cracked = False

    for line in proc.stdout:
        # STATUS 6 = cracked, STATUS 5 = exhausted
        if not line.startswith("STATUS"):
            continue

        parts = line.split()

        status = parts[1]
        if status == "6":
            cracked = True

            # machine-readable fields are fixed-position
            # EXEC_RUNTIME index is stable
            exec_runtime = float(parts[parts.index("EXEC_RUNTIME") + 1])
            proc.terminate()
            break

    proc.wait()

    return (proc, exec_runtime)