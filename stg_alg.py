import networkx as nx

# Read the asynchronous Boolean network from the input file
def read_network(file_path):
    network = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                variable, function = line.split('=')
                network[variable.strip()] = function.strip()
    return network

# Compute the state transition graph (STG) of the asynchronous Boolean network
def compute_stg(network):
    stg = nx.DiGraph()
    initial_state = ''.join(['{}={}'.format(var, '0') for var in network.keys()])
    print (str(initial_state))
    stg.add_node(initial_state)

    while True:
        updated = False
        nodes = list(stg.nodes)  # Copy the list of nodes
        print (nodes)
        for node in nodes:
            state = dict(var.split('=', 1) for var in node.split(','))
            for variable, function in network.items():
                # print (variable + "\t" + function + "\t" + str(state))
                value = eval(function, state)
                if state[variable] != str(int(value)):
                    new_state = node.replace('{}={}'.format(variable, state[variable]), '{}={}'.format(variable, str(int(value))))
                    if new_state not in stg.nodes:
                        stg.add_node(new_state)
                    stg.add_edge(node, new_state)
                    updated = True

        if not updated:
            break

    return stg

# Example usage
network_file = "boolean_network.txt"
network = read_network(network_file)
stg = compute_stg(network)

# Print the state transition graph
print("State Transition Graph:")
for node in stg.nodes:
    print(node)
    for successor in stg.successors(node):
        print("-->", successor)
