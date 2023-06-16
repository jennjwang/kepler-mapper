""" Adapt Mapper format into other common formats.

    - networkx

"""


def to_networkx(graph):
    """Convert a Mapper 1-complex to a networkx graph.

    Parameters
    -----------

    graph: dictionary, graph object returned from `kmapper.map`

    Returns
    --------

    g: graph as networkx.Graph() object

    """

    # import here so networkx is not always required.
    import networkx as nx

    nodes = graph["nodes"].keys()
    edges = [[start, end] for start, ends in graph["links"].items() for end in ends]

    g = nx.Graph()
    g.add_nodes_from(nodes)
    nx.set_node_attributes(g, dict(graph["nodes"]), "membership")

    g.add_edges_from(edges)

    return g

def to_json(graph, X_projected, X_data, X_names, data_path, json_file, extra_vars=None):
        from gerrychain.graph import Graph as GCGraph
        from networkx.readwrite import json_graph
        import json
        import pandas as pd

        gcgraph = GCGraph(to_networkx(graph))
        metadata = graph["meta_data"]
        metadata["columns"] = X_names
        metadata["data_path"] = data_path
        metadata["extra_vars"] = extra_vars

        cluster_ids = graph["nodes"].keys()
        filter_vals = map(lambda kv: [X_projected[n][0] for n in kv[1]], graph["nodes"].items())
        add_df = pd.DataFrame({'cluster_ids': cluster_ids, 'filter_vals': list(filter_vals)})
        add_df = add_df.set_index('cluster_ids')
        gcgraph.add_data(add_df)

        graph_data = json_graph.adjacency_data(gcgraph)

        with open(json_file, "w+") as f:
            json.dump({"metadata": metadata, "graph": graph_data}, f)


to_nx = to_networkx
