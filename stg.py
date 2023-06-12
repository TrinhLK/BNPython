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
        terms = function.split()
        inputs = []
        for term in terms:
            if term in ('AND', 'OR', 'XOR', 'NOT'):
                continue
            input_node = term.strip('()')
            input_value = state[list(boolean_network.keys()).index(input_node)]
            inputs.append(input_value)
        updated_state[list(boolean_network.keys()).index(node)] = evaluate_function(function, inputs)
    return tuple(updated_state)

def evaluate_function(function, inputs):
    result = inputs[0]
    index = 1
    while index < len(inputs):
        operator = function.split()[index - 1]
        if operator == 'AND':
            result = result and inputs[index]
        elif operator == 'OR':
            result = result or inputs[index]
        elif operator == 'XOR':
            result = result ^ inputs[index]
        elif operator == 'NOT':
            result = not inputs[index]
        index += 1
    return result

# Example usage
file_path = 'boolean_network.txt'  # Path to the input file
time_steps = 5  # Number of time steps to simulate

boolean_network = read_boolean_network(file_path)
stg = compute_stg(boolean_network, time_steps)

# Print the nodes and edges of the STG
print("Nodes:", stg.nodes())
print("Edges:", stg.edges())
