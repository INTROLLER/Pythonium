import pickle
from itertools import groupby

with open("benchmarks.pkl", "rb") as f:
    data = pickle.load(f)

g = open("results.txt", "w")

sorted_data = sorted(
    data,
    key=lambda x: (x[5], x[3], x[1], x[4])
)

for tool, group in groupby(sorted_data, key=lambda x: x[5]):
    # print(f"\n=== {tool} ===")
    g.write(f"\n=== {tool} ===\n")
    for entry in group:
        # print(entry)
        g.write(str(entry) + "\n")
