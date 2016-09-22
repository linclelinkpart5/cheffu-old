from modgrammar import (
    Grammar,
    WORD,
    ZERO_OR_MORE,
    OPTIONAL,
    REF,
    ONE_OR_MORE,
    OR,
    EMPTY,
)
from enum import Enum
from pydot import (
    Dot,
    Node,
    Edge,
)

import cheffu.constants as c

grammar_whitespace_mode = 'optional'

class String(Grammar):
    grammar =   (
                    WORD(c.STRING_CHARS),
                )

    def value(self):
        return self.string.strip()

class Phrase(Grammar):
    grammar =   (
                    WORD(c.PHRASE_CHARS),
                )

    def value(self):
        return self.string.strip()

class Modifier(Grammar):
    grammar =   (
                    c.MODIFIER_SIGIL,
                    String,
                )

    def value(self):
        return self[1].value()

class Annotation(Grammar):
    grammar =   (
                    c.ANNOTATION_SIGIL,
                    String,
                )

    def value(self):
        return self[1].value()

class Ingredient(Grammar):
    grammar =   (
                    Phrase,
                    ZERO_OR_MORE(Modifier),
                    ZERO_OR_MORE(Annotation),
                )

    def value(self):
        return self[0].value(), [m.value() for m in self[1]], [a.value() for a in self[2]]

class Directive(Grammar):
    grammar =   (
                    Phrase,
                    ZERO_OR_MORE(Modifier),
                    ZERO_OR_MORE(Annotation),
                )

    def value(self):
        return self[0].value(), [m.value() for m in self[1]], [a.value() for a in self[2]]

class Operand(Grammar):
    grammar =   (
                    c.OPERAND_SIGIL,
                    OPTIONAL(c.PSEUDO_OPERAND_SIGIL),
                    Ingredient,
                )

    def value(self):
        sigil = self[0].string
        sigil_flags = self[1].string if self[1] else ""
        name, modifiers, annotations = self[2].value()
        return sigil, sigil_flags, name, modifiers, annotations

class UnaryOp(Grammar):
    grammar =   (
                    c.UNARY_OP_SIGIL,
                    OPTIONAL(c.SIMULTANEOUS_OP_SIGIL),
                    Directive,
                )

    def value(self):
        sigil = self[0].string
        sigil_flags = self[1].string if self[1] else ""
        name, modifiers, annotations = self[2].value()
        return sigil, sigil_flags, name, modifiers, annotations

class BinaryOp(Grammar):
    grammar =   (
                    c.BINARY_OP_SIGIL,
                    OPTIONAL(c.SIMULTANEOUS_OP_SIGIL),
                    Directive,
                )

    def value(self):
        sigil = self[0].string
        sigil_flags = self[1].string if self[1] else ""
        name, modifiers, annotations = self[2].value()
        return sigil, sigil_flags, name, modifiers, annotations

class Token(Grammar):
    grammar =   (
                    OR(
                        Operand,
                        UnaryOp,
                        BinaryOp,
                    ),
                )

    def value(self):
        return self[0].value()

class Recipe(Grammar):
    grammar =   (
                    ONE_OR_MORE(Token),
                )

    def value(self):
        return [t.value() for t in self[0]]

def tokenize(text):
    recipe_parser = Recipe.parser()
    result = recipe_parser.parse_string(text)
    tokens = result.value()
    return tokens

# def generate_graph(tokens):
#     graph = Dot(graph_type='digraph')
#     node_stack = [] # Last element is top of stack

#     for i, token in enumerate(tokens):
#         sigil, sigil_flags, name, modifiers, annotations = token

#         node_id = "node_{}".format(i)

#         if kind == TokenType.value:
#             # Push onto stack
#             node_stack.append(Node(node_id, label=str(name)))
#         elif kind == TokenType.unaryop:
#             # Check if there is at least one value in stack
#             if len(node_stack) < 1:
#                 raise Exception("Expected at least 1 value in stack, found {}".format(len(node_stack)))

#             # Pop one value off the stack
#             node = node_stack.pop()

#             # Add the popped node to the graph
#             graph.add_node(node)

#             # "Calculate" and push back on stack
#             new_node = Node(node_id, label=name, shape='box')
#             graph.add_edge(Edge(node, new_node))
#             node_stack.append(new_node)

#         elif kind == TokenType.binaryop:
#             # Check if there is at least two values in stack
#             if len(node_stack) < 2:
#                 raise Exception("Expected at least 2 values in stack, found {}".format(len(node_stack)))

#             # Pop two values off the stack
#             node_a = node_stack.pop()
#             node_b = node_stack.pop()

#             # Add the popped nodes to the graph
#             graph.add_node(node_a)
#             graph.add_node(node_b)

#             # "Calculate" and push back on stack
#             new_node = Node(node_id, label=name, shape='box')
#             graph.add_edge(Edge(node_a, new_node))
#             graph.add_edge(Edge(node_b, new_node))
#             node_stack.append(new_node)

#     if len(node_stack) != 1:
#         raise Exception("Expected exactly 1 value in stack, found {}".format(len(node_stack)))
#     else:
#         graph.add_node(node_stack.pop())

#     graph.write_png('recipe.png')