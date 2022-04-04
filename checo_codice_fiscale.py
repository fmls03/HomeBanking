from codicefiscale import codicefiscale

surname = 'Iacolino'
name = 'Mauro'
sex = 'M'
birthdate = '13/5/2003'
birthplace = 'Palermo'

codice_fiscale_vero =codicefiscale.encode(surname = surname, name = name, sex = sex, birthdate = birthdate, birthplace = birthplace)

print(codice_fiscale_vero)