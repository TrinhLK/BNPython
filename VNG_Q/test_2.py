def findPrt(a):
  if prt[a] < 0:
    return a
  prt[a] = findPrt(prt[a])
  return prt[a]

def join(a, b):
  a = findPrt(a)
  b = findPrt(b)
  if a != b:
    prt[a] = b


# ------- Read input file
def read_input(file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()

    n = int(lines[0])
    astronaut = []
    for i in range(1,len(lines)):
        line = [int(x) for x in lines[i].split()]
        astronaut.append(line)
    return (n, astronaut)

test = read_input("demofile2.txt")
prt = [-1 for k in range(test[0])]

count = [0 for k in range(test[0])]
for k in range(test[0]):
  pk = findPrt(k)
  count[pk] = count[pk] + 1
print(sum([a * (test[0] - a) for a in count]) // 2)