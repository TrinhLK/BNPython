import itertools
from pyeda.inter import *
import re
from random import randint, choice
import random
import networkx as nx


# Read input file
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

# Compute Signed Directed Graph
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

# Compute State Transition Graph
# -----------------------------
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
# END Computing STG -----------------------------

# Compute Feedback Vertex Set
# -----------------------------
def compute_feedback_vertex_set(sdg):
    u = set()
    v_self = {v for v in sdg if v in sdg[v]}
    u.update(v_self)
    sdg.remove_nodes_from(v_self)
    c = get_nontrivial_sccs(sdg)
    while c:
        scc = random.choice(c)
        v = find_vertex_with_maximum_outdegree(sdg, scc)
        u.add(v)
        c_c = get_nontrivial_sccs(sdg.subgraph(scc - {v}))
        c.extend(c_c)
        c.remove(scc)
    return u

def get_nontrivial_sccs(sdg):
    return [scc for scc in nx.strongly_connected_components(sdg) if len(scc) > 1]

def find_vertex_with_maximum_outdegree(sdg, scc):
    max_outdegree = -1
    vertex = None
    for v in scc:
        outdegree = sdg.out_degree(v)
        if outdegree > max_outdegree:
            max_outdegree = outdegree
            vertex = v
    return vertex

# END Computing FVS -----------------------------

boolean_network = read_input("arellano_rootstem.bnet")

# Create {"Node_name":position}
dict_boolean_network = {}
for i in range(len(boolean_network.keys())):
    dict_boolean_network[list(boolean_network.keys())[i]] = i

print (dict_boolean_network)
stg = compute_stg(boolean_network)
signed_directed_graph = compute_signed_directed_graph(boolean_network)
feedback_vertex_set = compute_feedback_vertex_set(signed_directed_graph)

# Print the feedback vertex set
print("Feedback Vertex Set:")
print(feedback_vertex_set)

stg_prime = stg
#FVS
# fvs = {'x1', 'x3'}
set_B = []
for i in range(len(list(dict_boolean_network.keys()))):
    x = randint(0,1)
    set_B.append(x)

print("set_B:", str(set_B))
list_arcs_to_be_removed = []
for edge in stg.edges():
    # print (edge[0])
    check_str = str(edge[0]) + "\t" + str(edge[1])
    for elm in list(feedback_vertex_set):
        if edge[0][dict_boolean_network[elm]] == set_B[dict_boolean_network[elm]] and edge[0][dict_boolean_network[elm]] != edge[1][dict_boolean_network[elm]]:
            list_arcs_to_be_removed.append(edge)
            check_str += "\t <---"
            # stg.remove_edge(edge[0], edge[1])
            print (check_str)

for arc in list_arcs_to_be_removed:
    stg.remove_edge(arc[0], arc[1])

# print("Edges:", stg.edges())
# def get_value_of_a_Boolean_function(expression, state):
#     bdd_assignment = expression.restrict(state)
#     result = int(bdd_assignment)
#     print(f"Assignment: {state}, Result: {result}")
    
# expression = expr2bdd(expr("x1 & x2 & x3"))
# states = generate_all_states(expression.inputs)
# get_value_of_a_Boolean_function(expression,states[0])