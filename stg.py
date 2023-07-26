import itertools
from pyeda.inter import *
from random import randint, choice
import random
import copy

def construct_boolean_network(boolean_network):
    # Convert the dictionary of Boolean expressions into a dictionary of PyEDA BDDs
    bdd_network = {}
    for var, e_expr in boolean_network.items():
        bdd_network[bddvar(var)] = expr2bdd(expr(e_expr))
    return bdd_network

# Compute B
# -----------------------------
def count_satisfying_assignments(fi):
    fi_bdd = expr2bdd(fi)
    sols = fi_bdd.satisfy_all()
    count = 0
    for elm in sols:
        count = count + 1
    
    return count

def find_retained_set(B):
    assignment = []
    result = {}
    for bi in B:
        fi = bi  # fi is the Boolean function associated with bi
        # print ("bi: " + str(bi) + "\t" + str(type(bi)))
        bi_bddvar = bddvar(str(bi))
        ctrue = count_satisfying_assignments(fi)
        cfalse = 2 ** len(fi.inputs) - ctrue
        
        if ctrue > cfalse:
            assignment.append(1)
            result[bi_bddvar] = 1
        elif ctrue < cfalse:
            assignment.append(0)
            result[bi_bddvar] = 0
        else:
            assignment.append(random.choice([0, 1]))
            result[bi_bddvar] = random.choice([0, 1])
    # print("result: " + str(result))
    return result
# END B -----------------------------

# string_ss = "(B & C) & (A | C) & ~B"
def compute_stg_fixed_points(boolean_network):
    total_func = bddvar('x')
    total_func = total_func.restrict({total_func:1})

    for stg_bdd_node, stg_bdd_function in boolean_network.items():
        total_func &= (stg_bdd_node & stg_bdd_function) | (~stg_bdd_node & ~stg_bdd_function)

    return list(total_func.satisfy_all())

def compute_stg_minus_fixed_points(boolean_network, set_B):

    fp_reduced_STG = 1

    for node_bdd, func_bdd in boolean_network.items():

        if node_bdd in retained_set:
            if retained_set[node_bdd] == False:
                # B[node] = 0, only need the condition node_bdd --> func_bdd
                fp_reduced_STG &=  ((~node_bdd | func_bdd))
            else:
                # B[node] = 1, only need the condition ~node_bdd --> ~func_bdd
                fp_reduced_STG &=  ((node_bdd | ~func_bdd))
        else:
            # not in retained set, apply the usual characterization
            fp_reduced_STG &=  ((node_bdd & func_bdd) | (~node_bdd & ~func_bdd))

    return list(fp_reduced_STG.satisfy_all())

# Example Boolean network
# variables = ["A", "B", "C"]
boolean_functions = {
    "x1": "x1 & x2 & x3",
    "x2": "x1 | ~x3",
    "x3": "(x2 & ~x3) | (x1 & ~x2 & ~x3) | (x1 & x2 & x3)"
}

boolean_network = construct_boolean_network(boolean_functions)
fixed_points = compute_stg_fixed_points(boolean_network)

# fixed_points = compute_stg_fixed_points(boolean_functions)
print ("fixed_points: " + str(fixed_points))

print("\n\n------------------------------------------")

list_var = []
for i in range(len(list(boolean_functions.keys()))):
    list_var.append(exprvar(list(boolean_functions.keys())[i]))
# list_var = exprvars('x', 3)
print ("list_var: " + str(list_var))

retained_set = find_retained_set(list_var)
print ("retained_set: " + str(retained_set))

F = compute_stg_minus_fixed_points(boolean_network, retained_set)
print ("F= " + str(F))

# Compute State Transition Graph
# -----------------------------
def compute_bdd(s):
    bddS = 1
    for var, val in s.items():
        if val == 1:
            bddS &= var
        else:
            bddS &= ~var
    return bddS

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

def compute_translation_relation(boolean_network):
    # stg = nx.DiGraph()
    # list_str = list(boolean_network.keys())
    list_bddvar = list(boolean_network.keys())
    states = generate_all_states(tuple(list_bddvar))
    print (states)

    result = set()

    for state in states:
        next_state = state.copy()

        # Create the next_state
        for node in boolean_network.keys():
            next_state[bddvar('next_' + str(node))] = next_state[node]
            del next_state[node]
        
        # Update each next state
        for node, function in boolean_network.items():
            next_state_1 = next_state.copy()
            next_state_1[bddvar('next_' + str(node))] = function.restrict(state)
        # print (result)
    return result

# END Computing STG -----------------------------
compute_stg_bdd(boolean_network)
print("----++++----++++----++++----")
# # Check the reachability
# # -----------------------------

# def compute_bdd(s):
#     bddS = 1
#     for node_var, node_val in s.items():
#         if node_val == 1:
#             bddS &= node_var
#         else:
#             bddS &= ~node_var
#     return bddS

# def compute_transition_relation(boolean_network, dict_s):

def compute_next_states(boolean_network, dict_s):
    list_next_states = []

    for node_var_bdd, node_func_bdd in boolean_network.items():
        next_state = {}

        # Compute the new state at position node_var
        new_val = node_func_bdd.restrict(dict_s)
        next_state[node_var_bdd] = new_val

        # Keep the others value
        for s_var, s_val in dict_s.items():
            if s_var != node_var_bdd:
                next_state[s_var] = s_val

        list_next_states.append(next_state)

    return list_next_states

def compute_next_states_1(boolean_network, dict_s):
    list_next_states = []

    for node_var_bdd, node_func_bdd in boolean_network.items():
        print (bdd2expr(node_func_bdd).simplify())

    return list_next_states

def is_reachable(boolean_network, s1, s2):
    
    # list_next_state = compute_next_states(boolean_network, s1)
    compute_next_states_1(boolean_network, s1)
    for node_var_bdd, node_func_bdd in boolean_network.items():
        if node_var_bdd not in s1:
            s1[node_var_bdd] = 1

    visited = {compute_bdd(s1)}
    queue = [s1]

    while queue:
        curr = queue.pop()

        if str(compute_bdd(curr) & compute_bdd(s2)) != "0":
            print ("YES: " + str(curr) + " ----> " + str(s2))
            print ("compute_bdd: " 
                + str(compute_bdd(curr) & compute_bdd(s2)))
            return True
        for elm in compute_next_states(boolean_network, curr):
            if compute_bdd(elm) not in visited:
                visited.add(compute_bdd(elm))
                queue.append(elm)
    print ("NO: " + str(s1) + " --x--> " + str(s2))
    return False

# -----------------------------
print("--------------")

print(is_reachable(boolean_network, F[1], fixed_points[0]))
# print("----")
# print(is_reachable_2(boolean_functions, F[1], fixed_points[0]))
print("--------------")
# is_reachable_2(boolean_functions, F[0], F[1])
print(is_reachable(boolean_network, F[0], F[1]))
# print("----")
# print(is_reachable_2(boolean_functions, F[0], F[1]))
