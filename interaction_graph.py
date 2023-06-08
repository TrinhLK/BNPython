import networkx as nx
import matplotlib.pyplot as plt

# 1. Read input file
def read_boolean_network(file_path):
    boolean_network = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('#') or line.strip() == '':
                continue
            node, function = line.strip().split('=')
            boolean_network[node.strip()] = function.strip()
    return boolean_network

# 2. Compute the interaction graph
def compute_interaction_graph(boolean_network):
    interaction_graph = nx.DiGraph()
    for node in boolean_network:
        function = boolean_network[node]
        dependencies = [dep.strip() for dep in function.split('AND') + function.split('OR') + function.split('XOR')]
        for dep in dependencies:
            if dep in boolean_network:
                interaction_graph.add_edge(dep, node)
    return interaction_graph

# 3. Compute the FVS
def compute_fvs(interaction_graph):
    fvs = set()
    while interaction_graph.edges:
        node_degrees = dict(interaction_graph.in_degree())
        sorted(node_degrees.items())
        max_degree_node = max(node_degrees, key=node_degrees.get)
        print ("node_degress: " + str(node_degrees) + " max: " + str(max_degree_node))
        fvs.add(max_degree_node)
        interaction_graph.remove_node(max_degree_node)
    return fvs

# 4. Compute the FVS
def find_all_fvs(interaction_graph):
    fvs_list = []
    nodes = list(interaction_graph.nodes)
    fvs = set()

    def backtrack(node_idx):
        if node_idx >= len(nodes):
            fvs_list.append(list(fvs))
            return
        
        node = nodes[node_idx]
        fvs.add(node)
        if is_valid_fvs():
            backtrack(node_idx + 1)
        fvs.remove(node)
        backtrack(node_idx + 1)

    def is_valid_fvs():
        for edge in interaction_graph.edges:
            if edge[1] not in fvs and edge[0] in fvs:
                return False
        return True

    backtrack(0)
    return fvs_list
# Example usage
file_path = 'boolean_network_ex.txt'  # Path to the input file
boolean_network = read_boolean_network(file_path)
interaction_graph = compute_interaction_graph(boolean_network)
# print ("IG type: " + str(type(interaction_graph.edges)))
print (str(list(interaction_graph.edges)))
print ("In degree: " + str(interaction_graph.in_degree()))
# Plotting the interaction graph
# nx.draw(interaction_graph, with_labels=True, arrows=True)
# plt.show()

fvs = compute_fvs(interaction_graph)
print("Feedback Vertex Set:", fvs)

fvs_list = find_all_fvs(interaction_graph)
print("All Possible Feedback Vertex Sets:")
for fvs in fvs_list:
    print(fvs)
# Plotting the interaction graph without the FVS nodes
interaction_graph.remove_nodes_from(fvs)
nx.draw(interaction_graph, with_labels=True, arrows=True)
plt.show()


