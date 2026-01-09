import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Tabeller

hash_to_symbol = {
  "MD5": "o",
  "SHA256": "s",
  "bcrypt": "v"
}

charset_to_color = {
  "lower": "green",
  "lower+upper": "orange",
  "lower+upper+symbols": "red"
}

# Exempeldata (syntetisk)
data = [
    ("MD5", "lower", 5, 0.01),
    ("SHA256", "lower", 10, 0.02),
    ("bcrypt", "lower+upper", 15, 0.03),
    ("bcrypt", "lower+upper", 20, 0.04),
    ("bcrypt", "lower+upper+symbols", 25, 0.05),
]


# Skapa figur
plt.figure(figsize=(8, 5))

for row in data:
    plt.scatter(
        row[2],
        row[3],
        color=charset_to_color[row[1]],
        alpha=0.7,
        marker=hash_to_symbol[row[0]]
    )

# Axlar och skala
plt.yscale("log")
plt.xlabel("Lösenordslängd")
plt.ylabel("Tid till knäckning (sekunder, log-skala)")
plt.title("Brute-force benchmark")

# Legend (manuell för tydlighet)
for h, c in hash_to_symbol.items():
    plt.scatter([], [], marker=c, label=h, color="black")
plt.legend(title="Hashfunktion")

for c, h in charset_to_color.items():
    plt.scatter([], [], color=h, label=c)
plt.legend(title="Teckenkombination")

plt.tight_layout()
plt.show()
