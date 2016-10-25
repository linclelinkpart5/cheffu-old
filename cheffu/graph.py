from pydot import (
    Dot,
    Node,
    Edge,
)

import cheffu.constants as c
import cheffu.helpers as h

NODE_BOX_SHAPES =   {
                        c.OPERAND_SIGIL:        'ellipse',
                        c.UNARY_OP_SIGIL:       'box',
                        c.BINARY_OP_SIGIL:      'diamond',
                        c.PARTITION_OP_SIGIL:   'plain',
                        c.STORED_OPERAND_SIGIL: 'plain',
                    }

def generate_graph(recipe_dict, start_uuid):
    graph = Dot(graph_type='digraph', strict=True)

    def build_graph(recipe_dict, uuid):
        # Use the uuid and dict to get the target token
        token = recipe_dict[uuid]

        # Process inputs recursively
        input_uuids, frac_vals = h.get_non_passthrough_input_uuids(recipe_dict, uuid)
        input_nodes = [build_graph(recipe_dict, k) for k in input_uuids]

        # Find out what kind of token this is
        sigil = token['sigil']

        # Generate a label
        label = token['name']

        # Generate a string for amounts
        amount = h.format_amount(token)

        # Determine the graph box shape
        shape = NODE_BOX_SHAPES.get(sigil, 'plaintext')

        node = Node(str(uuid), label="\n".join([label, amount]), shape=shape)

        # Build edges from each input to this graph node
        edges = [Edge(input_node, node, label=h.number_to_str(frac_val) if frac_val != 1 else " ") for input_node, frac_val in zip(input_nodes, frac_vals)]

        # Add the graph node and edges to the graph
        graph.add_node(node)
        for edge in edges:
            graph.add_edge(edge)

        return node

    build_graph(recipe_dict, start_uuid)

    return graph