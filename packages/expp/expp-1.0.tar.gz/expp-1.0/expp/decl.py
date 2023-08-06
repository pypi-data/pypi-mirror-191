class DeclarateGlobalVars(object):
	
	__slots__ = ["__line", "__count", "__my_DICT"]
	
	__STATUS_ERROR = TypeError("Type Mismatch")
	
	@classmethod
	def __verify_type(cls, arg, types:type):
		if not isinstance(arg, (types)):
			print(f"ERROR: {cls.__STATUS_ERROR}. Argument type must be {types}\nNow: {type(arg)} [{arg}]")
			exit()
			
	def __init__(self, line):
		self.__verify_type(line, int)
		self.__line = line
		self.__count = 0
		self.__my_DICT = {}
		
	def get_vars(self, listglob):
		self.__verify_type(listglob, dict)
		for i in listglob:
			if self.__count < self.__line:
				self.__count += 1
				continue
			else:
				self.__my_DICT[str(i)] = listglob[i]
		for k in self.__my_DICT:
			strs = f"[{k}] -——- {self.__my_DICT[k]}"
			print(strs)
			
		return "\nDone"