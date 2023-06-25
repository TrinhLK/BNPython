from pyeda.inter import *
import re
import networkx as nx

# Read the input file
# with open("input.txt", "r") as file:
def read_input(file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()

    boolean_network = {}
    for line in lines:
        if line.startswith("#") or line == "\n" or line.startswith("targets,"):
            continue
        lhs, rhs = map(str.strip, line.split(","))
        rhs = rhs.replace("!", "~")
        boolean_network[lhs] = rhs
    return boolean_network

def compute_signed_directed_graph(boolean_network):
    signed_directed_graph = nx.DiGraph()

    for variable, boolean_function in boolean_network.items():
        if variable not in signed_directed_graph:
            signed_directed_graph.add_node(variable)

        fexpr = expr(boolean_function)
        bdd = expr2bdd(fexpr)
        fexpr = bdd2expr(bdd)
        string_fexpr = str(fexpr)
        for aVar in fexpr.inputs:
            if str(aVar) not in signed_directed_graph:
                signed_directed_graph.add_node(str(aVar))
            count_aVar = string_fexpr.count(str(aVar))
            count_minusAVar = string_fexpr.count("~"+str(aVar))
            # print (str(aVar) + "\t" + str(count_aVar - count_minusAVar - count_minusAVar))
            if (count_aVar - count_minusAVar - count_minusAVar) < 0:
                signed_directed_graph.add_edge(str(aVar), variable, sign=-1)
            else:
                signed_directed_graph.add_edge(str(aVar), variable, sign=1)
    return signed_directed_graph


boolean_network = read_input("boolean_network_1.txt")
signed_directed_graph = compute_signed_directed_graph(boolean_network)
print("Signed Directed Graph:")
for edge in signed_directed_graph.edges(data=True):
    source, target, data = edge
    print(f"{source} --> {target} (sign: {data['sign']})")