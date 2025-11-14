import bcrypt

<<<<<<< HEAD
def hash_password(password):
  salt = bcrypt.gensalt()
  hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
  return hashed_password

print(hash_password("password"))
=======
salt = bcrypt.gensalt()

print(salt)
>>>>>>> 0c56d7388a7045e64d8c59bf0cac959a4f311d5e
