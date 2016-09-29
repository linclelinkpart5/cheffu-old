import cheffu.constants as c
from copy import (
    copy,
    deepcopy,
)
from pprint import pformat

class CheffuValidateError(Exception):
    pass

def operand_process(token, operand_stack):
    return token, operand_stack

def unary_op_process(token, operand_stack):
    if len(operand_stack) < 1:
        raise CheffuValidateError("Expected at least one operand on stack, found {}".format(len(operand_stack)))

    input_operand = operand_stack.pop()
    token['inputs'] = [input_operand]
    return token, operand_stack

def binary_op_process(token, operand_stack):
    if len(operand_stack) < 2:
        raise CheffuValidateError("Expected at least two operands on stack, found {}".format(len(operand_stack)))

    input_operand_r = operand_stack.pop()
    input_operand_l = operand_stack.pop()
    token['inputs'] = [input_operand_l, input_operand_r]
    return token, operand_stack

FUNCS = {
            c.OPERAND_SIGIL: operand_process,
            c.UNARY_OP_SIGIL: unary_op_process,
            c.BINARY_OP_SIGIL: binary_op_process,
        }

def validate(tokens):
    operand_stack = []

    for token in tokens:
        sigil = token['sigil']
        func = FUNCS[sigil]
        token, operand_stack = func(token, operand_stack)
        operand_stack.append(token)

    if len(operand_stack) != 1:
        raise CheffuValidateError("Expected one item left on stack, found {}:\n{}".format(len(operand_stack), pformat(operand_stack)))
    return operand_stack[0]