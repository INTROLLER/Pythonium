import pickle

filename = "results/" + input("File name: ") + ".pkl"

with open(filename, "rb") as f:
  data = pickle.load(f)

with open("results/all.pkl", "wb") as f:
  data.extend(pickle.load(f))
  pickle.dump(data, f)