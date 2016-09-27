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

import cheffu.constants as c

grammar_whitespace_mode = 'optional'

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

class Ingredient(Grammar):
    grammar =   (
                    Phrase,
                    ZERO_OR_MORE(Modifier),
                    ZERO_OR_MORE(Annotation),
                )

    def value(self):
        return self[0].value(), [m.value() for m in self[1]], [a.value() for a in self[2]]

class Directive(Grammar):
    grammar =   (
                    Phrase,
                    ZERO_OR_MORE(Modifier),
                    ZERO_OR_MORE(Annotation),
                )

    def value(self):
        return self[0].value(), [m.value() for m in self[1]], [a.value() for a in self[2]]

class Operand(Grammar):
    grammar =   (
                    c.OPERAND_SIGIL,
                    OPTIONAL(c.PSEUDO_OPERAND_FLAG),
                    Ingredient,
                )

    def value(self):
        sigil = self[0].string
        sigil_flags = { 'pseudo': True if self[1] else False }
        data, modifiers, annotations = self[2].value()
        return sigil, sigil_flags, data, modifiers, annotations

class UnaryOp(Grammar):
    grammar =   (
                    c.UNARY_OP_SIGIL,
                    OPTIONAL(c.SIMULTANEOUS_OP_FLAG),
                    Directive,
                )

    def value(self):
        sigil = self[0].string
        sigil_flags = { 'simultaneous': True if self[1] else False }
        data, modifiers, annotations = self[2].value()
        return sigil, sigil_flags, data, modifiers, annotations

class BinaryOp(Grammar):
    grammar =   (
                    c.BINARY_OP_SIGIL,
                    OPTIONAL(c.SIMULTANEOUS_OP_FLAG),
                    Directive,
                )

    def value(self):
        sigil = self[0].string
        sigil_flags = { 'simultaneous': True if self[1] else False }
        data, modifiers, annotations = self[2].value()
        return sigil, sigil_flags, data, modifiers, annotations

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