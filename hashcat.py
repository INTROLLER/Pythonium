import subprocess
from pathlib import Path

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
        "--potfile-disable"
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=HASHCAT_DIR
    )

    return result