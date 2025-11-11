import ply.lex as lex

reserved = {
            "print":"PRINT",
            "if": "IF",
            "else": "ELSE",
            "while": "WHILE",
            "for": "FOR",
            "return": "RETURN",
            "var": "VAR"
}
# List of token names.   This is always required
tokens = (
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'VARIABLE',
    'FLOAT',
    'MAYORQUE',
    'MENORQUE',
    'IGUAL',
) + tuple(reserved.values())

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_MAYORQUE = r'\>'
t_MENORQUE = r'\<'
t_IGUAL = r'\='

def t_FLOAT(t):
    r'\d\.\d'
    t.value = float(t.value)
    return t
# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test it out
data = '''
3 + 4 * 10
  + -20 *2 9.5 ><=
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)
