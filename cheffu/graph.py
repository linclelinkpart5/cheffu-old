from pydot import (
    Dot,
    Node,
    Edge,
)

import cheffu.constants as c

NODE_BOX_SHAPES =   {
                        c.OPERAND_SIGIL:        'ellipse',
                        c.UNARY_OP_SIGIL:       'box',
                        c.BINARY_OP_SIGIL:      'diamond',
                        c.PARTITION_OP_SIGIL:   'plain',
                    }

def generate_graph(token_tree_root):
    graph = Dot(graph_type='digraph', strict=True)

    def build_graph(token_tree):
        # Process inputs recursively
        input_nodes = [build_graph(i) for i in token_tree.get('inputs', [])]

        # Find out what kind of token this is
        sigil = token_tree['sigil']

        # Generate a label
        label = token_tree.get('name', 'UNKNOWN')

        # Determine the graph box shape
        shape = NODE_BOX_SHAPES.get(sigil, 'plaintext')

        node = Node(str(token_tree['uuid']), label=label, shape=shape)

        # Build edges from each input to this graph node
        edges = [Edge(input_node, node, label=str(token_tree['inputs'][i].get('fraction', " "))) for i, input_node in enumerate(input_nodes)]

        # Add the graph node and edges to the graph
        graph.add_node(node)
        for edge in edges:
            graph.add_edge(edge)

        return node

    build_graph(token_tree_root)

    return graph