import networkx as nx
import itertools

def read_boolean_network(file_path):
    boolean_network = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('#') or line.strip() == '':
                continue
            line = line.replace('~', 'not ')
            line = line.replace('&', ' and ')
            line = line.replace('|', ' or ')
            line = line.replace('^', ' ^ ')
            node, function = line.strip().split('=')
            boolean_network[node.strip()] = function.strip()
    return boolean_network

def compute_stg(boolean_network):
    stg = nx.DiGraph()
    states = generate_all_states(boolean_network.keys())
    # print ("states: " + str(states))
    for state in states:
        print ("----------------------------------------------------------")
        print ("initial state: " + str(state))
        stg.add_node(state)
        # next_state = update_state(state, boolean_network)
        # stg.add_edge(state, next_state)
        for node in boolean_network:
            updated_state = list(state)
            function = boolean_network[node]
            terms = function.split()
            inputs_dict = {}
            for term in terms:
                if term in ('and', 'or', '^', 'not'):
                    continue
                input_node = term.strip('()')
                input_value = state[list(boolean_network.keys()).index(input_node)]
                inputs_dict[input_node] = input_value
            updated_state[list(boolean_network.keys()).index(node)] = evaluate_function_using_dict(function, inputs_dict)
            next_state = tuple(updated_state)
            stg.add_edge(state, next_state)
    return stg

def generate_all_states(nodes):
    all_states = list(itertools.product([0, 1], repeat=len(nodes)))
    return [tuple(state) for state in all_states]

def evaluate_function_using_dict(function, inputs_dict):

    for node, value in inputs_dict.items():
        function = function.replace(node, str(value))
    print (function + " = " + str(int(eval(function))))  
    return int(eval(function))

# Example usage
file_path = 'boolean_network.txt' 

boolean_network = read_boolean_network(file_path)
stg = compute_stg(boolean_network)

# Print the nodes and edges of the STG
print("Nodes:", stg.nodes())
print("Edges:", stg.edges())
