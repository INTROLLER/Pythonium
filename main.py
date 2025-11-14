import bcrypt
import time

def hash_password(password, rounds=12):
  salt = bcrypt.gensalt(rounds=rounds)
  hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
  return hashed_password

password = input("Enter password: ")
print(hash_password(password))
start = time.time()
hash = hash_password("password")
stop = time.time()
print(hash, stop - start)


start2 = time.time()
hash = hash_password("password", 4)
stop2 = time.time()
print(hash, stop2 - start2)
print((stop - start)/(stop2 - start2))
