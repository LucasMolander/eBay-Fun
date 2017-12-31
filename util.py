def pricesToNumbers(prices):
    out = []

    for price in prices:
        out.append(float(price[1:]))

    return out
