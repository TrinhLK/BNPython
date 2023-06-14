import networkx as nx
from networkx.algorithms.cycles import find_cycle

def compute_fvs(sdg):
    fvs = set()
    cycles = list(nx.simple_cycles(sdg))
    
    while cycles:
        cycle = cycles[0]
        fvs.update(cycle)
        sdg.remove_nodes_from(cycle)
        cycles = list(nx.simple_cycles(sdg))
    
    return fvs

# Example SDG
signed_directed_graph = nx.DiGraph()

# Add nodes to the SDG
signed_directed_graph.add_nodes_from(['x1', 'x2', 'x3'])

# Add edges with signs to the SDG
signed_directed_graph.add_edge('x1', 'x1', sign=1)
signed_directed_graph.add_edge('x1', 'x2', sign=1)
signed_directed_graph.add_edge('x1', 'x3', sign=1)
signed_directed_graph.add_edge('x2', 'x1', sign=1)
signed_directed_graph.add_edge('x2', 'x3', sign=1)
signed_directed_graph.add_edge('x3', 'x1', sign=1)
signed_directed_graph.add_edge('x3', 'x2', sign=-1)
signed_directed_graph.add_edge('x3', 'x3', sign=-1)
#-----------------
# signed_directed_graph.add_edge('x2', 'x1', sign=1)
# signed_directed_graph.add_edge('x3', 'x1', sign=1)
# signed_directed_graph.add_edge('x1', 'x2', sign=1)
# signed_directed_graph.add_edge('x2', 'x2', sign=-1)
# signed_directed_graph.add_edge('x1', 'x3', sign=1)

# Compute FVS
fvs = compute_fvs(signed_directed_graph)
print("Feedback Vertex Set:", fvs)
