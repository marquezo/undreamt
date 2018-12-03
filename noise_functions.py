import numpy as np
import random


def remove_one_noise(input_ids, lengths, pad, to_remove=None):
	"""
	input_ids: list of list of integers
	lengths: lengths of above lists, excluding padding
	pad: ID of PAD token
	to_remove: indices of elements to remove, or delete randomly
	"""
	if to_remove is not None:
		assert len(to_remove) == len(lengths)

	input_arr = np.array(input_ids)
	
	for i, length in enumerate(lengths):

		if to_remove is None:
			r = random.randint(0, length -2)
		else:
			r = to_remove[i]

		input_arr[r:-1, i] = input_arr[r+1:, i]
		input_arr[-1, i] = pad

	return input_arr.tolist()


def unit_test():
	test = [[100,200,300],[200,300,400],[300,4, 4],[4,0,0]]
	lengths = [4, 3, 3]
	to_delete = [2, 1, 1]
	result = [[100, 200, 300], [200, 4, 4], [4, 0, 0], [0, 0, 0]]

	out = remove_one_noise(test, lengths, 0, to_delete)
	print(out)
	assert(result == out)

	to_delete = [2, 0, 0]
	result = [[100, 300, 400], [200, 4, 4], [4, 0, 0], [0, 0, 0]]
	out = remove_one_noise(test, lengths, 0, to_delete)
	print(out)
	assert(result == out)

	to_delete = [0, 0, 1]
	result = [[200, 300, 300], [300, 4, 4], [4, 0, 0], [0, 0, 0]]
	out = remove_one_noise(test, lengths, 0, to_delete)
	print(out)
	assert(result == out)

	test = [[200, 300, 500], [100, 200, 300], [200, 100, 200], [400, 5, 4], [4, 4, 0]]
	to_delete = [3, 3, 1]
	result = [[200, 300, 500], [100, 200, 200], [200, 100, 4], [4, 4, 0], [0, 0, 0]]
	out = remove_one_noise(test, lengths, 0, to_delete)
	print(out)
	assert(result == out)

	out = remove_one_noise(test, lengths, 0)
	print(test)
	print(out)


if __name__ == "__main__":
	unit_test()

