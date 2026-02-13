import time


def timing_function(func):
	"""
	Timer decorator function
	
	:param func: Function to be decorated
	"""

	def wrapper():
		start = time.perf_counter
		func()
		end = time.perf_counter
		print(f"'{func}' execution time: {'{:.2e}'.format(end - start)}")
	return wrapper



def str_to_list(str:str) -> list[list]:
	"""
	Modifies the (str)vocabulary into a list
	
	:param str: The input str.
	:type str: str
	:return: The vocabulary as list of a list.
	:rtype: list[list]
	"""

	result = []
	for line in str.splitlines():
		line = line.strip()
		if not line:
			continue
		cols = [c.strip() for c in line.split(',')]
		result.append(cols)
	return result
