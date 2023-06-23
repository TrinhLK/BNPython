from pyeda.inter import *


# Read the input file
with open("input.txt", "r") as file:
    lines = file.readlines()

boolean_network = {}
for line in lines:
    if line.startswith("#") or line == "\n" or line.startswith("targets,"):
        continue
    lhs, rhs = map(str.strip, line.split(","))
    rhs = rhs.replace("!", "~")
    boolean_network[lhs] = rhs

for variable, boolean_function in boolean_network.items():
    fexpr = expr(boolean_function)
    print (fexpr)
