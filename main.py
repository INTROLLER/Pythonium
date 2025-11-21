import bcrypt
import time
import string
import itertools
from hashlib import sha256

chars = string.printable
chars = chars.strip("\n")
chars = chars.strip()

print(len(chars))
print(chars)

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


# password = input("Enter password: ")
list = itertools.product(chars, repeat=3)
for i in list:
  print("".join(i))