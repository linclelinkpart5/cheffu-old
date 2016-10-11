import cheffu.constants as c
from itertools import count

def format_standard(token_tree_root):
    ingredients = set()
    steps = []
    num = count()

    def process(token_tree):
        # Process inputs recursively
        for i in token_tree.get('inputs', []):
            process(i)

        sigil = token_tree['sigil']

        if sigil != c.OPERAND_SIGIL:
            return
        else:
            name = token_tree['name']
            modifiers = token_tree['modifiers']
            ingredients.add((next(num), name, modifiers))

    process(token_tree_root)

    return ingredients