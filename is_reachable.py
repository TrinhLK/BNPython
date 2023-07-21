from pyeda.inter import *

def construct_boolean_network(boolean_network):
    # Convert the dictionary of Boolean expressions into a dictionary of PyEDA BDDs
    bdd_network = {}
    for var, e_expr in boolean_network.items():
        bdd_network[var] = expr2bdd(expr(e_expr))
    return bdd_network

def can_reach_state(s1, s2, boolean_network):
    # Create PyEDA BDDs for s1 and s2
    # s1_bdd = expr2bdd(exprvar(var, val) for var, val in s1.items())
    # s2_bdd = expr2bdd(exprvar(var, val) for var, val in s2.items())
    
    # Perform reachability check from s1 to s2
    reachability_bdd = s1_bdd & s2_bdd

    # Check if the intersection of s1 and s2 BDDs is non-empty
    return not reachability_bdd.is_zero()

# Define the Boolean network, s1, and s2
boolean_network = {
    "x1": "x1 & x2 & x3",
    "x2": "x1 | ~x3",
    "x3": "(x2 & ~x3) | (x1 & ~x2 & ~x3) | (x1 & x2 & x3)"
}

s1 = {"x1": 1, "x2": 0, "x3": 0}
s2 = {"x1": 1, "x2": 1, "x3": 1}

# Construct the PyEDA Boolean network
bdd_network = construct_boolean_network(boolean_network)

# Check if s1 can reach s2 in the Boolean network
result = can_reach_state(s1, s2, bdd_network)
print(result)  # Output will be True if s1 can reach s2, False otherwise