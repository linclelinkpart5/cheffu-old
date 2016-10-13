import cheffu.constants as c

from collections import defaultdict

def shopping_list(recipe_dict):
    operand_tokens = list(filter(lambda x: x['sigil'] == c.OPERAND_SIGIL and not x['pseudo'], recipe_dict.values()))

    amount_dict = defaultdict(lambda: { 'quantity': 0, 'range': 0, 'a_approx': False, 'b_approx': False })
    unspecified_set = set()

    for operand_token in operand_tokens:
        name = operand_token['name']
        modifiers = operand_token['modifiers']
        key = (name, modifiers)

        amount = operand_token['amount']

        if amount:
            units = amount['units']
            unit_key = (*key, units)

            quantity    = amount['quantity']
            range_      = amount['range']
            a_approx    = amount['a_approx']
            b_approx    = amount['b_approx']

            amount_dict[unit_key]['quantity'] += quantity
            amount_dict[unit_key]['range'] += range_
            amount_dict[unit_key]['a_approx'] = amount_dict[unit_key]['a_approx'] or a_approx
            amount_dict[unit_key]['b_approx'] = amount_dict[unit_key]['b_approx'] or b_approx
        else:
            unspecified_set.add(key)

    return amount_dict