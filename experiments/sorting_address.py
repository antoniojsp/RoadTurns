# Sorting algorithm to be used to sort algorithms
# Sorts an array



test_arr1 = [2, 2, 1, 1, 1, 1, 1, 3, 4]


def address_changing(arr):
	""" Takes an array of ints and returns when it changes 'directions' (ints) """
	prev = arr[0]
	for i in range(len(arr)):
		if i == 0:
			print('Starting on ' + str(arr[i]))
		elif arr[i] != prev:		
			if arr[i] > prev: 
				print("Turn right on " + str(arr[i]))
			else:
				print("Turn left on " + str(arr[i]))
			prev = arr[i]



# Main
address_changing(test_arr1)
