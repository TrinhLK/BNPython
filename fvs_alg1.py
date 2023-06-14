import networkx as nx
import random

def compute_feedback_vertex_set(sdg):
    u = set()
    v_self = {v for v in sdg if v in sdg[v]}
    u.update(v_self)
    sdg.remove_nodes_from(v_self)
    c = get_nontrivial_sccs(sdg)
    while c:
        scc = random.choice(c)
        v = find_vertex_with_maximum_outdegree(sdg, scc)
        u.add(v)
        c_c = get_nontrivial_sccs(sdg.subgraph(scc - {v}))
        c.extend(c_c)
        c.remove(scc)
    return u

def get_nontrivial_sccs(sdg):
    return [scc for scc in nx.strongly_connected_components(sdg) if len(scc) > 1]

def find_vertex_with_maximum_outdegree(sdg, scc):
    max_outdegree = -1
    vertex = None
    for v in scc:
        outdegree = sdg.out_degree(v)
        if outdegree > max_outdegree:
            max_outdegree = outdegree
            vertex = v
    return vertex

signed_directed_graph = nx.DiGraph()
signed_directed_graph.add_nodes_from(['x1', 'x2', 'x3'])
#-----------------
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

# Compute the feedback vertex set
feedback_vertex_set = compute_feedback_vertex_set(signed_directed_graph)

# Print the feedback vertex set
print("Feedback Vertex Set:")
print(feedback_vertex_set)
