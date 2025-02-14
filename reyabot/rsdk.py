from examples.new import get_crypto_price

def cprice(currency):
	price = get_crypto_price(currency)
	return price

#print(cprice("ADA"))
