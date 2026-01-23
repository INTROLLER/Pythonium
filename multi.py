# Bibliotek
import bcrypt
import time
import string
from hashlib import sha256, md5
import multiprocessing
import pickle
import random
import hashcat

# Alla tecken
chars = string.printable
chars = chars.strip("\n")
chars = chars.strip()
chars = random.sample(chars, len(chars))

lowercase = string.ascii_lowercase
uppercase = string.ascii_uppercase
digits = string.digits
special_characters = string.punctuation

hash_types = ["sha256", "bcrypt", "md5"]
hash_type = int()


def hash_password(password, algo):
  """Hashar lösenord som skickas in."""
  if algo == "sha256":
    hashed_password = sha256(password.encode('utf-8')).hexdigest()
  elif algo == "bcrypt":
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=4))
  elif algo == "md5":
    hashed_password = md5(password.encode('utf-8')).hexdigest()

  return hashed_password


def index_to_password(index, length, chars, vals):
  """Omvandlar tal till lösenordskombinationer."""
  passwd = []
  for i in reversed(range(length)):
    val = vals[i]
    passwd.append(chars[index // val])
    index = index % val

  return "".join(passwd)


def brute_force(hash, chars, indexes, len, hash_algo, efound, qresult):
  """
  Utför simulation av ren brute force-attack i intervallet indexes.

  Använder efound och qresult för att synka med huvudprocess.
  """
  vals = []
  for i in range(10):
    vals.append(94 ** i)

  for i in range(indexes[0], indexes[1]):
    if i % 100 == 0:
      if efound.is_set():
        return

    candidate = index_to_password(i, len, chars, vals)

    if hash_algo == "bcrypt":
      if bcrypt.checkpw(candidate.encode(), hash):
        qresult.put(candidate)
        efound.set()
        return
    else:
      hashed = hash_password(candidate, hash_algo)
      if hashed == hash:
        qresult.put(candidate)
        efound.set()
        return


def benchmark(str, hash_algo, qcounter):
  """Ren benchmark för hashningshastighet, ger teoretisk maxhastighet."""
  count = 0
  time_start = time.monotonic()
  if hash_algo == 1:
    iterations = 10
  else:
    iterations = 10000

  while True:
    hash_password(str, hash_algo)
    count += 1

    if count % iterations == 0:
      if time.monotonic() - time_start >= 10:
        qcounter.put(count)
        break


def save_results(algo, charset, length, time, tool):
  data = []
  try:
    with open("benchmarks.pkl", "rb") as f:
      data = pickle.load(f)
  except:
    pass

  data.append((algo, charset, length, time, tool))

  with open("benchmarks.pkl", "wb") as f:
    pickle.dump(data, f)

def get_color_weight(password):
  color_weight = 0.0

  if not set(password).isdisjoint(special_characters):
    color_weight += 2.0
  if not set(password).isdisjoint(digits):
    color_weight += 0.5
  if not set(password).isdisjoint(uppercase):
    color_weight += 1.0
  if not set(password).isdisjoint(lowercase):
    color_weight += 1.0

  return color_weight

def generate_password(length, charset):
  password = ""
  for i in range(length):
    password += random.choice(charset)

  return password

def main(mode, hash_algo, proc, password):
  if mode == 0:
    hash = hash_password(password, hash_algo)
    print("Using " + str(proc) + " processes to brute force...")

    base = len(chars)
    efound = multiprocessing.Event()
    qresult = multiprocessing.Queue()

    time_start = time.monotonic()

    for i in range(1, 10):
      if(efound.is_set()):
        break

      print("Trying passwords with length " + str(i))
      total = base ** i
      chunk = total // proc
      processes = []
      ranges = []
      for j in range(proc):
        first = chunk*j
        if j == 7:
          last = total
        else:
          last = chunk*(j+1)
        ranges.append([first, last])

      for k in range(proc):
        p = multiprocessing.Process(target=brute_force, args=(hash, chars, ranges[k], i, hash_algo, efound, qresult))
        p.start()
        processes.append(p)

      while True:
        if not qresult.empty():
          guess = qresult.get()
          time_end = time.monotonic()
          elapsed = time_end - time_start
          print("Found password: " + guess)
          print("Elapsed time: " + str(elapsed))

          color_weight = get_color_weight(password)

          save_results(hash_algo, color_weight, len(password), elapsed, "python")

          for p in processes:
            # Stäng ned allt
            p.terminate()
          break

        if all(not p.is_alive() for p in processes):
          break

        time.sleep(0.01)
  else:
    print("Benchmarking using " + str(proc) + " processes...")
    bstring = "AAAAA"
    processes = []
    qcounter = multiprocessing.Queue()
    total = 0

    for i in range(proc):
      p = multiprocessing.Process(target=benchmark, args=(bstring, hash_algo, qcounter))
      p.start()
      processes.append(p)

    time.sleep(11)

    for p in processes:
      p.terminate()

    while not qcounter.empty():
      total += qcounter.get()

    efficiency = total / 10
    print("Estimated pure hashing efficiency: " + str(efficiency) + " H/s")

def hashcat_main(hash, hash_algo):
  start = time.monotonic()
  result = hashcat.crack(hash, hashcat.hash_map[hash_algo])
  end = time.monotonic()
  elapsed = end - start
  print(result.stdout)
  color_weight = get_color_weight(password)
  save_results(hash_algo, color_weight, len(password), elapsed, "hashcat")

# Huvudprocess
if __name__ == '__main__':
  # Skicka in lösenord och kör brute force
  mode = int(input("Mode (Brute force <0>, Benchmark <1>: )"))
  enable_random = False
  length = None
  password = None
  iterate = False
  repeat = 1
  charset = ""
  tool = int(input("Tool (python <0>, hashcat <1>): "))
  if mode == 0:
    enable_random = bool(int(input("Use random password? (0/1): ")))
    if enable_random:
      length = int(input("Password length: "))
      if input("Use special characters? (0/1): ") == "1":
        charset += special_characters
      if input("Use digits? (0/1): ") == "1":
        charset += digits
      if input("Use uppercase? (0/1): ") == "1":
        charset += uppercase
      if input("Use lowercase? (0/1): ") == "1":
        charset += lowercase
      password = generate_password(length, charset)
      iterate = bool(int(input("Iterate through length? (0/1): ")))
      repeat = int(input("Repeat? (0/1): "))
      if repeat == 1:
        repeat = int(input("Repeat amount: "))
      else:
        repeat = 1
    else:
      password = input("Password: ")

    test_all_hashes = bool(int(input("Test all hashes? (0/1): ")))
    if not test_all_hashes:
      hash_algo = hash_types[int(input("Hash type (sha256 <0>, bcrypt <1>, md5 <2>): "))]
  else:
    hash_algo = hash_types[int(input("Hash type (sha256 <0>, bcrypt <1>, md5 <2>): "))]

  if tool == 0:
    proc = int(input("Amount of processes to be used: "))

  for j in range(repeat):
    if test_all_hashes and iterate:
      for hashtype in hash_types:
        for i in range(1, length + 1):
          hash = hash_password(password, hashtype)
          if tool == 0:
            main(mode, hash, proc)
          else:
            hashcat_main(hash, hashtype)
    elif test_all_hashes:
      for hashtype in hash_types:
        hash = hash_password(password, hashtype)
        if tool == 0:
          main(mode, hash, proc)
        else:
          hashcat_main(hash, hashtype)
    elif iterate:
      for i in range(1, length + 1):
        hash = hash_password(password, hash_algo)
        if tool == 0:
          main(mode, hash, proc)
        else:
          hashcat_main(hash, hash_algo)
    else:
      hash = hash_password(password, hash_algo)
      if tool == 0:
        main(mode, hash, proc)
      else:
        hashcat_main(hash, hash_algo)