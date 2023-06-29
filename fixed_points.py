import networkx as nx
from pyeda.inter import *

def find_fixed_points(stg):
    num_vars = len(stg.nodes())
    num_next_vars = num_vars  # Number of variables for the next state

    bdd_vars = exprvars('x', num_vars)  # Declare variables for the current state
    bdd_next_vars = exprvars('y', num_next_vars)  # Declare variables for the next state

    # Construct the Boolean formula representing the STG transitions
    formula = Or(*[And(bdd_vars[list(stg.nodes()).index(u)], bdd_next_vars[list(stg.nodes()).index(v)]) for u, v in stg.edges()])

    # Encode the fixed point condition: current state is equal to the next state
    fixed_point = And(bdd_vars[i] == bdd_next_vars[i] for i in range(num_vars))

    # Convert the formula and fixed point condition to BDDs
    formula_bdd = expr2bdd(formula)
    fixed_point_bdd = expr2bdd(fixed_point)
    print (formula)
    print (fixed_point)
    # Find the satisfying assignment using BDD
    solution = (formula_bdd).satisfy_all()

    # Interpret the solutions as the fixed point states
    fixed_point_states = []
    for assignment in solution:
        print ("assignment: " + str(assignment))
        print (bdd_vars)
        # state = [bool(assignment[bdd_var]) for bdd_var in bdd_vars]
        # fixed_point_states.append(state)

    return fixed_point_states

# Example STG
stg = nx.DiGraph()

stg.add_node((0, 0))
stg.add_node((0, 1))
stg.add_node((1, 0))
stg.add_node((1, 1))

stg.add_edge((0, 0), (0, 0))
stg.add_edge((0, 0), (1, 0))
stg.add_edge((1, 0), (0, 0))
stg.add_edge((0, 1), (0, 0))
stg.add_edge((1, 0), (1, 1))
stg.add_edge((1, 1), (1, 1))

fixed_points = find_fixed_points(stg)
print("Fixed Points:")
for state in fixed_points:
    print(state)



# from pyeda.inter import *
# import networkx as nx

# stg = nx.DiGraph()

# stg.add_node((0,0))
# stg.add_node((0,1))
# stg.add_node((1,0))
# stg.add_node((1,1))
# stg.add_edge((0,0),(0,0))
# stg.add_edge((0,0),(1,0))
# stg.add_edge((1,0),(0,0))
# stg.add_edge((0,1),(0,0))
# stg.add_edge((1,0),(1,1))
# stg.add_edge((1,1),(1,1))

# stg_1 = stg
# stg_2 = nx.DiGraph()
# stg_2.add_edges_from(stg.edges)
# stg_2.remove_edge((0,1),(0,0))
# def find_fixed_points(stg):
#     not_fp = []
#     for edge in stg.edges:
#         if edge[0] != edge[1]:
#             not_fp.append(edge[0])
#     return set(stg.nodes()) - set(not_fp)

# find_fixed_points(stg)
# print ("-----")

# find_fixed_points(stg_2)
# print (len(stg_2.edges))

# # def find_fixed_points(transition_functions):
# #     num_states = len(transition_functions)
# #     vars = bddvars('x', num_states)  # Variable names for each state

# #     # Create initial state as a BDD
# #     initial_state = expr2bdd(vars[0])

# #     # Iterate until a fixed point is reached
# #     while True:
# #         next_state = initial_state
# #         for i in range(num_states):
# #             # Compute the next state based on the transition function
# #             next_state &= transition_functions[i](vars)

# #         if next_state.equivalent(initial_state):
# #             # Found a fixed point
# #             break

# #         initial_state = next_state

# #     # Convert the fixed point BDD to a list of states
# #     fixed_points = []
# #     for i in range(num_states):
# #         state = [int(val) for val in vars[i].satisfy_all()]
# #         fixed_points.append(state)

# #     return fixed_points

# # # Example transition functions
# # def transition_function1(states):
# #     return (states[0] & states[1]) | (~states[0] & ~states[1])

# # def transition_function2(states):
# #     return ~states[0] | states[1]

# # def transition_function3(states):
# #     return states[1]

# # # Define the transition functions
# # transition_functions = [transition_function1, transition_function2, transition_function3]

# # # Find the fixed points
# # fixed_points = find_fixed_points(transition_functions)

# # # Print the fixed points
# # for point in fixed_points:
# #     print("Fixed point:", point)