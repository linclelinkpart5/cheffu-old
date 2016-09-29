from pydot import (
    Dot,
    Node,
    Edge,
)

import cheffu.constants as c

def generate_graph(token_tree_root):
    graph = Dot(graph_type='digraph')

    def build_graph(token_tree):
        # Process inputs recursively
        input_nodes = []
        if 'inputs' in token_tree:
            input_nodes = [build_graph(i) for i in token_tree['inputs']]

        # Find out what kind of token this is
        sigil = token_tree['sigil']

        # Generate a label
        label = token_tree['name']

        # Determine the graph box shape
        if sigil == c.OPERAND_SIGIL:
            shape = 'ellipse'
        elif sigil == c.UNARY_OP_SIGIL:
            shape = 'box'
        elif sigil == c.BINARY_OP_SIGIL:
            shape = 'diamond'
        else:
            shape = 'ellipse'

        node = Node(str(id(token_tree)), label=label, shape=shape)

        # Build edges from each input to this graph node
        edges = [Edge(input_node, node) for input_node in input_nodes]

        # Add the graph node and edges to the graph
        graph.add_node(node)
        for edge in edges:
            graph.add_edge(edge)

        return node

    build_graph(token_tree_root)

    return graph