import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pickle
import numpy as np
from scipy.optimize import curve_fit

# Tabeller

hash_list = ["md5", "sha256", "bcrypt"]

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

filename = input("File to read from: ") + ".pkl"
ext_cap = float(input("Extrapolate up to: "))
tool_includes = (int(input("Include python? (<0> no, <1> yes): ")), int(input("Include hashcat? (<0> no, <1> yes): ")))
hash_func_incl = (int(input("Include md5? (<0> no, <1> yes): ")), int(input("Include sha256? (<0> no, <1> yes): ")), int(input("Include bcrypt? (<0> no, <1> yes): ")))
y_cap = float(input("Time cap (seconds): "))
if ext_cap < 1:
    ext_cap = 1

def exp_model(x, a, b):
    return a * np.exp(b * x)

def fit_exp(tool, data):
    x, y = [], []
    for row in data:
        if row[5] == tool:
            x.append(row[3])
            y.append(row[4])
    
    if len(x) == 0 or len(y) == 0:
        return None
    
    x = np.array(x)
    y = np.array(y)

    params, _ = curve_fit(exp_model, x, y)
    return params  # (a, b)

def draw_exp(params, x_min, x_max, tool, n=300):
    a, b = params
    x_draw = np.linspace(x_min, x_max, n)
    y_draw = exp_model(x_draw, a, b)
    plt.plot(x_draw, y_draw, color=tool_outline[tool])

def red_green_color(weight, vmin=0.5, vmax=4.5):
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
    cmap = plt.cm.RdYlGn_r  # red → yellow → green
    return cmap(norm(weight))

with open("results" + filename, "rb") as f:
    data = pickle.load(f)

# Skapa figur
plt.figure(figsize=(8, 5))

for row in data:
    if row[5] == "python" and tool_includes[0] == 0:
        continue

    if row[5] == "hashcat" and tool_includes[1] == 0:
        continue

    if row[3] > ext_cap:
        ext_cap = row[3]

    if row[1] == "md5" and hash_func_incl[0] == 0:
        continue

    if row[1] == "sha256" and hash_func_incl[1] == 0:
        continue

    if row[1] == "bcrypt" and hash_func_incl[2] == 0:
        continue

    plt.scatter(
        row[3],
        row[4],
        color=red_green_color(weight=row[2]),
        alpha=0.7,
        marker=hash_to_symbol[row[1]],
        edgecolors=tool_outline[row[5]]
    )

python_params = fit_exp("python", data)
hashcat_params = fit_exp("hashcat", data)

# Axlar och skala
plt.xlabel("Lösenordslängd")
plt.ylabel("Tid till knäckning (sekunder)")
plt.title("Brute force-resultat från " + filename)

# Linjer
if python_params is not None and tool_includes[0] == 1:
    draw_exp(python_params, 1, ext_cap, "python")
if hashcat_params is not None and tool_includes[1] == 1:
    draw_exp(hashcat_params, 1, ext_cap, "hashcat")

# Legend
for h, c in hash_to_symbol.items():
    if hash_func_incl[hash_list.index(h)] == 1:
        plt.scatter([], [], marker=c, label=h, color="black")
plt.legend(title="Hashfunktion")

plt.ylim(0, y_cap)
plt.tight_layout()
plt.show()