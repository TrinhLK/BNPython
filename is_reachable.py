from pyeda.inter import *

# # Boolean variables for current and next state
# curr_vars = [bddvar(f'x{i}') for i in range(N)]
# next_vars = [bddvar(f'x{i}_') for i in range(N)] 

# # BDDs for update functions
# update_fn = []
# for i in range(N):
#    fn_i = expr2truthtable(update_rules[i])
#    update_fn.append(fn_i(next_vars[i], *curr_vars))

# # BDD for s1  
# s1_bdd = And(*[var if s1[i]==1 else ~var for i, var in enumerate(curr_vars)])

# # BDD for s2
# s2_bdd = And(*[var if s2[i]==1 else ~var for i, var in enumerate(next_vars)])

# # BDD for reaching s2 from s1
# reach_bdd = And(s1_bdd, And(*update_fn), s2_bdd) 

# # Check if BDD is satisfiable
# print(is_satisfiable(reach_bdd))

boolean_functions = {
    "x1": "x1 & x2 & x3",
    "x2": "x1 | ~x3",
    "x3": "(x2 & ~x3) | (x1 & ~x2 & ~x3) | (x1 & x2 & x3)"
}
dict_bn = {}

for k, v in boolean_functions.items():
    stg_bdd_node = bddvar(k)
    stg_bdd_function = expr2bdd(expr(v))
    dict_bn[stg_bdd_node] = stg_bdd_function
    # total_func &= (stg_bdd_node & stg_bdd_function) | (~stg_bdd_node & ~stg_bdd_function)

def is_reachable_1(dict_bn, s1, s2):
    # Perform BFS starting from s1
    visited = [s1]
    queue = [s1]
    path = []
    test_func = 1
    while queue:
        curr = queue.pop(0)
        path.append(curr)

        for func in list(dict_bn.values()):
            test_func &= func
            print(test_func)
        # Check if s2 is visited
        if curr == s2:
            print ("path: " + str(path))
            return True
        # Add unvisited successor states to the queue

        # for succ in G.successors(curr):
        #     if succ not in visited:
        #         visited.add(succ)
        #         queue.append(succ)
    # If s2 is not visited, it is not reachable from s1
    return False

s1 = {bddvar('x1'): 0, bddvar('x3'): 1}
s2 = {bddvar('x1'): 1, bddvar('x2'): 1, bddvar('x3'): 1}

is_reachable_1(dict_bn, s1, s2)

def is_reachable(boolean_functions, s1, s2):
    #Initiate BDD with s1
    bddS1 = 1
    for v in s1:
        if s1[v] == 1:
            bddS1 &= v
        else:
            bddS1 &= ~v

    for i in range(10):
        bddS1_prev = bddS1
        for var, func in boolean_functions.items():
            tmpbdd_func = expr2bdd(expr(func))
            bddS1 |= tmpbdd_func.compose(bddS1)
        if bddS1.equivalent(bddS1_prev):
            break
# -----------------------------
is_reachable(boolean_functions, F[0], fixed_points[0])
