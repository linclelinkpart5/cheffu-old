from pydot import (
    Dot,
    Node,
    Edge,
)

import cheffu.constants as c

def generate_graph(node_root):
    graph = Dot(graph_type='digraph')
    count = 0

    def build_graph(node, count):
        sub_graph_nodes = []

        for child in node.child_nodes:
            sub_graph_node, count = build_graph(child, count)
            sub_graph_nodes.append(sub_graph_node)

        sigil, flags, name, modifiers, annotations = node.value()

        # Each subgraph will connect to this node
        # Build a graph node for this tree node
        label = name
        if modifiers:
            label = (c.MODIFIER_SIGIL + " ").join([label, (c.MODIFIER_SIGIL + " ").join(modifiers)])
        if annotations:
            label = (c.ANNOTATION_SIGIL + " ").join([label, (c.ANNOTATION_SIGIL + " ").join(annotations)])

        if sigil == c.OPERAND_SIGIL:
            shape = 'ellipse'
        elif sigil == c.UNARY_OP_SIGIL:
            shape = 'box'
        elif sigil == c.BINARY_OP_SIGIL:
            shape = 'diamond'
        else:
            shape = 'ellipse'

        graph_node = Node(str(count), label=label, shape=shape)
        count = count + 1

        # Build edges from each child to this graph node
        edges = [Edge(sub_graph_node, graph_node) for sub_graph_node in sub_graph_nodes]

        # Add the graph node and edges to the graph
        graph.add_node(graph_node)
        for edge in edges:
            graph.add_edge(edge)

        return graph_node, count

    build_graph(node_root, 0)

    return graph