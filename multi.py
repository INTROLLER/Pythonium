# Bibliotek
import bcrypt
import time
import string
from hashlib import sha256, md5
import multiprocessing
import pickle


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


# Huvudprocess
if __name__ == '__main__':
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

  # Skicka in lösenord och kör brute force
  mode = int(input("Mode (Brute force <0>, Benchmark <1>: )"))
  hash_algo = hash_types[int(input("Hash type (sha256 <0>, bcrypt <1>, md5 <2>): "))]
  proc = int(input("Amount of processes to be used: "))

  if mode == 0:
    password = input("Password: ")
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

          save_results(hash_algo, "all", len(password), elapsed, "python")

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
