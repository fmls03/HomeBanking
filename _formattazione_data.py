import datetime
from _signup import *


def formatta_data(data):
	
	formato_data = datetime.datetime.strptime(data, '%Y-%m-%d').strftime('%d/%m/%Y')

	print(formato_data)

	return formato_data

	