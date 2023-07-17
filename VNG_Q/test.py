import sys
sys.setrecursionlimit(5000) # python limits 1000 recursion by default

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

def dfs(node, adj, visited, count):
	visited[node] = True
	count += 1
	for neighbor in adj[node]:
		if not visited[neighbor]:
			count = dfs(neighbor, adj, visited, count)
	return count

def count_pairs(N, mat):
	# Create adjacency list
	adj = [[] for i in range(N)]
	for i, j in mat:
		adj[i].append(j)
		adj[j].append(i)

    # Count the number of connected components
	visited = [False] * N
	v = []
	for i in range(N):
		count = 0
		if not visited[i]:
			count = dfs(i, adj, visited, count)
			v.append(count)

	print (v)
	ans = N * (N - 1) // 2
	for i in range(len(v)):
        # Exclude pairs from each connected components
		ans -= v[i] * (v[i] - 1) // 2

	return ans
# test = read_input("demofile2.txt")
# test = read_input("input_code_1.txt")

# 4527147
N = 5
mat = [[1,2],[0,2],[1,4]]
print (count_pairs(N,mat))
# print (count_pairs(test[0],test[1]))