import networkx as nx
from pyeda.boolalg.bdd import exprvar
from pyeda.boolalg.expr import *


def compute_sdg_from_abn(abn):
    # Extract variables from ABN equations
    variables = set()
    for equation in abn:
        equation = equation.strip()
        parts = equation.split('=')
        function = parts[1].strip()
        tmp_var = function.replace(' AND ', ' ')
        tmp_var = tmp_var.replace(' OR ', ' ')
        tmp_var = tmp_var.replace(' XOR ', ' ')
        tmp_var = tmp_var.replace(' NOT ', ' ')
        tmp_var = tmp_var.replace(' & ', ' ')
        tmp_var = tmp_var.replace(' | ', ' ')
        tmp_var = tmp_var.replace(' ~ ', ' ')
        variables.update(set(tmp_var.replace('(', '').replace(')', '').split()))

    print ("variables: " + str(variables))
    # Create BDD variables
    var_map = {var: exprvar(var) for var in variables}

    # Construct BDDs for each equation
    bdds = {}
    for equation in abn:
        equation = equation.strip()
        parts = equation.split('=')
        target = parts[0].strip()
        function = parts[1].strip()

        # Build BDD for the Boolean function
        bdd = expr(function).to_bdd(var_map)

        # Store BDD in the dictionary
        bdds[target] = bdd

    # Create the Signed Directed Graph (SDG)
    sdg = nx.DiGraph()

    # Traverse the BDDs to generate SDG edges
    for target, bdd in bdds.items():
        # Get the variable associated with the target
        var = var_map[target]

        # Traverse the BDD nodes
        traverse_bdd(bdd, sdg, target, var)

    return sdg

def traverse_bdd(bdd, sdg, source, var):
    # Terminal case: BDD is a constant (0 or 1)
    if bdd.is_zero() or bdd.is_one():
        return

    # Extract low and high branches of the BDD
    low_bdd = bdd.low
    high_bdd = bdd.high

    # Extract the variable associated with the low branch
    low_var = low_bdd.top

    # Extract the variable associated with the high branch
    high_var = high_bdd.top

    # Determine the sign of the edge
    sign = 1 if high_var == var else -1

    # Add edge to the SDG
    sdg.add_edge(source, high_var, sign=sign)

    # Recursively traverse the low and high branches
    traverse_bdd(low_bdd, sdg, source, low_var)
    traverse_bdd(high_bdd, sdg, source, high_var)

# Example ABN
abn = [
    'x1 = x1 & x2 & x3',
    'x2 = x1 | ~ x3',
    'x3 = (x2 AND NOT x3) OR (x1 AND NOT x2 AND NOT x3) OR (x1 AND x2 AND x3)'
]

# Compute the SDG using BDDs
sdg = compute_sdg_from_abn(abn)

# Print the SDG
print("Signed Directed Graph (SDG):")
for edge in sdg.edges(data=True):
    source, target, data = edge
    print(f"{source} --> {target} (sign: {data['sign']})")
