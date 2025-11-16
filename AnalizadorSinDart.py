import ply.yacc as yacc
from AnalizadorLexDart import tokens

start = 'sentencias'

def p_sentencias(p):
    '''sentencias : sentencias sentencia
                  | sentencia'''

def p_sentencia(p):
    '''sentencia : declaracion_variables
                | asignacion_variables
                | declara_func_void
                | sentenciaif
                | valorbool
                | valor
                | tipodato
                | parametro
                | expresionesbool
                | exprbool
                | declaracion_list
                | sentenciawhile
                | parametros
                | comparador
                | sentenciafor
                | forcomparador
                | forunarios
    '''


def p_asignacion_variables(p):
    '''asignacion_variables : ID IGUAL valor SEMICOLON
                            | ID IGUAL ID SEMICOLON
    '''

def p_declaracion_variables(p):
    '''declaracion_variables : tipodato ID IGUAL valor SEMICOLON
                            | VAR ID IGUAL valor SEMICOLON'''

def p_declaracion_func_void(p):
    '''declara_func_void : VOID ID LPAREN RPAREN LBRACKET sentencias RBRACKET
                        | VOID ID LPAREN parametros RPAREN LBRACKET sentencias RBRACKET
    '''

def p_declaracion_list(p):
    'declaracion_list : tipodato ID IGUAL LCORCH RCORCH SEMICOLON'

def p_sentenciawhile(p):
    '''sentenciawhile : WHILE LPAREN expresionesbool RPAREN RBRACKET sentencias RBRACKET
                        | WHILE LPAREN expresionesbool RPAREN RBRACKET sentencias RETURN valorreturn RBRACKET
    '''

def p_imprimircadena(p):
    'imprimircadena : PRINT LPAREN CADENA RPAREN SEMICOLON'

def p_imprimirvariable(p):
    'imprimirvariable : PRINT LPAREN ID RPAREN SEMICOLON'

def p_imprimirexpresion(p):
    'imprimirexpresion : PRINT LPAREN SEMICOLON'

def p_expresionaritmetica(p):
    '''exprearitmetica : valoresnumericos PLUS valoresnumericos
                        | valoresnumericos MINUS valoresnumericos
                        | valoresnumericos TIMES valoresnumericos
                        | valoresnumericos DIVIDE valoresnumericos
    '''

def d_expresion(p):
    '''expresion : ID PLUS CADENA
                | expresionaritmeticq
    '''

def p_parametro(p):
    'parametro : tipodato ID'

def p_parametros(p):
    '''parametros : parametro
                    | parametro COMA parametros
    '''

def p_valorreturn(p):
    '''valorreturn : ID SEMICOLON
                    | valor
    '''

def p_valoresnumericos(p):
    '''valoresnumericos : NUMBER
                        | FLOAT_NUMBER
    '''

def p_sentenciafor(p):
    '''sentenciafor : FOR LPAREN VAR ID IGUAL NUMBER SEMICOLON ID forcomparador NUMBER SEMICOLON ID forunarios RPAREN LBRACKET sentencias RBRACKET
                        | FOR LPAREN INT ID IGUAL NUMBER SEMICOLON ID forcomparador NUMBER SEMICOLON ID forunarios RPAREN LBRACKET sentencias RBRACKET
                        | FOR LPAREN VAR ID IN ID RPAREN LBRACKET sentencias RBRACKET
                        | FOR LPAREN tipodato ID IN ID RPAREN LBRACKET sentencias RBRACKET'''

def p_tipodato(p):
    '''tipodato : STRING
                    | INT
                    | FLOAT
                    | BOOL
    '''

def p_forcomparador(p):
    '''forcomparador : MENORQUE
                       | MAYORQUE
                       | NOT IGUAL
    '''

def p_forunarios(p):
    '''forunarios : PLUS PLUS
                        | MINUS MINUS
                         '''


def p_sentenciaif(p):
    '''sentenciaif : IF LPAREN expresionesbool RPAREN LBRACKET sentencias RETURN valorreturn RBRACKET
                    | IF LPAREN expresionesbool RPAREN LBRACKET sentencias RBRACKET
    '''

def p_valorbool(p):
    '''valorbool : TRUE
                   | FALSE
    '''

def p_comparador(p):
    '''comparador : IGUAL IGUAL
                    | MAYORQUE IGUAL
                    | MENORQUE IGUAL
                    | MAYORQUE
                    | MENORQUE
                    | NOT IGUAL
    '''
def p_expresionesbool(p):
    '''expresionesbool : exprbool
                         | NOT exprbool
                         | exprbool AND LPAREN expresionesbool RPAREN
                         | exprbool OR LPAREN expresionesbool RPAREN
    '''

def p_exprbool(p):
    '''exprbool : valor comparador valor
                  | ID IS tipodato
                  | valorbool
                  | ID comparador ID
    '''

def p_valor(p):
    '''valor : CADENA
            | FLOAT_NUMBER
            | NUMBER'''

def p_error(p):
    print("Error de sintaxis en la linea %d" % p.lineno)

parser = yacc.yacc()

while True:
    try:
        s = input('python > ')
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    print(result)