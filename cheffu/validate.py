import cheffu.constants as c
import uuid
from copy import (
    copy,
    deepcopy,
)
from itertools import count

class CheffuValidateError(Exception):
    pass

def validate(tokens):
    operand_stack = []
    stored_mem = []
    recipe_dict = {}
    index = count()

    def add_to_dict(token):
        id_ = uuid.uuid4()
        token['index'] = next(index)
        recipe_dict[id_] = token
        return id_

    def operand_process(token):
        return add_to_dict(token)

    def unary_op_process(token):
        if len(operand_stack) < 1:
            raise CheffuValidateError("Expected at least one operand on stack, found {}".format(len(operand_stack)))

        input_id = operand_stack.pop()
        token['inputs'] = [input_id]
        return add_to_dict(token)

    def binary_op_process(token):
        if len(operand_stack) < 2:
            raise CheffuValidateError("Expected at least two operands on stack, found {}".format(len(operand_stack)))

        input_id_r = operand_stack.pop()
        input_id_l = operand_stack.pop()
        token['inputs'] = [input_id_l, input_id_r]
        return add_to_dict(token)

    def partition_op_process(token):
        if len(operand_stack) < 1:
            raise CheffuValidateError("Expected at least one operand on stack, found {}".format(len(operand_stack)))

        input_id = operand_stack.pop()

        token['inputs'] = [input_id]
        # token['name'] = 'PARTITION_OP_PASSTHROUGH'
        stored_token = deepcopy(token)
        stored_token['fraction'] = 1 - stored_token['fraction']
        stored_id = add_to_dict(stored_token)

        stored_mem.append(stored_id)

        return add_to_dict(token)

    def stored_operand_process(token):
        key = token['key']

        if len(stored_mem) < key:
            raise CheffuValidateError("Expected an operand in stored memory at index {}, but stored memory only contains {} elements".format(key, len(stored_mem)))

        retrieved_id = stored_mem[key]
        stored_mem[key] = None

        if not retrieved_id:
            raise CheffuValidateError("Expected an operand in stored memory at index {}, but element did not exist".format(key))

        token['inputs'] = [retrieved_id]
        # token['name'] = 'STORED_OPERAND_PASSTHROUGH'

        return add_to_dict(token)

    FUNCS = {
                c.OPERAND_SIGIL: operand_process,
                c.UNARY_OP_SIGIL: unary_op_process,
                c.BINARY_OP_SIGIL: binary_op_process,
                c.PARTITION_OP_SIGIL: partition_op_process,
                c.STORED_OPERAND_SIGIL: stored_operand_process,
            }

    for token in tokens:
        sigil = token['sigil']
        func = FUNCS[sigil]
        id_ = func(token)
        operand_stack.append(id_)

    if len(operand_stack) != 1:
        raise CheffuValidateError("Expected one item left on stack, found {}:\n{}".format(len(operand_stack), pformat(operand_stack)))
    if any(stored_mem):
        raise CheffuValidateError("Expected no items left in stored mem, found {}".format(pformat(stored_mem)))

    return recipe_dict, operand_stack[0]