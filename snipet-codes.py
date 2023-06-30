import itertools
import random
from pyeda.inter import *
import networkx as nx
from networkx.algorithms import tournament

text = "0  or  not 0"
result = int(eval(text))
print (result)
test_list = [1,2,3,4,6,0,32,6,7]
print (random.choice(test_list))

# Convert an expression to a BDD
expression = expr2bdd(expr("A & B & C"))

# Calculate the value of the Boolean function
satisfying_assignment = expression.satisfy_one()
satisfying_assignments = expression.satisfy_all()

# Print the satisfying assignment and the function value
print("Satisfying assignment:", satisfying_assignment)

print("all satisfying assignment:" + str(list(expression.satisfy_all())))

print("Function value:", expression.restrict(satisfying_assignment))

# def generate_all_states(nodes):
#     all_states = list(itertools.product([0, 1], repeat=len(nodes)))
#     print ("all_states: " + str(all_states))
#     return [tuple(state) for state in all_states]

def generate_all_states(nodes):
	all_states = list(itertools.product([0, 1], repeat=len(nodes)))
	# print ("all_states: " + str(all_states))
	result = []
	for elm in all_states:
		a_dict = {}
		# print ("checking: " + str(list(nodes)) + "\t" + str(list(elm)))
		list_keys = list(nodes)
		list_values = list(elm)
		res = {list_keys[i]: list_values[i] for i in range(len(list_keys))}
		# for key in nodes:
		# 	for value in list(elm):
		# 		print ("checking: " + str(key) + "\tvalue: " + str(value))
		# 		a_dict[key] = value
		result.append(res)
	# print (result)
	return result

states = generate_all_states(expression.inputs)
print ("states: " + str(states))

def get_value_of_a_Boolean_function(expression, state):
    bdd_assignment = expression.restrict(state)
    result = int(bdd_assignment)
    print(f"Assignment: {state}, Result: {result}")

get_value_of_a_Boolean_function(expression, states[0])
# for assignment in states:
# 	print (str(type(assignment)) + "\t" + str(type(expression)))
# 	bdd_assignment = expression.restrict(assignment)
# 	result = int(bdd_assignment)
# 	print(f"Assignment: {assignment}, Result: {result}")
	
def get_full_states_of_chosen_one(expression, all_states):
	result = []
	for satisfied_one in list(expression.satisfy_all()):
		rs1 = []
		for state in all_states:
			res = all(state.get(k) == v for k,v in satisfied_one.items())
			# print ("checking: " + str(satisfied_one) + "\tvs.\t" + str(state) + "\tresult:\t" + str(res))
			if res == True:
				rs1.append(state)
		if rs1 != []:
			result.append(rs1)
	return result

chosen_states = get_full_states_of_chosen_one(expression, states)
print (chosen_states)
# generate_all_states_1(expression.inputs)
# elm = {"A": 0, "C": 1}
# elm = {"A": 0, "B":0, "C": 1}
# elm_2 = {"A": 0, "B":1, "C": 1}
# res = all(elm_2.get(k) == v for k,v in elm.items())
# print (res)
list_str = ['A', 'B', 'C']
list_bddvar = [bddvar(elm) for elm in list_str]
for elm in list_bddvar:
	print (type(elm))
	print (elm)

G = nx.DiGraph([(1, 0), (1, 3), (1, 2), (2, 3), (2, 0), (3, 0)])
print (tournament.is_reachable(G, 1, 3))

# from pyeda.inter import *

def count_satisfying_assignments(fi):
    fi_bdd = expr2bdd(fi)
    sols = fi_bdd.satisfy_all()
    count = 0
    for elm in sols:
    	count = count + 1
    
    return count

def find_assignment(B):
    assignment = []
    
    for bi in B:
        fi = bi  # Assume fi is the Boolean function associated with bi
        
        ctrue = count_satisfying_assignments(fi)
        cfalse = 2 ** len(fi.inputs) - ctrue
        
        if ctrue > cfalse:
            assignment.append(1)
        elif ctrue < cfalse:
            assignment.append(0)
        else:
            assignment.append(random.choice([0, 1]))
    
    return tuple(assignment)

# Example usage
B = exprvars('b', 5)  # Assuming B is a set of 5 Boolean variables

assignment = find_assignment(B)
print("Assignment:", assignment)