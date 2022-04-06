import random, string

def generate_iban():
	alphabet = list(string.ascii_uppercase)
	i = 0
	j = 0

	sn = 'IT' # sigla nazionale
	nc = '88' # checksum internazionale - italia (88)
	cin = alphabet[random.randint(0, 25)]
	abi = '38055'
	cab = ''
	cc = ''
	
	while i < 5:
		cab += str(random.randint(0,9))
		i += 1

	while j < 12:
		cc += str(random.randint(0,9)) # conto corrente 
		j += 1

	iban = sn + nc + cin + abi + cab + cc

	return iban