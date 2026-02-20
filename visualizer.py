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

filename = "results/" + input("File to read from: ") + ".pkl"
ext_cap = float(input("Extrapolate up to: "))
tool_includes = (int(input("Include python? (<0> no, <1> yes): ")), int(input("Include hashcat? (<0> no, <1> yes): ")))
hash_func_incl = (int(input("Include md5? (<0> no, <1> yes): ")), int(input("Include sha256? (<0> no, <1> yes): ")), int(input("Include bcrypt? (<0> no, <1> yes): ")))
auto_y_cap = int(input("Auto time cap? (<0> no, <1> yes): "))

if auto_y_cap != 1:
    y_cap = float(input("Time cap (seconds): "))
else:
    y_cap = 0

if ext_cap < 1:
    ext_cap = 1

tool_counter = [0, 0]
hash_func_counter = [0, 0, 0]

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

def readable_function(params, tool, hash_name):
    a, b = params
    k = np.exp(b)

    print(f"{tool} — {hash_name}:")
    print(f"  f(x) = {a:.6g} * e^({b:.6g} x)")
    print(f"       = {a:.6g} * {k:.6g}^x")
    print()

with open(filename, "rb") as f:
    data = pickle.load(f)

# Skapa figur
plt.figure(figsize=(8, 5))

for row in data:
    if row[5] == "python":
        tool_counter[0] += 1
        if tool_includes[0] == 0:
            continue

    if row[5] == "hashcat":
        tool_counter[1] += 1
        if tool_includes[1] == 0:
            continue

    if auto_y_cap == 1 and row[4] > y_cap:
        y_cap = row[4]

    if row[3] > ext_cap:
        ext_cap = row[3]

    if row[1] == "md5":
        hash_func_counter[0] += 1
        if hash_func_incl[0] == 0:
            continue

    if row[1] == "sha256":
        hash_func_counter[1] += 1
        if hash_func_incl[1] == 0:
            continue

    if row[1] == "bcrypt":
        hash_func_counter[2] += 1
        if hash_func_incl[2] == 0:
            continue

    plt.scatter(
        row[3],
        row[4],
        color=red_green_color(weight=row[2]),
        alpha=0.7,
        marker=hash_to_symbol[row[1]],
        edgecolors=tool_outline[row[5]]
    )

if auto_y_cap == 1:
    y_cap *= 1.1

data_bcrypt = [row for row in data if row[1] == "bcrypt"]
data_sha256 = [row for row in data if row[1] == "sha256"]
data_md5 = [row for row in data if row[1] == "md5"]

data_batches = [data_md5, data_sha256, data_bcrypt]

python_params = fit_exp("python", data)
hashcat_params = fit_exp("hashcat", data)

# Axlar och skala
plt.xlabel("Lösenordslängd")
plt.ylabel("Tid till knäckning (sekunder)")
plt.title("Brute force-resultat från " + filename)

# Linjer
for batch in data_batches:
    low_entoropy = []
    high_entoropy = []

    if len(batch) == 0 or hash_func_incl[hash_list.index(batch[0][1])] == 0:
        continue

    for row in batch:
        if row[2] == 0:
            low_entoropy.append(row)
        if row[2] == 4.5:
            high_entoropy.append(row)

    entropy_groups = [low_entoropy, high_entoropy]
    for group in entropy_groups:
        if len(group) == 0:
            continue

        python_params = fit_exp("python", group)
        hashcat_params = fit_exp("hashcat", group)

        if python_params is not None and tool_includes[0] == 1:
            draw_exp(python_params, 1, ext_cap, "python")
            readable_function(python_params, "python", batch[0][1])
        if hashcat_params is not None and tool_includes[1] == 1:
            draw_exp(hashcat_params, 1, ext_cap, "hashcat")
            readable_function(hashcat_params, "hashcat", batch[0][1])

# Legend
for h, c in hash_to_symbol.items():
    if hash_func_counter[hash_list.index(h)] > 0:
        plt.scatter([], [], marker=c, label=h, color="black")
plt.legend(title="Hashfunktion")

plt.ylim(0, y_cap)
plt.tight_layout()
plt.show()