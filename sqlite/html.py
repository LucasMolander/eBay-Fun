import re

class HTMLParseUtil(object):

    @staticmethod
    def removeOffersTaken(titles, prices):
        i = len(prices) - 1

        while i >= 0:
            if (i < 0 or i >= len(prices)):
                # This should never happen, but if this isn't here, a thread will
                # be out of bounds and throw an Exception at the end of the program.
                # This ONLY happens in a threaded version.
                # Without multithreading, this never happens. Sigh.
                return

            if (re.search(r'STRIKETHROUGH', prices[i])):
                del prices[i]
                del titles[i]
            i = i - 1

        # OLD:
        # while i >= 0:
        #     if not (re.search(r'^\$\d+\.\d+$', prices[i])):
        #         del prices[i]
        #         del titles[i]
        #     i = i - 1

    """
    Removes results containing any of the given words.
    This is case in-sensitive, for both the title and words.
    """
    @staticmethod
    def removeContaining(titles, prices, words):
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

    """
    Removes results not containing all of the given words.
    This is case in-sensitive, for both the title and words.
    """
    @staticmethod
    def removeNotContaining(titles, prices, words):
        i = len(prices) - 1
        while i >= 0:
            for w in words:
                if not w.lower() in titles[i].lower():
                    del prices[i]
                    del titles[i]
                    break

            i = i - 1

    def __init__(self):
        pass
