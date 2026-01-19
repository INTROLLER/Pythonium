# Bibliotek
import bcrypt
import time
import string
import itertools
from hashlib import sha256, md5

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
def brute_force(hash, chars):
  guesses = 0

  start = time.monotonic()
  for i in range(1, 10):
    print("Testing all passwords with " + str(i) + " characters")
    combination_list = itertools.product(chars, repeat=i)

    for combination in combination_list:
      candidate = "".join(combination)

      guesses += 1

      # Statusuppdatering för att se till att datorn inte går sönder
      if guesses % 1000000 == 0:
        print("Currently guessed " + str(guesses) + " passwords. Last guessed password: " + candidate)

      if hash_algo == "bcrypt":
        if bcrypt.checkpw(candidate.encode(), hash):
          end(candidate, guesses, start)
          return
      else:
        hashed = hash_password(candidate, hash_algo)
        if hashed == hash:
          end(candidate, guesses, start)
          return
      
  # Lösenord hittades inte
  print("Couldn't find password")

def end(candidate, guesses, start):
  print("Found password: " + candidate)
  print("Passwords attempted: " + str(guesses))
  end = time.monotonic()
  elapsed = end - start
  print("Elapsed time: " + str(elapsed) + " seconds")
  efficiency = guesses / elapsed
  print("Average guessing efficiency: " + str(efficiency) + " hashes/s")
  
# Skicka in lösenord och kör brute force
hash_algo = hash_types[int(input("Hash type (sha256 <0>, bcrypt <1>, md5 <2>): "))]
password = input("Password: ")
hash = hash_password(password, hash_algo)
brute_force(hash, chars[:94])