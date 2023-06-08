import networkx as nx
import itertools

def read_boolean_network(file_path):
    boolean_network = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('#') or line.strip() == '':
                continue
            node, function = line.strip().split('=')
            boolean_network[node.strip()] = function.strip()
    return boolean_network

def compute_stg(boolean_network, time_steps):
    stg = nx.DiGraph()
    states = generate_all_states(boolean_network.keys())
    for state in states:
        stg.add_node(state)
        next_state = update_state(state, boolean_network)
        stg.add_edge(state, next_state)
    return stg

def generate_all_states(nodes):
    all_states = list(itertools.product([0, 1], repeat=len(nodes)))
    return [tuple(state) for state in all_states]

def update_state(state, boolean_network):
    updated_state = list(state)
    for node in boolean_network:
        function = boolean_network[node]
        dependencies = [dep.strip() for dep in function.split('AND') + function.split('OR') + function.split('XOR')]
        inputs = [state[list(boolean_network.keys()).index(dep)] for dep in dependencies]
        updated_state[list(boolean_network.keys()).index(node)] = evaluate_function(function, inputs)
    return tuple(updated_state)

def evaluate_function(function, inputs):
    expression = function
    for i in range(len(inputs)):
        expression = expression.replace(str(i), str(inputs[i]))
    return eval(expression)

# Example usage
file_path = 'boolean_network_ex.txt'  # Path to the input file
time_steps = 5  # Number of time steps to simulate

boolean_network = read_boolean_network(file_path)
stg = compute_stg(boolean_network, time_steps)

# Print the nodes and edges of the STG
print("Nodes:", stg.nodes())
print("Edges:", stg.edges())
