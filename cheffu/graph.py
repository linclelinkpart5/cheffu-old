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
                        c.STORED_OPERAND_SIGIL: 'plain',
                    }

def format_amount(operand_dict):
    if 'amount' in operand_dict:
        if 'quantity' in operand_dict:
            quantity = operand_dict['quantity']
            range_ = operand_dict.get('range', 0)
            units = operand_dict.get('units', 'count')
            if range_ != 0:
                return "{}-{} {}".format(quantity, quantity + range_, units)
            else:
                return "{} {}".format(quantity, units)
        else:
            return ""
    else:
        return ""

def generate_graph_old(token_tree_root):
    graph = Dot(graph_type='digraph', strict=True)

    def build_graph(token_tree):
        # Process inputs recursively
        input_nodes = [build_graph(i) for i in token_tree.get('inputs', [])]

        # Find out what kind of token this is
        sigil = token_tree['sigil']

        # Generate a label
        label = token_tree.get('name', 'UNKNOWN')

        # Generate a string for amounts
        amount = format_amount(token_tree)

        # Determine the graph box shape
        shape = NODE_BOX_SHAPES.get(sigil, 'plaintext')

        node = Node(str(token_tree['uuid']), label="\n".join([label, amount]), shape=shape)

        # Build edges from each input to this graph node
        edges = [Edge(input_node, node, label=str(token_tree['inputs'][i].get('fraction', " "))) for i, input_node in enumerate(input_nodes)]

        # Add the graph node and edges to the graph
        graph.add_node(node)
        for edge in edges:
            graph.add_edge(edge)

        return node

    build_graph(token_tree_root)

    return graph

def generate_graph(recipe_dict, start_key):
    graph = Dot(graph_type='digraph', strict=True)

    def build_graph(recipe_dict, key):
        # Use the key and dict to get the target token
        token = recipe_dict[key]

        # Process inputs recursively
        input_nodes = [build_graph(recipe_dict, k) for k in token.get('inputs', [])]

        # Find out what kind of token this is
        sigil = token['sigil']

        # Generate a label
        label = token.get('name', 'UNKNOWN')

        # Generate a string for amounts
        amount = format_amount(token)

        # Determine the graph box shape
        shape = NODE_BOX_SHAPES.get(sigil, 'plaintext')

        node = Node(str(key), label="\n".join([label, amount]), shape=shape)

        # Build edges from each input to this graph node
        edges = [Edge(input_node, node) for i, input_node in enumerate(input_nodes)]

        # Add the graph node and edges to the graph
        graph.add_node(node)
        for edge in edges:
            graph.add_edge(edge)

        return node

    build_graph(recipe_dict, start_key)

    return graph