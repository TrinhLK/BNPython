from pyeda.inter import *
import re
from pyeda.boolalg.bdd import expr2bdd



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
        bdd = expr2bdd(fexpr)
        # print (bdd.inputs)
        print (bdd)
        fexpr = bdd2expr(bdd)
        print (fexpr)
        print (fexpr.inputs)

        current_node = bdd.root
        while not bdd.is_terminal(current_node):
            level = bdd.level_of(current_node)
            if level.var == variable:
                low_edge = bdd.low(current_node)
                high_edge = bdd.high(current_node)
                if bdd.is_zero(low_edge) and bdd.is_one(high_edge):
                    return True
                elif bdd.is_one(low_edge) and bdd.is_zero(high_edge):
                    return False
            current_node = bdd.low(current_node)  # Follow low edge

    for boolean_function in boolean_network.values():
        print (boolean_function)
        tokens = re.split("\&|\||\^", boolean_function)
        print (tokens)
        # print (boolean_network.keys())
        # bdd.to_dot()
        # fexpr = bdd2expr(bdd)
        # for bdd_var in fexpr.inputs:
        #     if isinstance(bdd_var, ExprComplement):
        #         print("yes")
        # fexpr = bdd2expr(bdd)
        # print (fexpr)
compute_signed_directed_graph(boolean_network)