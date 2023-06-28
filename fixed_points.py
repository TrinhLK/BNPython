from pyeda.inter import *
import networkx as nx

stg = nx.DiGraph()

stg.add_node('00')
stg.add_node('01')
stg.add_node('10')
stg.add_node('11')
stg.add_edge('00','00')
stg.add_edge('00','10')
stg.add_edge('10','00')
stg.add_edge('01','00')
stg.add_edge('10','11')
stg.add_edge('11','11')

stg_1 = stg

def find_fixed_points(stg):
    not_fp = []
    for edge in stg.edges:
        print (edge)
        if edge[0] != edge[1]:
            # print (str(edge[0]))
            not_fp.append(edge[0])

    print (set(stg.nodes()) - set(not_fp))

find_fixed_points(stg)
print ("-----")
stg_1.remove_edge('01', '00')
find_fixed_points(stg_1)

# def find_fixed_points(transition_functions):
#     num_states = len(transition_functions)
#     vars = bddvars('x', num_states)  # Variable names for each state

#     # Create initial state as a BDD
#     initial_state = expr2bdd(vars[0])

#     # Iterate until a fixed point is reached
#     while True:
#         next_state = initial_state
#         for i in range(num_states):
#             # Compute the next state based on the transition function
#             next_state &= transition_functions[i](vars)

#         if next_state.equivalent(initial_state):
#             # Found a fixed point
#             break

#         initial_state = next_state

#     # Convert the fixed point BDD to a list of states
#     fixed_points = []
#     for i in range(num_states):
#         state = [int(val) for val in vars[i].satisfy_all()]
#         fixed_points.append(state)

#     return fixed_points

# # Example transition functions
# def transition_function1(states):
#     return (states[0] & states[1]) | (~states[0] & ~states[1])

# def transition_function2(states):
#     return ~states[0] | states[1]

# def transition_function3(states):
#     return states[1]

# # Define the transition functions
# transition_functions = [transition_function1, transition_function2, transition_function3]

# # Find the fixed points
# fixed_points = find_fixed_points(transition_functions)

# # Print the fixed points
# for point in fixed_points:
#     print("Fixed point:", point)