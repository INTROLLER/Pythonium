import matplotlib.pyplot as plt
import pickle

# Tabeller

hash_to_symbol = {
  "md5": "o",
  "sha256": "s",
  "bcrypt": "v"
}

charset_to_color = {
  "lower": "green",
  "lower+upper": "orange",
  "all": "red"
}

# Tool to outline

tool_outline = {
    "python": "black",
    "hashcat": "red"
}

with open("benchmarks.pkl", "rb") as f:
    data = pickle.load(f)

# Skapa figur
plt.figure(figsize=(8, 5))

for row in data:
    plt.scatter(
        row[2],
        row[3],
        color=charset_to_color[row[1]],
        alpha=0.7,
        marker=hash_to_symbol[row[0]],
        edgecolors=tool_outline[row[4]]
    )

# Axlar och skala
plt.xlabel("Lösenordslängd")
plt.ylabel("Tid till knäckning (sekunder, log-skala)")
plt.title("Brute-force benchmark")

# Legend (manuell för tydlighet)
for h, c in hash_to_symbol.items():
    plt.scatter([], [], marker=c, label=h, color="black")
plt.legend(title="Hashfunktion")

plt.tight_layout()
plt.show()
