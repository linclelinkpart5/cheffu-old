import cheffu.constants as c
from copy import (
    copy,
    deepcopy,
)
from pprint import pformat

class CheffuValidateError(Exception):
    pass

def operand_process(token, operand_stack, stored_mem):
    return token, operand_stack, stored_mem

def unary_op_process(token, operand_stack, stored_mem):
    if len(operand_stack) < 1:
        raise CheffuValidateError("Expected at least one operand on stack, found {}".format(len(operand_stack)))

    input_operand = operand_stack.pop()
    token['inputs'] = [input_operand]
    return token, operand_stack, stored_mem

def binary_op_process(token, operand_stack, stored_mem):
    if len(operand_stack) < 2:
        raise CheffuValidateError("Expected at least two operands on stack, found {}".format(len(operand_stack)))

    input_operand_r = operand_stack.pop()
    input_operand_l = operand_stack.pop()
    token['inputs'] = [input_operand_l, input_operand_r]
    return token, operand_stack, stored_mem

def partition_op_process(token, operand_stack, stored_mem):
    if len(operand_stack) < 1:
        raise CheffuValidateError("Expected at least one operand on stack, found {}".format(len(operand_stack)))

    input_operand = operand_stack.pop()

    stored_operand = deepcopy(input_operand)
    input_operand['fraction'] = input_operand.get('fraction', 1) * token['fraction']
    stored_operand['fraction'] = stored_operand.get('fraction', 1) * (1 - token['fraction'])
    stored_mem.append(stored_operand)

    token['inputs'] = [input_operand]

    return input_operand, operand_stack, stored_mem

def stored_operand_process(token, operand_stack, stored_mem):
    key = token['key']

    if len(stored_mem) < key:
        raise CheffuValidateError("Expected an operand in stored memory at index {}, but stored memory only contains {} elements".format(key, len(stored_mem)))

    retrieved_operand = stored_mem[key]
    stored_mem[key] = None

    if not retrieved_operand:
        raise CheffuValidateError("Expected an operand in stored memory at index {}, but element did not exist".format(key))

    # token['inputs'] = [retrieved_operand]
    token = retrieved_operand

    return token, operand_stack, stored_mem

FUNCS = {
            c.OPERAND_SIGIL: operand_process,
            c.UNARY_OP_SIGIL: unary_op_process,
            c.BINARY_OP_SIGIL: binary_op_process,
            c.PARTITION_OP_SIGIL: partition_op_process,
            c.STORED_OPERAND_SIGIL: stored_operand_process,
        }

def validate(tokens):
    operand_stack = []
    stored_mem = []

    for token in tokens:
        sigil = token['sigil']
        func = FUNCS[sigil]
        token, operand_stack, stored_mem = func(token, operand_stack, stored_mem)
        operand_stack.append(token)

    if len(operand_stack) != 1:
        raise CheffuValidateError("Expected one item left on stack, found {}:\n{}".format(len(operand_stack), pformat(operand_stack)))
    if any(stored_mem):
        raise CheffuValidateError("Expected no items left in stored mem, found {}".format(pformat(stored_mem)))

    return operand_stack[0]