import networkx as nx

def is_reachable(G, s1, s2):
    # Perform BFS starting from s1
    visited = {s1}
    queue = [s1]
    while queue:
        curr = queue.pop(0)
        # Check if s2 is visited
        if curr == s2:
            return True
        # Add unvisited successor states to the queue
        for succ in G.successors(curr):
            if succ not in visited:
                visited.add(succ)
                queue.append(succ)
    # If s2 is not visited, it is not reachable from s1
    return False

stg = nx.DiGraph()

stg.add_node((0, 0))
stg.add_node((0, 1))
stg.add_node((1, 0))
stg.add_node((1, 1))

stg.add_edge((0, 0), (0, 0))
stg.add_edge((0, 0), (1, 0))
stg.add_edge((1, 0), (0, 0))
stg.add_edge((0, 1), (0, 0))
stg.add_edge((1, 0), (1, 1))
stg.add_edge((1, 1), (1, 1))# Check if (1,0) is reachable from (0,0) in the STG
reachable = is_reachable(stg, (0,0), (1,0))
print(reachable) # should print True
test1 = [1,2,3,4]
test2 = [3,5,6]
test1 = test1 + test2
print(test1)