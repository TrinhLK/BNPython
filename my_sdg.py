import networkx as nx
from pyeda.inter import *

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

def compute_signed_directed_graph(abn):
    signed_directed_graph = nx.DiGraph()

    for node, function in abn.items():
        expr_function = expr(function)
        # Minimize the function using Espresso
        minimized_function = espresso_exprs(expr_function)
        expr_str = str(minimized_function[0])
        list_vars = []
        if node not in signed_directed_graph:
            signed_directed_graph.add_node(node)

        for aVar in list(minimized_function[0].inputs):
            if str(aVar) not in signed_directed_graph:
                signed_directed_graph.add_node(str(aVar))

            if "~"+str(aVar) in expr_str:
                list_vars.append("~"+str(aVar))
                signed_directed_graph.add_edge(str(aVar), node, sign=-1)
            elif str(aVar) in expr_str:
                list_vars.append(str(aVar))
                signed_directed_graph.add_edge(str(aVar), node, sign=1)
                
    return signed_directed_graph

# Example ABN
my_abn = read_boolean_network("boolean_network.txt")
# Compute the signed directed graph
signed_directed_graph = compute_signed_directed_graph(my_abn)

# Print the signed directed graph
print("Signed Directed Graph:")
for edge in signed_directed_graph.edges(data=True):
    source, target, data = edge
    print(f"{source} --> {target} (sign: {data['sign']})")
