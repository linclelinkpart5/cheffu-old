from fractions import Fraction
from collections_extended import bijection
import cheffu.constants as c

def number_to_str(n):
    if isinstance(n, int):
        return str(n)
    elif isinstance(n, Fraction):
        whl = n.numerator // n.denominator
        n = n - whl
        num = n.numerator
        den = n.denominator

        if whl > 0:
            return "{}{}{}{}{}".format(whl, " ", num, c.FRACTION_SEPARATOR, den)
        else:
            return "{}{}{}".format(num, c.FRACTION_SEPARATOR, den)
    else:
        return str(n)

def format_amount(operand_dict):
    if 'amount' in operand_dict:
        amount_dict = operand_dict['amount']
        if 'quantity' in amount_dict:
            quantity = amount_dict['quantity']
            range_ = amount_dict.get('range', 0)
            units = amount_dict.get('units', 'count')
            if range_ != 0:
                return "{}-{} {}".format(number_to_str(quantity), number_to_str(quantity + range_), units)
            else:
                return "{} {}".format(number_to_str(quantity), units)
        else:
            return ""
    else:
        return ""

def get_non_passthrough_input_uuids_old(recipe_dict, target_uuid):
    target_input_uuids = recipe_dict[target_uuid].get('inputs', [])
    non_passthrough_input_ids = []

    for target_input_uuid in target_input_uuids:
        # Get the input token
        input_token = recipe_dict[target_input_uuid]

        # CHECK IF THE INPUT TOKEN HAS A FIELD WE CARE ABOUT

        # Check if the token is passthrough
        # A token is "passthrough" if it has no name AND has a non-empty input UUID list
        if 'name' not in input_token and input_token.get('inputs', []):
            discovery = get_non_passthrough_input_uuids(recipe_dict, target_input_uuid)
            non_passthrough_input_ids.extend(discovery)

            # THIS IS A PASSTHROUGH, SO ALL ITEMS IN DISCOVERY WILL HAVE FIELDS PULLED AND PROCESSED WITH THIS TOKEN'S FIELD, ONE-BY-ONE IN ORDER
        else:
            non_passthrough_input_ids.append(target_input_uuid)
            # HERE, WE WOULD JUST APPEND A DEFAULT VALUE, SINCE IT'S NOT A PASSTHROUGH TOKEN

    return non_passthrough_input_ids

def get_non_passthrough_input_uuids(recipe_dict, target_uuid):
    target_input_uuids = recipe_dict[target_uuid].get('inputs', [])
    non_passthrough_input_ids = []
    reduced_vals = []
    DEFAULT_VALUE = 1

    for target_input_uuid in target_input_uuids:
        # Get the input token
        input_token = recipe_dict[target_input_uuid]

        # CHECK IF THE INPUT TOKEN HAS A FIELD WE CARE ABOUT

        # Check if the token is passthrough
        # A token is "passthrough" if it has no name AND has a non-empty input UUID list
        if 'name' not in input_token and input_token.get('inputs', []):
            discovery, discovered_vals = get_non_passthrough_input_uuids(recipe_dict, target_input_uuid)
            non_passthrough_input_ids.extend(discovery)

            # THIS IS A PASSTHROUGH, SO ALL ITEMS IN DISCOVERY VALS WILL HAVE FIELDS PULLED AND PROCESSED WITH THIS TOKEN'S FIELD, ONE-BY-ONE IN ORDER
            op = input_token.get('fraction', DEFAULT_VALUE)
            reduced_vals.extend([op * dv for dv in discovered_vals])
        else:
            non_passthrough_input_ids.append(target_input_uuid)
            # HERE, WE WOULD JUST APPEND A DEFAULT VALUE, SINCE IT'S NOT A PASSTHROUGH TOKEN
            reduced_vals.append(DEFAULT_VALUE)

    return non_passthrough_input_ids, reduced_vals

KNOWN_UNITS =   bijection({
                    # Mass
                    'kg'.casefold()             : 'kg'.casefold(),
                    'g'.casefold()              : 'g'.casefold(),
                    'mg'.casefold()             : 'mg'.casefold(),
                    'lb'.casefold()             : 'lbs'.casefold(),
                    'pound'.casefold()          : 'pounds'.casefold(),
                    'oz'.casefold()             : 'oz'.casefold(),
                    'ounce'.casefold()          : 'ounces'.casefold(),
                    # Volume
                    'l'.casefold()              : 'l'.casefold(),
                    'liter'.casefold()          : 'liters'.casefold(),
                    'litre'.casefold()          : 'litres'.casefold(),
                    'fl oz'.casefold()          : 'fl oz'.casefold(),
                    'fluid ounce'.casefold()    : 'fluid ounces'.casefold(),
                    # Count
                    'count'.casefold()          : 'count'.casefold(),
                    'whole'.casefold()          : 'whole'.casefold(),
                    'sprig'.casefold()          : 'sprigs'.casefold(),
                })

def make_plural_unit(unit_name):
    pass

def make_singular_unit(unit_name):
    pass