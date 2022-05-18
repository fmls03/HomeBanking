from passlib.hash import sha256_crypt

s = 'admin'

print(sha256_crypt.hash(s))