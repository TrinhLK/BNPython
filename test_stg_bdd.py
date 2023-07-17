import itertools
from pyeda.inter import *
from random import randint, choice
import random

# Compute B
# -----------------------------
def count_satisfying_assignments(fi):
    fi_bdd = expr2bdd(fi)
    sols = fi_bdd.satisfy_all()
    count = 0
    for elm in sols:
        count = count + 1
    
    return count

def find_assignment(B):
    assignment = []
    result = {}
    for bi in B:
        fi = bi  # fi is the Boolean function associated with bi
        # print ("bi: " + str(bi) + "\t" + str(type(bi)))
        bi_bddvar = bddvar(str(bi))
        ctrue = count_satisfying_assignments(fi)
        cfalse = 2 ** len(fi.inputs) - ctrue
        
        if ctrue > cfalse:
            assignment.append(1)
            result[bi_bddvar] = 1
        elif ctrue < cfalse:
            assignment.append(0)
            result[bi_bddvar] = 0
        else:
            assignment.append(random.choice([0, 1]))
            result[bi_bddvar] = random.choice([0, 1])
    # print("result: " + str(result))
    return result
# END B -----------------------------

# Example Boolean network
# variables = ["A", "B", "C"]
boolean_functions = {
    "x1": "x1 & x2 & x3",
    "x2": "x1 | ~x3",
    "x3": "(x2 & ~x3) | (x1 & ~x2 & ~x3) | (x1 & x2 & x3)"
}

# boolean_functions = {
#     "A": "A & B & C",
#     "B": "A | ~C",
#     "C": "(B & ~C) | (A & ~B & ~C) | (A & B & C)"
# }

# x1, x1 & x2 & x3
# x2, x1 | ~x3
# x3, (x2 & ~x3) | (x1 & ~x2 & ~x3) | (x1 & x2 & x3)

# string_ss = "(B & C) & (A | C) & ~B"
def compute_stg_fixed_points(boolean_network):
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


def compute_stg_minus_fixed_points(boolean_network, set_B):
    total_func = bddvar('x')
    total_func = total_func.restrict({total_func:1})
    # cyclic_attractor = total_func
    # for k, v in set_B.items():
    #     print (str(k) + "\t" + str(type(k)))
    #     print (str(v) + "\t" + str(type(v)))
    for k, v in boolean_network.items():
        stg_bdd_node = bddvar(k)
        stg_bdd_function = expr2bdd(expr(v))
        # print (type(set_B))
        # print (type(stg_bdd_function))

        print(stg_bdd_node.restrict(set_B))
        # if stg_bdd_function.restrict(set_B) == 1:
            # continue
            # total_func &= (stg_bdd_node & stg_bdd_function) | (~stg_bdd_node & ~stg_bdd_function)
        # cyclic_attractor ^= (stg_bdd_node & ~stg_bdd_function)
        total_func &= (stg_bdd_node & stg_bdd_function) | (~stg_bdd_node & ~stg_bdd_function)
        total_func |= (stg_bdd_node.restrict(set_B) != stg_bdd_function.restrict(set_B))
        # {000, 010, 011, 001})
        # if len(list(cyclic_attractor.satisfy_all())) > 0:
        #     print(list(cyclic_attractor.satisfy_all()))


    if len(list(total_func.satisfy_all())) > 0:
        print(list(total_func.satisfy_all()))

print("\n\n------------------------------------------")

compute_stg_fixed_points(boolean_functions)

list_var = []
for i in range(len(list(boolean_functions.keys()))):
    list_var.append(exprvar(list(boolean_functions.keys())[i]))
# list_var = exprvars('x', 3)
print ("list_var: " + str(list_var))

set_B = find_assignment(list_var)
print (set_B)

compute_stg_minus_fixed_points(boolean_functions, set_B)

