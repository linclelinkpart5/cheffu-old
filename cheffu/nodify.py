import cheffu.constants as c

class CheffuNodifyError(Exception):
    pass

class Node:
    def __init__(self, sigil, flags, data, modifiers, annotations, *child_nodes):
        self.sigil = sigil
        self.flags = flags
        self.data = data
        self.modifiers = tuple(modifiers)
        self.annotations = tuple(annotations)
        self.child_nodes = tuple(child_nodes)

    def __str__(self):
        s = "{} {} {} {} {}\n".format(self.sigil, self.flags, self.data, self.modifiers, self.annotations)
        for c in self.child_nodes:
            s = s + "\t{}".format(c)

        return s

    def value(self):
        return self.sigil, self.flags, self.data, self.modifiers, self.annotations

def nodify(tokens):
    stack = []

    for sigil, flags, data, modifiers, annotations in tokens:
        if sigil == c.OPERAND_SIGIL:
            children = ()
        elif sigil == c.UNARY_OP_SIGIL:
            if len(stack) < 1:
                raise CheffuNodifyError("Expected at least one operand on stack, found {}".format(len(stack)))

            children = (stack.pop(),)
        elif sigil == c.BINARY_OP_SIGIL:
            if len(stack) < 2:
                raise CheffuNodifyError("Expected at least two operands on stack, found {}".format(len(stack)))

            child_a = stack.pop()
            child_b = stack.pop()
            children = (child_b, child_a)
        else:
            raise CheffuNodifyError("Unknown sigil")

        new_item = Node(sigil, flags, data, modifiers, annotations, *children)
        stack.append(new_item)

    if len(stack) != 1:
        raise CheffuNodifyError("Expected one item left on stack, found {}:\n{}".format(len(stack), "\n".join([str(n) for n in stack])))
    else:
        return stack[0]