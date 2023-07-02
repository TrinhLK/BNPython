import itertools
from pyeda.inter import *

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
    # print(result)
    return result

def find_key_from_val(my_dict, val):
    # list out keys and values separately
    key_list = list(my_dict.keys())
    val_list = list(my_dict.values())
     
    # print key with val 100
    position = val_list.index(val)
    return key_list[position]
    # print(key_list[position])

def compute_stg(boolean_network):
    # stg = nx.DiGraph()
    list_str = list(boolean_network.keys())
    list_bddvar = [bddvar(elm) for elm in list_str]
    states = generate_all_states(tuple(list_bddvar))
    stg_bdd_nodes = dict()
    for i in range(len(states)):
        x_i = bddvar('x',i)
        stg_bdd_nodes[x_i] = states[i]

    print(stg_bdd_nodes)
    stg_bdd_edges = set()
    # print(stg_bdd_edges)
    for node, function in boolean_network.items():
        expression = expr2bdd(expr(boolean_network[node]))  # Convert to BDD
        print ("node: " + str(type(node)) + str(node) )
        for k,v in stg_bdd_nodes.items():
            my_updated_state = v.copy()
            bdd_assignment = expression.restrict(v)
            my_updated_state[bddvar(node)] = int(bdd_assignment)
            print (str(v) + "-->" + str(my_updated_state))
            edge = find_key_from_val(stg_bdd_nodes, v) & find_key_from_val(stg_bdd_nodes, my_updated_state)
            stg_bdd_edges.add(edge)
    # return stg
    print ("set size: " + str(len(stg_bdd_edges)))
    print (stg_bdd_nodes)
    for edge in stg_bdd_edges:
        for k,v in stg_bdd_nodes.items():
            flag = True
            next_node = edge.restrict(v)
            if next_node == k:
                print (next_node)
            # for edge in stg_bdd_edges:
            #     next_node = edge.restrict(v)
            #     print ("next_node: " + str(next_node))
            #     if k == next_node

    # return stg
# END Computing STG -----------------------------

def find_fixed_points(state_transition_bdd, num_states):
    fixed_points = []

    for state in range(num_states):
        next_state = state_transition_bdd.restrict(state)

        # If the current state is equal to the next state, it is a fixed point
        if state == next_state:
            fixed_points.append(state)

    return fixed_points

# Example Boolean network
variables = ["A", "B", "C"]
boolean_functions = {
    "A": "A & B & C",
    "B": "A | ~C",
    "C": "(B & ~C) | (A & ~B & ~C) | (A & B & C)"
}

compute_stg(boolean_functions)
# string_ss = "(B & C) & (A | C) & ~B"

# # Define the number of states (2^N, where N is the number of variables)
# num_states = 2 ** len(variables)

# # Construct the BDD for the state transition function
# state_transition_bdd = expr2bdd(expr(string_ss))

# # Find fixed points
# fixed_points = find_fixed_points(state_transition_bdd, num_states)

print("Fixed points:")
for point in fixed_points:
    print(f"State: {point}")
