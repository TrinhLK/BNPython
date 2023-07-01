import random

def gen_data(n):
	rs = str(n) + "\n"
	for i in range(n):
		rs += str(random.randint(0,n-1)) + " " + str(random.randint(0, n-1)) + "\n"
	return rs

rs = gen_data(5000)
print (rs)

f = open("demofile2.txt", "w")
f.write(rs)
f.close()