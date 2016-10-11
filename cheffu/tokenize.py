from modgrammar import (
    Grammar,
    WORD,
    ZERO_OR_MORE,
    OPTIONAL,
    ONE_OR_MORE,
    OR,
)
from fractions import Fraction
import uuid

import cheffu.constants as c

grammar_whitespace_mode = 'optional'

class NonNegInteger(Grammar):
    grammar =   (
                    WORD(c.DIGIT_CHARS),
                )

    def value(self):
        return int(self.string)

class PosInteger(Grammar):
    grammar =   (
                    WORD(c.NZ_DIGIT_CHARS, c.DIGIT_CHARS),
                )

    def value(self):
        return int(self.string)

class PosFraction(Grammar):
    grammar =   (
                    PosInteger,
                    c.FRACTION_SEPARATOR,
                    PosInteger,
                )

    def value(self):
        return Fraction(self[0].value(), self[2].value())

class PosDecimal(Grammar):
    grammar =   (
                    NonNegInteger,
                    c.DECIMAL_SEPARATOR,
                    PosInteger,
                )

    def value(self):
        return Fraction(self.string)

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

class Sentence(Grammar):
    grammar =   (
                    Phrase,
                    ZERO_OR_MORE(Modifier),
                    ZERO_OR_MORE(Annotation),
                )

    def value(self):
        return  {
                    'name': self[0].value(),
                    'modifiers': frozenset([s.value() for s in self[1]]),
                    'annotations': frozenset([s.value() for s in self[2]]),
                }

class Partition(Grammar):
    grammar =   (
                    ONE_OR_MORE(c.PARTITION_A_PORTION_FLAG),
                    ONE_OR_MORE(c.PARTITION_B_PORTION_FLAG),
                )

    def value(self):
        num = len(self[0].string)
        den = len(self.string)
        return Fraction(num, den)

class PosNumber(Grammar):
    grammar =   (
                    OR(
                        PosInteger,
                        PosFraction,
                        PosDecimal,
                    ),
                )

    def value(self):
        return self[0].value()

class Quantity(Grammar):
    grammar =   (
                    OPTIONAL(c.QUANTITY_RANGE_APPROX_FLAG),
                    PosNumber,
                    OPTIONAL(
                        c.QUANTITY_RANGE_SEPARATOR,
                        PosNumber,
                    ),
                    OPTIONAL(c.QUANTITY_RANGE_APPROX_FLAG),
                )

    def value(self):
        return  {
                    'a_approx': True if self[0] else False,
                    'quantity': self[1].value(),
                    'range': self[2][1].value() if self[2] else 0,
                    'b_approx': True if self[3] else False,
                }

class Units(Grammar):
    grammar =   (
                    Phrase,
                )

    def value(self):
        return self[0].value()

class Amount(Grammar):
    grammar =   (
                    c.AMOUNT_SIGIL,
                    Quantity,
                    Units,
                )

    def value(self):
        return  {
                    **self[1].value(),
                    'units': self[2].value(),
                }

class Operand(Grammar):
    grammar =   (
                    c.OPERAND_SIGIL,
                    OPTIONAL(c.PSEUDO_OPERAND_FLAG),
                    Sentence,
                    OPTIONAL(Amount),
                )

    def value(self):
        return  {
                    'sigil': self[0].string,
                    'pseudo': True if self[1] else False,
                    **self[2].value(),
                    **(self[3].value() if self[3] else {}),
                }

class UnaryOp(Grammar):
    grammar =   (
                    c.UNARY_OP_SIGIL,
                    OPTIONAL(c.SIMULTANEOUS_OP_FLAG),
                    Sentence,
                )

    def value(self):
        return  {
                    'sigil': self[0].string,
                    'simultaneous': True if self[1] else False,
                    **self[2].value(),
                }

class BinaryOp(Grammar):
    grammar =   (
                    c.BINARY_OP_SIGIL,
                    OPTIONAL(c.SIMULTANEOUS_OP_FLAG),
                    Sentence,
                )

    def value(self):
        return  {
                    'sigil': self[0].string,
                    'simultaneous': True if self[1] else False,
                    **self[2].value(),
                }

class PartitionOp(Grammar):
    grammar =   (
                    c.PARTITION_OP_SIGIL,
                    Partition,
                )

    def value(self):
        return  {
                    'sigil': self[0].string,
                    'fraction': self[1].value(),
                }

class StoredOperand(Grammar):
    grammar =   (
                    c.STORED_OPERAND_SIGIL,
                    NonNegInteger,
                )

    def value(self):
        return  {
                    'sigil': self[0].string,
                    'key': self[1].value(),
                }

class Token(Grammar):
    grammar =   (
                    OR(
                        Operand,
                        UnaryOp,
                        BinaryOp,
                        PartitionOp,
                        StoredOperand,
                    ),
                )

    def value(self):
        return  {
                    **self[0].value(),
                    'uuid': uuid.uuid4(),
                }

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