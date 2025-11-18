import ply.lex as lex

reserved = {
        "abstract": "ABSTRACT",  # gilmaramg66
    "as": "AS",  # gilmaramg66
    "assert": "ASSERT",  # gilmaramg66
    "async": "ASYNC",
    "await": "AWAIT",
    "bool": "BOOL",  # lisbllam
    "break": "BREAK",  # gilmaramg66
    "catch": "CATCH",  # gilmaramg66
    "class": "CLASS",
    "const": "CONST",  # lisbllam
    "do": "DO",  # gilmaramg66
    "else": "ELSE",
    "extends": "EXTENDS",  # gilmaramg66
    "false": "FALSE",  # gilmaramg66
    "final": "FINAL",  # lisbllam
    "float": "FLOAT",  # lisbllam
    "for": "FOR",
    "Future": "FUTURE",
    "if": "IF",
    "implements": "IMPLEMENTS",  # gilmaramg66
    "import": "IMPORT",  # gilmaramg66
    "in": "IN",
    "interface": "INTERFACE",  # gilmaramg66
    "int": "INT",  # lisbllam
    "is": "IS",
    "library": "LIBRARY",  # gilmaramg66
    "ListQueue": "LIST_QUEUE",
    "null": "NULL",  # gilmaramg66
    "print": "PRINT",
    "Queue" : "QUEUE",
    "return": "RETURN",
    "set": "SET",  # gilmaramg66
    "static": "STATIC",  # gilmaramg66
    "String": "STRING",  # lisbllam
    "super": "SUPER",  # gilmaramg66
    "switch": "SWITCH",
    "throw": "THROW",  # gilmaramg66
    "true": "TRUE",  # gilmaramg66
    "try": "TRY",  # gilmaramg66
    "var": "VAR",
    "void": "VOID",  # gilmaramg66
    "while": "WHILE"
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
             'LCORCH',
             'RCORCH',
             'LBRACKET',  # anzagood1
             'RBRACKET',  # anzagood1
             'AND',
             'OR',
             'FLOAT_NUMBER',
             'MAYORQUE',
             'MENORQUE',
             'IGUAL',
             'ID',  # anzagood1
             'CADENA',  # lisbllam
             'SEMICOLON',  # lisbllam
             'COMENTARIO',  # anzagood1
             'NULLABLE',
             #'METODO',  # anzagood1
             'LAMBDA',  # gilmaramg66
             'HASH',  # gilmaramg66
             'COLON',  # gilmaramg66
             'NOT',  # gilmaramg66
             'COMMENTBLOCK',  # gilmaramg66
             'DOLLAR',  # gilmaramg66
             'BIT_AND',  # gilmaramg66
             'BIT_OR',  # gilmaramg66
             'BIT_XOR',  # gilmaramg66
             'BIT_NOT',  # gilmaramg66
             'LSHIFT',  # gilmaramg66
             'RSHIFT',  # gilmaramg66
             'COMA',
            'PUNTO'
         ) + tuple(reserved.values())

# Regular expression rules for simple tokens
t_COMENTARIO = r'//.*'  # anzagood1
#t_METODO = r'\..*()'  # anzagood1
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_MAYORQUE = r'>'
t_MENORQUE = r'<'
t_IGUAL = r'='
t_LCORCH = r'\['  # anzagood
t_RCORCH = r'\]'  # anzagood
t_LBRACKET = r'\{'  # lisbllam
t_RBRACKET = r'\}'  # lisbllam
t_AND = r'&&'
t_OR = r'\|\|'
t_SEMICOLON = r';'  # anzagood
t_NULLABLE = r'\?'  # lisbllam
t_LAMBDA = r'=>'  # gilmaramg66
t_HASH = r'\#'  # gilmaramg66
t_COLON = r':'  # gilmaramg66
t_NOT = r'!'  # gilmaramg66
t_DOLLAR = r'\$'  # gilmaramg66
t_BIT_AND = r'&'  # gilmaramg66
t_BIT_OR = r'\|'  # gilmaramg66
t_BIT_NOT = r'~'  # gilmaramg66
t_BIT_XOR = r'\^'  # gilmaramg66
t_LSHIFT = r'<<'  # gilmaramg66
t_RSHIFT = r'>>'  # gilmaramg66
t_COMA = r'\,'
t_PUNTO = r'\.'


def t_CADENA(t):  # lisbllam
    r'\'[^\']*\'|\"[^\"]*\"'
    return t


def t_FLOAT_NUMBER(t):  # anzagood1
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


# A regular expression rule with some action code
def t_NUMBER(t):  # anzagood1
    r'\d+'
    t.value = int(t.value)
    return t


def t_ID(t):  # anzagood1
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_COMMENTBLOCK(t):  # gilmaramg66
    r'/\*(.|\n)*?\*/'
    pass


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

# Test it out
data = '''
=>
a
+
b
;
int aver(int a, int b) => a + b;
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)
