import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pickle
import numpy as np
from scipy.optimize import curve_fit

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

def exp_model(x, a, b):
    return a * np.exp(b * x)

def regression(tool, data):
    x, y = [], []
    print(data)
    for row in data:
        if row[5] == tool:
            x.append(row[3])
            y.append(row[4])

    if len(x) == 0 or len(y) == 0:
        return None
    
    params, cov = curve_fit(exp_model, x, y)
    a, b = params

    x_fit = np.linspace(min(x), max(x), 200)
    y_fit = exp_model(x_fit, a, b)

    return (x_fit, y_fit)

def red_green_color(weight, vmin=0.5, vmax=4.5):
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
    cmap = plt.cm.RdYlGn_r  # red → yellow → green
    return cmap(norm(weight))

with open("benchmarks.pkl", "rb") as f:
    data = pickle.load(f)

# Skapa figur
plt.figure(figsize=(8, 5))

for row in data:
    plt.scatter(
        row[3],
        row[4],
        color=red_green_color(weight=row[2]),
        alpha=0.7,
        marker=hash_to_symbol[row[1]],
        edgecolors=tool_outline[row[5]]
    )

python_reg = regression("python", data)
hashcat_reg = regression("hashcat", data)

# Linjer
if python_reg is not None:
    x_fit, y_fit = python_reg
    plt.plot(x_fit, y_fit, color="black", label="python")
if hashcat_reg is not None:
    x_fit, y_fit = hashcat_reg
    plt.plot(x_fit, y_fit, color="red", label="hashcat")

# Axlar och skala
plt.xlabel("Lösenordslängd")
plt.ylabel("Tid till knäckning (sekunder)")
plt.title("Brute-force benchmark")

# Legend (manuell för tydlighet)
for h, c in hash_to_symbol.items():
    plt.scatter([], [], marker=c, label=h, color="black")
plt.legend(title="Hashfunktion")

plt.tight_layout()
plt.show()