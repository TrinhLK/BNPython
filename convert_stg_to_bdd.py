import networkx as nx
from pyeda.boolalg.bdd import expr2bdd

def check_reachability(state_transition_bdd, initial_state, target_state):
    current_states = initial_state

    while True:
        next_states = state_transition_bdd.restrict(current_states)

        # If the target state is reachable, return True
        if target_state & next_states != expr2bdd(0):
            return True

        # If no new states can be reached, return False
        if next_states == current_states:
            return False

        current_states = next_states

# Example usage
G = nx.DiGraph([(1, 0), (1, 3), (1, 2), (2, 3), (2, 0), (3, 0)])

# Define the variables and expressions for the BDD
variables = sorted(list(set(G.nodes)))
print (variables)
expressions = {}
for node in G.nodes:
    expressions[node] = expr2bdd("v", node)

bdd = expr2bdd(1)  # Initialize the BDD with True

# Define the initial and target states
initial_state = expressions[1]  # Node A
target_state = expressions[0]  # Node B

# Define the state transition function
for edge in G.edges:
    source, target = edge
    bdd &= expressions[source].compose({f"v_{source}": expressions[target]})

# Check reachability
is_reachable = check_reachability(bdd, initial_state, target_state)

if is_reachable:
    print("Node B is reachable from Node A in the state transition graph.")
else:
    print("Node B is not reachable from Node A in the state transition graph.")
