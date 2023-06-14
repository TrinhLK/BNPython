import networkx as nx
import random

def find_all_fvs(sdg):
    fvs_list = []
    nodes = list(sdg.nodes())

    def backtrack(index, current_fvs):
        if index == len(nodes):
            fvs_list.append(current_fvs)
            return

        v = nodes[index]

        if is_fvs(current_fvs, v):
            # Skip v, as it is already covered by the current FVS
            backtrack(index + 1, current_fvs)
        else:
            # Include v in the current FVS
            backtrack(index + 1, current_fvs + [v])

            # Exclude v from the current FVS
            if is_fvs(current_fvs + [v], v):
                backtrack(index + 1, current_fvs)

    def is_fvs(fvs, v):
        sdg_copy = sdg.copy()
        u = set()
        v_self = {vertex for vertex in fvs if vertex in sdg_copy[vertex]}
        u.update(v_self)
        sdg_copy.remove_nodes_from(v_self)
        c = get_nontrivial_sccs(sdg_copy)
        while c:
            scc = random.choice(c)
            vertex = find_vertex_with_maximum_outdegree(sdg_copy, scc)
            u.add(vertex)
            c_c = get_nontrivial_sccs(sdg_copy.subgraph(scc - {vertex}))
            c.extend(c_c)
            c.remove(scc)
        return v in u

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

    backtrack(0, [])

    return fvs_list
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

# Compute the feedback vertex set
all_fvs = find_all_fvs(signed_directed_graph)

# Print the found FVSs
print("All Feedback Vertex Sets:")
for fvs in all_fvs:
    print(fvs)