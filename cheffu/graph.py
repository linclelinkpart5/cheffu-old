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

def get_non_passthrough_input_uuids(recipe_dict, target_uuid):
    target_token = recipe_dict[target_uuid]

    target_input_uuids = target_token.get('inputs', [])

    non_passthrough_input_ids = []

    for target_input_uuid in target_input_uuids:
        # Get the input token
        input_token = recipe_dict[target_input_uuid]

        # Check if the token is passthrough
        # A token is "passthrough" if it has no name AND has a non-empty input UUID list
        if 'name' not in input_token and input_token.get('inputs', []):
            discovery = get_non_passthrough_input_uuids(recipe_dict, target_input_uuid)
            non_passthrough_input_ids.extend(discovery)
        else:
            non_passthrough_input_ids.append(target_input_uuid)

    return non_passthrough_input_ids

def generate_graph(recipe_dict, start_key):
    graph = Dot(graph_type='digraph', strict=True)

    def build_graph(recipe_dict, key):
        # Use the key and dict to get the target token
        token = recipe_dict[key]

        # Process inputs recursively
        input_uuids = get_non_passthrough_input_uuids(recipe_dict, key)
        input_nodes = [build_graph(recipe_dict, k) for k in input_uuids]

        # Find out what kind of token this is
        sigil = token['sigil']

        # Generate a label
        label = token['name']

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