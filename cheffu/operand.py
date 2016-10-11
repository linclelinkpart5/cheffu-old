import cheffu.constants as c

def operands_equal(operand_a, operand_b):
    sigil_a = operand_a['sigil']
    sigil_b = operand_b['sigil']

    assert(sigil_a == sigil_b == c.OPERAND_SIGIL)

    name_a = operand_a['name']
    name_b = operand_b['name']

    if name_a != name_b:
        return False

    modifiers_a = operand_a['modifiers']
    modifiers_b = operand_b['modifiers']

    if len(modifiers_a ^ modifiers_b) != 0:
        return False

    return True