# Bibliotek
import bcrypt
import time
import string
import itertools
from hashlib import sha256

# Alla tecken
chars = string.printable
chars = chars.strip("\n")
chars = chars.strip()

# Hasha lösenord
def hash_password(password):
  hashed_password = sha256(password.encode('utf-8')).hexdigest()
  return hashed_password

# Ren brute force-attack (hash är inputlösenord, slice är antal tecken från chars som ska vara med)
def brute_force(hash, slice):
  global chars
  chars = chars[:slice]
  guesses = 0

  for i in range(1, 10):
    print("Testing all passwords with " + str(i) + " characters")
    combination_list = itertools.product(chars, repeat=i)

    for combination in combination_list:
      hashed = hash_password("".join(str(x) for x in combination))

      # Progress-uppdatering för att se till att datorn inte går sönder
      guesses += 1
      if guesses % 1000000 == 0:
        print("Currently guessed " + str(guesses) + " passwords")

      # Avbryt funktion om lösenord hittas
      if hashed == hash:
        print("Found password: " + "".join(str(x) for x in combination))
        return
      
  # Lösenord hittades inte
  print("Couldn't find password")

  
# Skicka in lösenord och kör brute force
password = input("Password: ")
hash = hash_password(password)
brute_force(hash, 94)