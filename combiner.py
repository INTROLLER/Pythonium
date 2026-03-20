import pickle
import os

auto_mode = int(input("Auto mode? (0/1): "))

data = []

try:
    with open("results/all.pkl", "rb") as f:
        data.extend(pickle.load(f))
except:
    pass

if auto_mode == 1:
    all_files = os.listdir("results/")

    for file in all_files:
        if file != "all.pkl":
            filename = "results/" + file

            with open(filename, "rb") as f:
                data.extend(pickle.load(f))

else:
    filename = "results/" + input("File name: ") + ".pkl"

    with open(filename, "rb") as f:
        data.extend(pickle.load(f))

with open("results/all.pkl", "wb") as f:
    pickle.dump(data, f)
