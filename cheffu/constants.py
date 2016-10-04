OPERAND_SIGIL                   =   '*'
PSEUDO_OPERAND_FLAG             =   ':'
UNARY_OP_SIGIL                  =   '='
BINARY_OP_SIGIL                 =   '/'
SIMULTANEOUS_OP_FLAG            =   '+'
MODIFIER_SIGIL                  =   ','
ANNOTATION_SIGIL                =   ';'
ALPHA_CHARS                     =   "A-Za-z"
NZ_DIGIT_CHARS                  =   "1-9"
DIGIT_CHARS                     =   "0" + NZ_DIGIT_CHARS
PHRASE_CHARS                    =   "-' \"" + ALPHA_CHARS
STRING_CHARS                    =   PHRASE_CHARS + DIGIT_CHARS + "[]#\."

PARTITION_OP_SIGIL              =   '<'
PARTITION_A_PORTION_FLAG        =   '%'
PARTITION_B_PORTION_FLAG        =   '_'

STORED_OPERAND_SIGIL            =   '>'