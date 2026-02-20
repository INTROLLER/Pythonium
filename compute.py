import pickle
import pprint

filename = "results/" + input("File name: ") + ".pkl"

tool_sort = input("What tool? (python <0>, hashcat <1>): ")
hash_sort = input("What hash? (md5 <0>, sha256 <1>, bcrypt <2>): ")
complexity_sort = input("What entropy? (Numbers only <0>, All characters <1>): ")

container = {
  1: [],
  2: [],
  3: [],
  4: [],
  5: [],
  6: []
}

with open(filename, "rb") as f:
  data = pickle.load(f)

for row in data:
  if row[5] == "python" and tool_sort == "1":
    continue
  if row[5] == "hashcat" and tool_sort == "0":
    continue
  if row[1] == "md5" and hash_sort != "0":
    continue
  if row[1] == "sha256" and hash_sort != "1":
    continue
  if row[1] == "bcrypt" and hash_sort != "2":
    continue
  if row[2] == 4.5 and complexity_sort != "1":
    continue
  if row[2] == 0 and complexity_sort != "0":
    continue

  container[row[3]].append(row[4])

pprint.pp(container)


for i in range(1, 7):
  if len(container[i]) == 0:
    continue
  
  print(f"Average for {i}: {round(sum(container[i]) / len(container[i]), 4)}")