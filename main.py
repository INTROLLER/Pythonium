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

password = input("Enter password: ")
print(hash_password(password))
hash = hash_password("password")
print(hash)

hash = hash_password("password")
print(hash)