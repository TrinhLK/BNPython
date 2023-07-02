import random

def gen_data(n):
	rs = str(n) + "\n"
	for i in range(n):
		x = str(random.randint(0,n-1))
		y = str(random.randint(0,n-1))
		tmp = ""
		if x != y:
			tmp += x + " " + y + "\n"
		if tmp not in rs:
			rs += tmp
	return rs

def gen_data_1():
	while True:
		m = random.randint(0, 700)
		n = random.randint(0, 700)

		if abs(m-n) <= 300 and m >= 2 and n >= 2:
			break
	# m = 3
	# n = 4
	operator = ['P', '2P', '3P', 'T', '2T', '3T']
	rs = str(m) + " " + str(n) + "\n"
	mat = [[random.randint(0,1) for y in range(n)] for x in range(m)]
	for i in range(m):
		for j in range(n):
			rs += str(mat[i][j]) + " "
		rs += "\n"
	tmp = []
	for i in range(random.randint(1,20)):
		tmp.append(operator[random.randint(0,len(operator)-1)])
		rs += operator[random.randint(0,len(operator)-1)] + " "
	rs += "\n"
	return rs
# rs = gen_data(5000)
rs = gen_data_1()
print (str(rs))

f = open("demofile2.txt", "w")
f.write(rs)
f.close()

