"""
This file contains short tests for sanity checks.
"""


def myFun(index, nums, out):
	print(str(index) + ': ' + str(sum(nums)))

	# This should be okay because each thread gets a unique index.
	out[index] = sum(nums)
	return


import threading

# Create the threads
threads = []
output = []
for i in range(0,5):
	output.append(0)
	t = threading.Thread(target=myFun, args=(i, [i, i + 1], output))
	threads.append(t)
	t.start()

# # Run the threads
# for t in threads:
# 	t.start()

for t in threads:
	t.join()

for o in output:
	print(o)

print('Done!')


# import re

# foilTitle = 'this is a string that contains Foil'
# nonFoilTitle = 'MTG 1X The Locust God X1 Hour of Devastation NM/MT Magic HOU Legendary'

# boolIsTrue  = True
# boolIsFalse = False

# print('boolIsTrue is ' + ('TRUE' if boolIsTrue else 'FALSE'))
# print('boolIsFalse is ' + ('TRUE' if boolIsFalse else 'FALSE'))

# if (re.search(r'foil', foilTitle, re.IGNORECASE) != None):
# 	print('Search for \"foil\" succeeded in foilTitle')
# else:
# 	print('Search for \"foil\" failed in foilTitle')

# if (re.search(r'foil', nonFoilTitle, re.IGNORECASE) != None):
# 	print('Search for \"foil\" succeeded in nonFoilTitle')
# else:
# 	print('Search for \"foil\" failed in nonFoilTitle')



# if (re.search(r'foil', foilTitle, re.IGNORECASE) == None):
# 	print('Search for \"foil\" negated in foilTitle')
# else:
# 	print('Search for \"foil\" did not negate in foilTitle')

# if (re.search(r'foil', nonFoilTitle, re.IGNORECASE) == None):
# 	print('Search for \"foil\" negated in nonFoilTitle')
# else:
# 	print('Search for \"foil\" did not negate in nonFoilTitle')






# myArr = [1, 2, 3, 4, 5]
# print(myArr[0:2])




# #
# # Multithreading.
# #
# def my_function(nums):
# 	return nums[0] * nums[1]

# my_array = []
# for i in range(0, 1000000):
# 	my_array.append([i, i + 1])

# from multiprocessing.dummy import Pool as ThreadPool
# pool = ThreadPool(8)
# results = pool.map(my_function, my_array)

# # print('Results:')
# # for r in results:
# # 	print(r)








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