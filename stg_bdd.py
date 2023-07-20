import itertools
from pyeda.inter import *
from pyeda.boolalg.bfarray import exprvars
import re
from random import randint, choice
import random
import networkx as nx

# ------- Read input file
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

# ------- Compute Signed Directed Graph
def compute_signed_directed_graph(boolean_network):
    signed_directed_graph = nx.DiGraph()

    for variable, boolean_function in boolean_network.items():
        if variable not in signed_directed_graph:
            signed_directed_graph.add_node(variable)

        fexpr = expr(boolean_function)
        bdd_expr = expr2bdd(fexpr)
        fexpr = bdd2expr(bdd_expr)       # Convert the expression to BDD

        string_fexpr = str(fexpr)
        for aVar in fexpr.inputs:
            if str(aVar) not in signed_directed_graph:
                signed_directed_graph.add_node(str(aVar))

            vy = bddvar(str(aVar))
            fx_res_vy_0 = bdd_expr.restrict({vy:0})
            fx_res_vy_1 = bdd_expr.restrict({vy:1})
            pos_arc = ~fx_res_vy_0 & fx_res_vy_1
            neg_arc = fx_res_vy_0 & ~fx_res_vy_1

            if pos_arc.is_one() or pos_arc.satisfy_one():
                signed_directed_graph.add_edge(str(aVar), variable, sign=1)
            if neg_arc.is_one() or neg_arc.satisfy_one():
                signed_directed_graph.add_edge(str(aVar), variable, sign=-1)
                
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
        expression = expr2bdd(expr(boolean_network[node]))  # Convert to BDD
        for state in states:
            stg.add_node(tuple(state.values()))
            updated_state = list(state.values())
            bdd_assignment = expression.restrict(state)     # Choose a state using restrict 
            updated_state[list(boolean_network.keys()).index(node)] = int(bdd_assignment)  # Calculate next state
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

# Compute B
# -----------------------------
def count_satisfying_assignments(fi):
    fi_bdd = expr2bdd(fi)
    sols = fi_bdd.satisfy_all()
    count = 0
    for elm in sols:
        count = count + 1
    
    return count

def find_assignment(B):
    assignment = []
    
    for bi in B:
        fi = bi  # fi is the Boolean function associated with bi
        
        ctrue = count_satisfying_assignments(fi)
        cfalse = 2 ** len(fi.inputs) - ctrue
        
        if ctrue > cfalse:
            assignment.append(1)
        elif ctrue < cfalse:
            assignment.append(0)
        else:
            assignment.append(random.choice([0, 1]))
    
    return tuple(assignment)
# END B -----------------------------


# ------- Find Fixed Pointes
def find_fixed_points(stg):
    not_fp = []
    for edge in stg.edges:
        if edge[0] != edge[1]:
            not_fp.append(edge[0])
    return set(stg.nodes()) - set(not_fp)

def find_fixed_points_bdd(stg):
    not_fp = []
    for edge in stg.edges:
        if edge[0] != edge[1]:
            not_fp.append(edge[0])
    return set(stg.nodes()) - set(not_fp)

# ------- Remove arcs from a graph
def remove_arcs_from_graph(stg, set_B):
    stg_prime = nx.DiGraph()
    stg_prime.add_edges_from(stg.edges)
    list_arcs_to_be_removed = []

    for edge in stg_prime.edges():
        check_str = str(edge[0]) + "\t" + str(edge[1])
        for elm in list(feedback_vertex_set):
            if edge[0][dict_boolean_network[elm]] == set_B[dict_boolean_network[elm]] and edge[0][dict_boolean_network[elm]] != edge[1][dict_boolean_network[elm]]:
                list_arcs_to_be_removed.append(edge)

    for arc in list_arcs_to_be_removed:
        stg_prime.remove_edge(arc[0], arc[1])

    return stg_prime

# ------- Check whether s2 can be reached from s1
def is_reachable(G, s1, s2):
    # Perform BFS starting from s1
    print("s1 = " + str(s1))
    visited = {s1}
    queue = [s1]
    path = []
    while queue:
        curr = queue.pop(0)
        path.append(curr)
        # Check if s2 is visited
        if curr == s2:
            print ("path: " + str(path))
            return True
        # Add unvisited successor states to the queue
        for succ in G.successors(curr):
            if succ not in visited:
                visited.add(succ)
                queue.append(succ)
    # If s2 is not visited, it is not reachable from s1
    return False

def is_reachable_1(G, s1, s2):
    # Perform BFS starting from s1
    visited = {s1}
    queue = [s1]
    path = []
    while queue:
        curr = queue.pop(0)
        path.append(curr)
        # Check if s2 is visited
        if curr == s2:
            print ("path: " + str(path))
            return True
        # Add unvisited successor states to the queue
        for succ in G.successors(curr):
            if succ not in visited:
                visited.add(succ)
                queue.append(succ)
    # If s2 is not visited, it is not reachable from s1
    return False

# boolean_network = read_input("arellano_rootstem.bnet")
boolean_network = read_input("boolean_network_1.txt")

#  Create {"Node_name":position}
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
print ("stg: " + str(len(stg.edges)))

print (len(list(boolean_network.keys())))

list_var = []
for i in range(len(list(boolean_network.keys()))):
    list_var.append(exprvar('x', i))
# list_var = exprvars('x', 3)
print ("list_var: " + str(list_var))

set_B = find_assignment(list_var)
# for i in range(len(list(dict_boolean_network.keys()))):
#     x = randint(0,1)
#     set_B.append(x)

stg_prime = remove_arcs_from_graph(stg, set_B)
print ("stg_prime: " + str(len(stg_prime.edges)))

F = find_fixed_points(stg_prime)
# print (len(F))
F_fix = find_fixed_points(stg)
print ("F_fix: ")
print (F_fix)
F = F - F_fix
A = F_fix
TT = A.union(F)

print ("A: ")
for elm in A:
    print (elm)

print ("F: ")
for elm in F:
    print (elm)

print ("A + F: ")
print (len(TT))
for elm in TT:
    print (elm)

# print (len(F))
while len(F) != 0:
    s = F.pop()
    # print (len(F))
    # print ("s: " + str(s))
    # flag = False
    for elm_tt in TT:
        # print ("checking: " + str(elm_tt) + " to " + str(s))
        # print ("is_reachable: " + str(is_reachable(stg, elm_tt, s)))
        if is_reachable(stg, elm_tt, s) == False:
            # print ("add: " + str(s))
            # print ("to: " + str(A))
            A.add(s)        

print ("updated A: ")
print (len(A))
for elm in A:
    print (elm)
# print (len(F))
