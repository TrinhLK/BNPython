import sys
sys.setrecursionlimit(5000)
print(sys.getrecursionlimit())

def dfs(node, adj, visited, count):
	visited[node] = True
	count += 1
	for neighbor in adj[node]:
		if not visited[neighbor]:
			count = dfs(neighbor, adj, visited, count)
	return count

def count_pairs(n, astronaut):
	adj = [[] for i in range(n)]
	for i, j in astronaut:
		adj[i].append(j)
		adj[j].append(i)

	visited = [False] * n
	v = []
	for i in range(n):
		count = 0
		if not visited[i]:
			count = dfs(i, adj, visited, count)
			v.append(count)

	ans = n * (n - 1) // 2
	for i in range(len(v)):
		ans -= v[i] * (v[i] - 1) // 2

	return ans

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

# test = read_input("demofile2.txt")
test = read_input("input_code_1.txt")

# 4527147
N = 9
mat = [[0,1],[1,2],[2,5]]
print ()
print (count_pairs(test[0],test[1]))