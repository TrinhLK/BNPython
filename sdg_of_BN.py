from pyeda.inter import *


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

boolean_network = read_input("boolean_network_1.txt")

def compute_signed_directed_graph(boolean_network):
    for variable, boolean_function in boolean_network.items():
        fexpr = expr(boolean_function)
        print (fexpr)

compute_signed_directed_graph(boolean_network)