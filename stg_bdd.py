import itertools
from pyeda.inter import *
import re
import networkx as nx


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

def generate_all_states(nodes):
    all_states = list(itertools.product([0, 1], repeat=len(nodes)))
    result = []
    for elm in all_states:
        a_dict = {}
        list_keys = list(nodes)
        list_values = list(elm)
        res = {list_keys[i]: list_values[i] for i in range(len(list_keys))}
        result.append(res)
    return result

def compute_stg(boolean_network):
    stg = nx.DiGraph()
    list_str = list(boolean_network.keys())
    list_bddvar = [bddvar(elm) for elm in list_str]
    states = generate_all_states(tuple(list_bddvar))

    for node, function in boolean_network.items():
        expression = expr2bdd(expr(boolean_network[node]))
        for state in states:
            stg.add_node(tuple(state.values()))
            updated_state = list(state.values())
            bdd_assignment = expression.restrict(state)
            updated_state[list(boolean_network.keys()).index(node)] = int(bdd_assignment)
            stg.add_edge(tuple(state.values()), tuple(updated_state))

    return stg


boolean_network = read_input("boolean_network_1.txt")
stg = compute_stg(boolean_network)

print("Edges:", stg.edges())
# def get_value_of_a_Boolean_function(expression, state):
#     bdd_assignment = expression.restrict(state)
#     result = int(bdd_assignment)
#     print(f"Assignment: {state}, Result: {result}")
    
# expression = expr2bdd(expr("x1 & x2 & x3"))
# states = generate_all_states(expression.inputs)
# get_value_of_a_Boolean_function(expression,states[0])