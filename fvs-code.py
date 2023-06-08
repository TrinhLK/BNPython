def read_boolean_network(file_path):
    boolean_network = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('#') or line.strip() == '':
                continue
            node, function = line.strip().split('=')
            boolean_network[node.strip()] = function.strip()
    return boolean_network

def compute_fvs(boolean_network):
    fvs = set()
    for node in boolean_network:
        modified_network = boolean_network.copy()
        del modified_network[node]
        if not has_feedback_loop(modified_network):
            fvs.add(node)
    return fvs

def has_feedback_loop(boolean_network):
    for node in boolean_network:
        if evaluate_node(node, boolean_network, set()):
            return True
    return False

def evaluate_node(node, boolean_network, visited):
    if node in visited:
        return True
    visited.add(node)
    function = boolean_network[node]
    dependencies = [dep.strip() for dep in function.split('AND') + function.split('OR') + function.split('XOR')]
    for dep in dependencies:
        if dep not in boolean_network:
            continue
        if evaluate_node(dep, boolean_network, visited):
            return True
    visited.remove(node)
    return False

# Example usage
file_path = 'CAC.txt'  # Path to the input file
boolean_network = read_boolean_network(file_path)
fvs = compute_fvs(boolean_network)
print("Feedback Vertex Set:", fvs)