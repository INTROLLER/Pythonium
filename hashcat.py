import subprocess
from pathlib import Path
import hashlib

BASE = Path(__file__).resolve().parent
HASHCAT_DIR = BASE / "hashcat-7.1.2"
HASHCAT_EXE = HASHCAT_DIR / "hashcat.exe"

hash = hashlib.md5(b"pass").hexdigest()

cmd = [
    HASHCAT_EXE,
    "-m", "0",                  # hash type (MD5 example)
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

print("Return code:", result.returncode)
print("STDOUT:\n", result.stdout)
print("STDERR:\n", result.stderr)