"""
This file contains short tests for sanity checks.
"""


def my_function(nums):
	return nums[0] * nums[1]


#
# Multithreading.
#

my_array = []
for i in range(0, 1000000):
	my_array.append([i, i + 1])

from multiprocessing.dummy import Pool as ThreadPool
pool = ThreadPool(1)
results = pool.map(my_function, my_array)

# print('Results:')
# for r in results:
# 	print(r)

# # Get rid of bookkeeping lines?
# with Pool(8) as p: p.map( *whatever* )



# #
# # Indexing
# #
# for x in range(0, 3):
# 	print(x)





#
# Regular expressions.
#

# import re

# one = 'This\nHas\n\nA\n\n\nLot\nOf New Lines\n\n\n\n'

# print(one)

# one = re.sub(r'\n', '', one)
# one = re.sub(r'e', '', one)

# print(one)




# one = 'This\nHas\n\nA\n\n\nLot\nOf New Lines\n\n\n\n'

# print(one)

# # one = re.sub(r'[\ne]', '', one)
# one = one.replace('\n', '')
# one = one.replace('e', '')

# print(one)