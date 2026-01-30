import pickle

with open("benchmarks.pkl", "rb") as f:
    data = pickle.load(f)

print(data)