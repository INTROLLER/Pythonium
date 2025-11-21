import bcrypt
import time
import string
import itertools
from hashlib import sha256

chars = string.printable
chars = chars.strip("\n")
chars = chars.strip()

def hash_password(password):
  hashed_password = sha256(password.encode('utf-8')).hexdigest()
  return hashed_password

def brute_force(hash, slice, charcount):
  global chars
  chars = chars[:slice]
  guess = []
  for i in range(charcount):
    guess.append(chars[0])
  print("".join(str(x) for x in guess))


password = input("Password: ")
hash = hash_password(password)
combination_list = itertools.product(chars, repeat=4)

for combination in combination_list:
  hashed = hash_password("".join(str(x) for x in combination))
  if hashed == hash:
    print("Found password: " + "".join(str(x) for x in combination))
    break