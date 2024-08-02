from random import randint

if __name__ == "__main__":
	vars = set()
	with open("./input.pig", "w") as fin:
		for _ in range(1000):
			# choose operation with unequal probability:
			# D (declare) - 2/10
			# A (assign) - 3/10
			# B (branch) - 2/10
			# O (output) - 2/10
			# R (remove) - 1/10
			r = randint(1, 10)
			if 0 <= r < 2:
				dtype = [8, 16, 32, 64][randint(0, 3)]
				name = randint(0, 99)
				while name in vars:
					name = randint(0, 99)
				name = f"var{name:03}"
				vars.add(name)
				fin.write(f"D bv{dtype} {name}\n")
			elif 2 <= r < 5:
