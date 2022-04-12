from passlib.hash import sha256_crypt

p = 'HomeBankingAdmin2022'

print(sha256_crypt.hash(p))