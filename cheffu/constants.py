OPERAND_SIGIL                   =   '*'
UNARY_OP_SIGIL                  =   '='
BINARY_OP_SIGIL                 =   '/'
VARIANT_LIST_START_SIGIL        =   '['
VARIANT_LIST_SEPARATOR          =   '|'
VARIANT_LIST_CLOSE_SIGIL        =   ']'
VARIANT_TAG_LIST_SEPARATOR      =   ','
PSEUDO_OPERAND_SIGIL            =   ':'
SIMULTANEOUS_OP_SIGIL           =   '+'
VARIANT_TAG_SIGIL               =   '#'
MODIFIER_SIGIL                  =   ','
ANNOTATION_SIGIL                =   ';'
ALPHA_CHARS                     =   "A-Za-z"
NZ_DIGIT_CHARS                  =   "1-9"
DIGIT_CHARS                     =   "0" + NZ_DIGIT_CHARS
PHRASE_CHARS                    =   "-' \"" + ALPHA_CHARS
STRING_CHARS                    =   PHRASE_CHARS + DIGIT_CHARS + "[]#\."