def pricesToNumbers(prices):
	return [float(p[1:]) for p in prices]

def priceToStr(price):
	out = str(round(price, 2))

	# If it's something like '13.2' instead of '13.20'
	if (out.find('.') == len(out) - 2):
		out += '0'

	return out