import random, string

def generate_iban():
	alphabet = list(string.ascii_uppercase)
	i = 0
	iban = "IT"
	iban = iban + str(random.randint(0, 9)) + str(random.randint(0, 9)) 
	iban = iban + alphabet[random.randint(0, 25)]
	while i < 11:
		iban = iban + str(random.randint(0, 9)) 
		i = i + 1
	iban = iban + alphabet[random.randint(0, 25)]
	iban = iban + alphabet[random.randint(0, 25)]
	
	j = 0

	while j < 9:
		iban = iban + str(random.randint(0, 9)) 
		j = j + 1

	return iban

generate_iban()