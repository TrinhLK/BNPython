import networkx as nx

def compute_signed_directed_graph(abn):
    signed_directed_graph = nx.DiGraph()

    for equation in abn:
        equation = equation.strip()
        parts = equation.split('=')
        target = parts[0].strip()
        function = parts[1].strip()

        if target not in signed_directed_graph:
            signed_directed_graph.add_node(target)

        temp_functions = function.replace(' AND ', ', ')
        temp_functions = temp_functions.replace(' OR ', ', ')
        temp_functions = temp_functions.replace(' XOR ', ', ')
        temp_functions = temp_functions.replace(')', '')
        temp_functions = temp_functions.replace('(', '')
        dependencies = temp_functions.split(', ')

        print ("dependency: " + str(dependencies))
        for dependency in dependencies:
            sign = 1
            if 'NOT' in dependency:
                sign = -1
                dependency = dependency.replace('NOT ', '')

            if ' AND ' in dependency:
                and_parts = dependency.split(' AND ')
                for part in and_parts:
                    if part not in signed_directed_graph:
                        signed_directed_graph.add_node(part)
                    signed_directed_graph.add_edge(part, target, sign=sign)
            elif ' XOR ' in dependency:
                xor_parts = dependency.split(' XOR ')
                for part in xor_parts:
                    if part not in signed_directed_graph:
                        signed_directed_graph.add_node(part)
                    signed_directed_graph.add_edge(part, target, sign=sign)
                    signed_directed_graph.add_edge(target, part, sign=sign)
            else:
                if dependency not in signed_directed_graph:
                    signed_directed_graph.add_node(dependency)
                signed_directed_graph.add_edge(dependency, target, sign=sign)

    return signed_directed_graph

# Example ABN
abn = [
    'x1 = x1 AND x2 AND x3',
    'x2 = x1 OR NOT x3',
    'x3 = (x2 AND NOT x3) OR (x1 AND NOT x2 AND NOT x3) OR (x1 AND x2 AND x3)'
]

# Compute the signed directed graph
signed_directed_graph = compute_signed_directed_graph(abn)

# Print the signed directed graph
print("Signed Directed Graph:")
for edge in signed_directed_graph.edges(data=True):
    source, target, data = edge
    print(f"{source} --> {target} (sign: {data['sign']})")
