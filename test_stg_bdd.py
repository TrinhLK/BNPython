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

def find_retained_set(B):
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

# string_ss = "(B & C) & (A | C) & ~B"
def compute_stg_fixed_points(boolean_network):
    total_func = bddvar('x')
    total_func = total_func.restrict({total_func:1})

    for k, v in boolean_network.items():
        stg_bdd_node = bddvar(k)
        stg_bdd_function = expr2bdd(expr(v))
        total_func &= (stg_bdd_node & stg_bdd_function) | (~stg_bdd_node & ~stg_bdd_function)

    return list(total_func.satisfy_all())

def compute_stg_minus_fixed_points(boolean_network, set_B):

    fp_reduced_STG = 1

    for node, func in boolean_network.items():
        node_bdd = bddvar(node)
        func_bdd = expr2bdd(expr(func))
        node = bddvar(node)

        if node in retained_set:
            if retained_set[node] == False:
                # B[node] = 0, only need the condition node_bdd --> func_bdd
                fp_reduced_STG &=  ((~node_bdd | func_bdd))
            else:
                # B[node] = 1, only need the condition ~node_bdd --> ~func_bdd
                fp_reduced_STG &=  ((node_bdd | ~func_bdd))
        else:
            # not in retained set, apply the usual characterization
            fp_reduced_STG &=  ((node_bdd & func_bdd) | (~node_bdd & ~func_bdd))

    # print (list(fp_reduced_STG.satisfy_all()))
    return list(fp_reduced_STG.satisfy_all())


fixed_points = compute_stg_fixed_points(boolean_functions)
print ("fixed_points: " + str(fixed_points))

print("\n\n------------------------------------------")

list_var = []
for i in range(len(list(boolean_functions.keys()))):
    list_var.append(exprvar(list(boolean_functions.keys())[i]))
# list_var = exprvars('x', 3)
print ("list_var: " + str(list_var))

retained_set = find_retained_set(list_var)
print ("retained_set: " + str(retained_set))

F = compute_stg_minus_fixed_points(boolean_functions, retained_set)
print ("F= " + str(F))

# # Check the reachability
# # -----------------------------
def is_reachable(boolean_functions, s1, s2):
    #Initiate BDD with s1
    bddS1 = 1
    for v in s1:
        if s1[v] == 1:
            bddS1 &= v 
        else:
            bddS1 &= ~v

    bddS2 = 1
    for v in s2:
        if s2[v] == 1:
            bddS2 &= v
        else:
            bddS2 &= ~v

    for i in range(10):
        # bddS1_prev = bddS1
        for var, func in boolean_functions.items():
            tmpbdd_func = expr2bdd(expr(func)).restrict(s1)
            bddS1 &= tmpbdd_func

        if bddS1 == (bddS2):
            print("Break after " + str(i))
            break

    
    if bddS2 != bddS1:
        print ("NO: " + str(s1) + " --x--> " + str(s2))
    else:
        print ("YES: " + str(s1) + " ----> " + str(s2))
# -----------------------------
is_reachable(boolean_functions, F[1], fixed_points[0])
print("--------------")
is_reachable(boolean_functions, F[0], F[1])
