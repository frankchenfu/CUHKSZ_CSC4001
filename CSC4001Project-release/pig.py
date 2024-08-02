class Integer:
	def __init__(self, value: int, dtype: int) -> None:
		self.value = value
		self.dtype = dtype
	def __str__(self) -> str:
		return f"({self.value}, dtype={self.dtype})"
	def __repr__(self) -> str:
		return f"{self.value:0{self.dtype}b}"
	
	def __add__(self, other: "Integer") -> "Integer":
		res_dtype = max(self.dtype, other.dtype)
		res_value = (self.value + other.value) % (1 << res_dtype)
		return Integer(res_value, res_dtype)
	def __sub__(self, other: "Integer") -> "Integer":
		res_dtype = max(self.dtype, other.dtype)
		res_value = (self.value - other.value) % (1 << res_dtype)
		return Integer(res_value, res_dtype)
	def __and__(self, other: "Integer") -> "Integer":
		res_dtype = max(self.dtype, other.dtype)
		res_value = self.value & other.value
		return Integer(res_value, res_dtype)
	def __or__(self, other: "Integer") -> "Integer":
		res_dtype = max(self.dtype, other.dtype)
		res_value = self.value | other.value
		return Integer(res_value, res_dtype)

	def __bool__(self) -> bool:
		return bool(self.value)
	def __int__(self) -> int:
		return self.value
	
	def resize(self, dtype: int) -> "Integer":
		return Integer(self.value % (1 << dtype), dtype)

def parser(s: list, vars: dict) -> "Integer":
	for i in range(len(s)):
		if s[i].isdigit():
			s[i] = f"Integer(int(\"{s[i]}\", base=2), {len(s[i])})"
	return eval(" ".join(s), globals(), vars)

if __name__ == "__main__":
	with open("./input.pig", "r") as fin, open("./1.out", "w") as fout:
		vars = dict()
		lines = fin.readlines()
		cur = 0
		for _ in range(5000):
			if cur >= len(lines):
				break
			tokens = lines[cur].strip().split()
			if tokens[0] == "D":
				assert tokens[1] not in vars.keys(), f"Variable {tokens[1]} is already declared"
				vars[tokens[2]] = Integer(0, int(tokens[1][2:]))
			elif tokens[0] == "A":
				assert tokens[1] in vars.keys(), f"Variable {tokens[1]} is not declared"
				vars[tokens[1]] = parser(tokens[2:], vars).resize(vars[tokens[1]].dtype)
			elif tokens[0] == "B":
				assert 0 <= int(tokens[1]) < len(lines), f"Branch out of range"
				if parser(tokens[2:], vars):
					cur = int(tokens[1])
					continue
			elif tokens[0] == "O":
				assert tokens[1] in vars.keys(), f"Variable {tokens[1]} is not declared"
				fout.write(f"{vars[tokens[1]].__repr__()}\n")
			elif tokens[0] == "R":
				assert tokens[1] in vars.keys(), f"Variable {tokens[1]} is not declared"
				del vars[tokens[1]]
			cur += 1
		else:
			print("too-many-lines")