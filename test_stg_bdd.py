import itertools
from pyeda.inter import *

# Compute State Transition Graph
# -----------------------------
def find_assignment(B):
    assignment = []
    
    for bi in B:
        fi = bi  # fi is the Boolean function associated with bi
        
        ctrue = count_satisfying_assignments(fi)
        cfalse = 2 ** len(fi.inputs) - ctrue
        
        if ctrue > cfalse:
            assignment.append(1)
        elif ctrue < cfalse:
            assignment.append(0)
        else:
            assignment.append(random.choice([0, 1]))
    
    return tuple(assignment)
# END Computing STG -----------------------------


# Example Boolean network
variables = ["A", "B", "C"]
boolean_functions = {
    "A": "A & B & C",
    "B": "A | ~C",
    "C": "(B & ~C) | (A & ~B & ~C) | (A & B & C)"
}

# string_ss = "(B & C) & (A | C) & ~B"
def compute_stg_2(boolean_network):
    total_func = bddvar('x')
    total_func = total_func.restrict({total_func:1})
    cyclic_attractor = total_func
    for k, v in boolean_network.items():
        stg_bdd_node = bddvar(k)
        stg_bdd_function = expr2bdd(expr(v))
        total_func &= (stg_bdd_node & stg_bdd_function) | (~stg_bdd_node & ~stg_bdd_function)
        cyclic_attractor ^= (stg_bdd_node & ~stg_bdd_function)
        
        # {000, 010, 011, 001})
        if len(list(cyclic_attractor.satisfy_all())) > 0:
            print(list(cyclic_attractor.satisfy_all()))


    if len(list(total_func.satisfy_all())) > 0:
        print(list(total_func.satisfy_all()))

    

print("\n\n------------------------------------------")

compute_stg_2(boolean_functions)

