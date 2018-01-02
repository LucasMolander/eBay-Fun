import sys
import re
import inspect

"""
Removes all non-ascii (less than 128) characters from a string.
"""
def removeNonASCII(str):

    # print('removeNonASCII')
    # sys.stdout.flush()

    out = []

    for c in str:
        out.append(c if ord(c) < 128 else '')

    return ''.join(out)

def removeOffersTaken(titles, prices):

    # print('removeOffersTaken')
    # sys.stdout.flush()

    i = len(prices) - 1

    while i >= 0:
        if not (re.search(r'^\$\d+\.\d+$', prices[i])):
            del prices[i]
            del titles[i]
        i = i - 1

"""
Removes results containing any of the given words.
This is case in-sensitive, for both the title and words.
"""
def removeContaining(titles, prices, words):

    # print('pricesToNumbers')
    # sys.stdout.flush()

    i = len(prices) - 1

    while i >= 0:
        if (i < 0 or i >= len(titles)):
            # This should never happen, but if this isn't here, a thread will
            # be out of bounds and throw an Exception at the end of the program.
            # This ONLY happens in a threaded version.
            # Without multithreading, this never happens. Sigh.
            return

        for w in words:
            if w.lower() in titles[i].lower():
                del prices[i]
                del titles[i]
                break

        i = i - 1

    # except:
    #     print(inspect.trace())

"""
Removes results not containing all of the given words.
This is case in-sensitive, for both the title and words.
"""
def removeNotContaining(titles, prices, words):

    # print('pricesToNumbers')
    # sys.stdout.flush()

    i = len(prices) - 1

    while i >= 0:
        for w in words:
            if not w.lower() in titles[i].lower():
                del prices[i]
                del titles[i]
                break

        i = i - 1
