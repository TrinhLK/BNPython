from pyeda.inter import *
from pyeda.boolalg.bdd import *

# Example usage
# Assuming 'x' is the variable we're interested in
x = exprvar('x')
f = ~x
bdd = expr2bdd(f)
bdd.root
