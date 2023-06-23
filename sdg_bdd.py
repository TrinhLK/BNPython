from pyeda.boolalg.bdd import expr2bdd, exprvar
import networkx as nx

# Define the Boolean network equations
boolean_network = [
    exprvar('x1') & exprvar('x2') & exprvar('x3'),
    exprvar('x1') | ~exprvar('x3'),
    (exprvar('x2') & ~exprvar('x3')) | (exprvar('x1') & ~exprvar('x2') & ~exprvar('x3')) | (exprvar('x1') & exprvar('x2') & exprvar('x3'))
]

# Create an empty nx.DiGraph object for the SDG
sdg = nx.DiGraph()

# Create a dictionary to map variables to BDD nodes
var_to_node = {}

# Iterate over each equation in the Boolean network
for equation in boolean_network:
    # Convert the equation to BDD
    bdd = expr2bdd(equation)

    # Get the input variables of the BDD
    input_vars = bdd.support

    # Iterate over the input variables and add the edges to the SDG
    for var in input_vars:
        var_name = var.name

        # Check if the variable has a corresponding BDD node in the dictionary
        if var_name in var_to_node:
            node = var_to_node[var_name]
        else:
            # Create a new BDD variable for the variable
            node = var
            var_to_node[var_name] = node

        # Get the successors of the node
        successors = bdd.edges(node)

        # Iterate over the successors and add edges to the SDG
        for successor in successors:
            successor_var = successor[1]

            # Add an edge to the SDG with the sign based on the polarity of the successor
            sdg.add_edge(var_name, successor_var.name, sign=1)

# Print the SDG
for edge in sdg.edges(data=True):
    source, target, data = edge
    print(f"{source} --> {target} (sign: {data['sign']})")
