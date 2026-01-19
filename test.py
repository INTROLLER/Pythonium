import string

chars = string.printable
chars = chars.strip("\n")
chars = chars.strip()

for i in range(500):
  index = i

  passwd = []
  for i in reversed(range(3)):
    passwd.append(chars[index // 94 ** i])
    index = index % 94 ** i

  print("".join(passwd))