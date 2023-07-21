import itertools
from pyeda.inter import *
from random import randint, choice
import random
import copy
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
def compute_bdd(s):
    bddS = 1
    for v in s:
        if s[v] == 1:
            bddS |= v
    for v in s:
        if s[v] != 1:
            bddS &= ~v
    return bddS

def is_equivalent(dict1, dict2):
    if len(dict1) <= len(dict2):
        for k, v in dict1.items():
            if dict1[k] != dict2[k]:
                return False
    else:
        for k, v in dict2.items():
            if dict1[k] != dict2[k]:
                return False
    return True

def is_reachable(boolean_functions, s1, s2):
    #Initiate BDD with s1
    next_bddS1 = 1

    for node, func in boolean_functions.items():
        node_bdd = bddvar(node)
        func_bdd = expr2bdd(expr(func))
        node = bddvar(node)

        if node in s1:
            if s1[node] == False:
                # B[node] = 0, only need the condition node_bdd --> func_bdd
                next_bddS1 &=  ((~node_bdd | func_bdd))
            else:
                # B[node] = 1, only need the condition ~node_bdd --> ~func_bdd
                next_bddS1 &=  ((node_bdd | ~func_bdd))

    list_next_states = list(next_bddS1.satisfy_all())
    print(list_next_states)
    # while list_next_states:
    #     next_state = list_next_states.pop()

    for next_state in list_next_states:
        if is_equivalent(next_state, s2):
        # if compute_bdd(s2) & compute_bdd(next_state) != 0:
            print("YESS: " + str(next_state))
        else:
            print("NO" + str(next_state))
    # for v in s1:
    #     if s1[v] == 1:
    #         bddS1 |= v
    # for v in s1:
    #     if s1[v] != 1:
    #         bddS1 &= ~v

    # bddS2 = 1
    # for v in s2:
    #     if s2[v] == 1:
    #         bddS2 |= v
    # for v in s2:
    #     if s2[v] != 1:
    #         bddS2 &= ~v

    # RS = {bddS1}
    # FS = [bddS1]

    # while FS:
    #     curr = FS.pop()
    #     print (str(curr) + "\t" + str(bddS2))
    #     if curr & bddS2 != 0:
    #         return True

    #     list_FS_k1 = []
    #     for var, func in boolean_functions.items():
    #         tmpbdd_func &= (bddvar(var) & expr2bdd(expr(func))) | (~bddvar(var) & ~expr2bdd(expr(func)))
    #     list_FS_k1.append(tmpbdd_func)

    #     for elm in list_FS_k1:
    #         if elm not in RS:
    #             RS.add(elm)
    #             FS.append(elm)

    # print("RS: " + str(RS))


    # for i in range(10):
    #     bddS1_next = bddS1
    #     for var, func in boolean_functions.items():
    #         tmpbdd_func = expr2bdd(expr(func))
    #         bddS1_next = bddS1_next & tmpbdd_func

    #         if bddS1_next & bddS2 != 0:
    #             return True

    # return False
    # if bddS2 != bddS1:
    #     print ("NO: " + str(s1) + " --x--> " + str(s2))
    # else:
    #     print ("YES: " + str(s1) + " ----> " + str(s2))

def is_reachable_1(boolean_functions, s1, s2):
    
    for node, func in boolean_functions.items():
        if bddvar(node) not in s1:
            s1[bddvar(node)] = 1
    print(s1)
    tp_s1 = tuple(s1.values())
    reachable_set = {tp_s1}
    foward_set = [s1]
    path = []
    k = 0
    while foward_set:
        cur = foward_set.pop()
        
        for node, func in boolean_functions.items():
            if bddvar(node) not in s1:
                s1[bddvar(node)] = 1
                cur[bddvar(node)] = 1
        print("--- cur: " + str(cur))
        # next_state = copy.deepcopy(cur)
        
        path.append(cur)
        if cur == s2:
            return True

        list_next_states = []
        for node, func in boolean_functions.items():
            next_state = cur
            # print(node + "\t" + func + "\t" + str(expr2bdd(expr(func)).restrict(s1)))
            next_state[bddvar(node)] = expr2bdd(expr(func)).restrict(s1)
            print("next_state: " + str(next_state))
            tmp_next = copy.deepcopy(next_state)
            print ("check: " + str(tmp_next) + "\t" + str(list_next_states) + ": " + str(is_in(tmp_next, list_next_states)))
            if is_in(tmp_next, list_next_states) == False:
                list_next_states.append(tmp_next)
        # print("---next---")
        print(cur)
        print(list_next_states)
        lns_1 = [i for n, i in enumerate(list_next_states) if i not in list_next_states[n + 1:]]
        print(lns_1)
        break
        # for node, func in boolean_functions.items():
        # print("--- next_state: " + str(next_state))
        for n_state in list_next_states:
            if n_state not in reachable_set:
                reachable_set.append(n_state)
                foward_set.append(n_state)
    return False

def standardize_state(s, boolean_functions):
    for node, func in boolean_functions.items():
        if bddvar(node) not in s:
            s[bddvar(node)] = 1
    tp_node_s = tuple(s.keys())
    int_val = [int(v) for v in list(s.values())]
    # tp_val_s = tuple(s.values())
    my_tuple = (tp_node_s, tuple(int_val))
    # print (my_tuple)
    return my_tuple

def is_in(s, list_s):
    for s_i in list_s:
        if all((s_i.get(k) == v for k, v in s.items())):
            return True
    return False

def is_reachable_3(boolean_functions, s1, s2):
    tmp_s1 = {}
    for k, v in s1.items():
        tmp_s1[str(k)] = v

    tmp_s2 = {}
    for k, v in s2.items():
        tmp_s2[str(k)] = v

    reachable_set = [tmp_s1]
    foward_set = [tmp_s1]
    path = []
    k = 0
    while foward_set:
        cur = foward_set.pop()
        
        for node, func in boolean_functions.items():
            if (node) not in tmp_s1:
                tmp_s1[(node)] = 1
                cur[(node)] = 1
        print("--- cur: " + str(cur))
        # next_state = copy.deepcopy(cur)
        
        path.append(cur)
        if cur == tmp_s2:
            return True

        list_next_states = []
        for node, func in boolean_functions.items():
            next_state = cur
            # print(node + "\t" + func + "\t" + str(expr2bdd(expr(func)).restrict(s1)))
            next_state[(node)] = expr2bdd(expr(func)).restrict(s1)
            print("next_state: " + str(next_state))
            tmp_next = copy.deepcopy(next_state)
            print ("check: " + str(tmp_next) + "\t" + str(list_next_states) + ": " + str(is_in(tmp_next, list_next_states)))
            if is_in(tmp_next, list_next_states) == False:
                list_next_states.append(tmp_next)
        # print("---next---")
        print(cur)
        print(list_next_states)
        lns_1 = [i for n, i in enumerate(list_next_states) if i not in list_next_states[n + 1:]]
        print(lns_1)
        break

def is_reachable_2(boolean_functions, s1, s2):
  
    tp_s1 = standardize_state(s1,boolean_functions)
    tp_s2 = standardize_state(s2,boolean_functions)
    visited = {tp_s1[1]}
    queue = [tp_s1[1]]
    path = []
    while queue:
        curr = queue.pop(0)
        path.append(curr)
        # Check if s2 is visited
        if curr == tp_s2[1]:
            print ("path: " + str(path))
            print (str(s1) + " ----> " + str(s2))
            return True

        list_successor_s1 = []
        for i in range(len(tp_s1[0])):
            new_value = list(curr)
            new_value[i] = int(expr2bdd(expr(boolean_functions[str(tp_s1[0][i])])).restrict(s1))
            list_successor_s1.append(new_value)

        list_successor_s1.sort()
        list_successor_s1 = list(list_successor_s1 for list_successor_s1,_ in itertools.groupby(list_successor_s1))
        print (list_successor_s1)

        for succ in list_successor_s1:
            if tuple(succ) not in visited:
                visited.add(tuple(succ))
                queue.append(tuple(succ))
    print (str(s1) + " --x--> " + str(s2))
    return False


    # print(str(tp_node_s1) + "\t" + str(tp_val_s1))
# -----------------------------
print("--------------")

# is_reachable_2(boolean_functions, F[1], fixed_points[0])
print(is_reachable(boolean_functions, F[1], fixed_points[0]))

print(is_reachable_2(boolean_functions, F[1], fixed_points[0]))
print("--------------")
# is_reachable_2(boolean_functions, F[0], F[1])
print(is_reachable(boolean_functions, F[0], F[1]))

print(is_reachable_2(boolean_functions, F[0], F[1]))
# lns_1 = [i for n, i in enumerate(list_next_states) if i not in list_next_states[n + 1:]]


# inputTuple = (('a','b','c'),(1,2,3))
# result = {inputTuple[0][i] : inputTuple[1][i] for i, _ in enumerate(inputTuple[1])}
# print (result)
# inputTuple_1 = (('a','c','b'),(1,3,2))
# result_1 = {inputTuple_1[0][i] : inputTuple_1[1][i] for i, _ in enumerate(inputTuple_1[1])}
# print (result_1)
# res = all((result_1.get(k) == v for k, v in result.items()))
# print(res)

    # for i in len