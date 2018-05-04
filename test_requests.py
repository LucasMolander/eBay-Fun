import requests
import threading

    # # Takes 3 seconds
    # l = list(string)
    # length = len(l)
    # for i in range(length - 1, -1, -1):
    #     if (ord(l[i]) >= 128):
    #         del l[i]

    # return ''.join(l)


    # # Didn't even finish...
    # out = ''
    # for c in string:
    #     if (ord(c) < 128):
    #         out += c

    # return out


    # # Takes 4 seconds
    # out = []

    # for c in string:
    #     out.append(c if ord(c) < 128 else '')

    # return ''.join(out)

# 50 facebook.com requests: 17 seconds
# At about 420kb though
#
# Threaded 50 facebook.com requests: 2 seconds
def getPage(HTMLs, index):
    url = 'https://www.facebook.com/'
    r = requests.get(url)

    HTMLs[index] = r.text


n = 50

threads = []

# Target for threads
HTMLs = ['' for i in range(0, n)]

# Create and run the threads
for i in range(0, n):
    args = (HTMLs, i)
    t = threading.Thread(target=getPage, args=args)
    threads.append(t)
    t.start()

# Wait for all threads to be done.
for t in threads:
    t.join()
    del t

for i in range(0, len(HTMLs)):
    HTMLs[i] = HTMLs[i].encode('ascii', 'ignore')
    print(str(len(HTMLs[i])))


# for i in range(0, 50):
#     getPage()
