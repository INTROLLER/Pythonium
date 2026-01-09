# Bibliotek
import bcrypt
import time
import string
import itertools
from hashlib import sha256, md5
import pickle
import random

# Alla tecken
chars = string.printable
chars = chars.strip("\n")
chars = chars.strip()

lowercase = string.ascii_lowercase
uppercase = string.ascii_uppercase
digits = string.digits
special_characters = string.punctuation

hash_types = ["sha256", "bcrypt", "md5"]
hash_type = int()

# Hasha lösenord
def hash_password(password, algo):

  if algo == "sha256":
    hashed_password = sha256(password.encode('utf-8')).hexdigest()
  elif algo == "bcrypt":
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=4))
  elif algo == "md5":
    hashed_password = md5(password.encode('utf-8')).hexdigest()

  return hashed_password

# Ren brute force-attack (hash är inputlösenord, slice är antal tecken från chars som ska vara med)
def brute_force(hash, slice):
  global chars
  chars = chars[:slice]
  guesses = 0

  start = time.time()
  for i in range(1, 10):
    print("Testing all passwords with " + str(i) + " characters")
    combination_list = itertools.product(chars, repeat=i)
    interval = 0
    subtract = start

    for combination in combination_list:
      interval += time.time() - subtract
      subtract = time.time()
      candidate = "".join(str(x) for x in combination)

      guesses += 1

      # Statusuppdatering för att se till att datorn inte går sönder
      if interval >= 10:
        print("Currently guessed " + str(guesses) + " passwords")
        print("Last guessed password: " + candidate)
        interval = 0

      if hash_algo == "bcrypt":
        if bcrypt.checkpw(candidate.encode(), hash):
          end(combination, guesses, start)
          return
      else:
        hashed = hash_password("".join(str(x) for x in combination), hash_algo)
        if hashed == hash:
          end(combination, guesses, start)
          return
      
  # Lösenord hittades inte
  print("Couldn't find password")

def end(combination, guesses, start):
  print("Found password: " + "".join(str(x) for x in combination))
  print("Passwords attempted: " + str(guesses))
  end = time.time()
  elapsed = end - start
  data = []
  try:
    with open("benchmarks.pkl", "rb") as f:
      data = pickle.load(f)
  except:
    pass

  data.append((hash_algo, "all", len(password), elapsed, "python"))
  with open("benchmarks.pkl", "wb") as f:
    pickle.dump(data, f)
  print("Elapsed time: " + str(elapsed) + " seconds")
  
# Skicka in lösenord och kör brute force
#hash_algo = hash_types[int(input("Hash type (sha256 <0>, bcrypt <1>, md5 <2>): "))]

for i in range(15):
  hash_algo = random.choice(hash_types)
  password = ""
  length = random.randint(1, 2)
  for j in range(length):
    password += random.choice(chars)
  print("Password: " + password)
  hash = hash_password(password, hash_algo)
  brute_force(hash, 94)


""" password = input("Password: ")
  hash = hash_password(password, hash_algo)
  brute_force(hash, 94) """