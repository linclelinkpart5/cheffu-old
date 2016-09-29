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
from fractions import Fraction

import cheffu.constants as c

grammar_whitespace_mode = 'optional'

class NonNegInteger(Grammar):
    grammar =   (
                    WORD(c.DIGIT_CHARS),
                )

    def value(self):
        return int(self.string)

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
                    'modifiers': [s.value() for s in self[1]],
                    'annotations': [s.value() for s in self[2]],
                }

class Operand(Grammar):
    grammar =   (
                    c.OPERAND_SIGIL,
                    OPTIONAL(c.PSEUDO_OPERAND_FLAG),
                    Sentence,
                )

    def value(self):
        return  {
                    'sigil': self[0].string,
                    'pseudo': True if self[1] else False,
                    **self[2].value(),
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