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
                | condition
                | exp_logica
                | declaracion_list
                | sentenciawhile
                | parametros
                | comparador
                | sentenciafor
                | forcomparador
                | forunarios
                | lambda_function
                | set_declare
                | set_literal
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
    '''sentenciawhile : WHILE LPAREN exp_logica RPAREN RBRACKET sentencias RBRACKET
                        | WHILE LPAREN exp_logica RPAREN RBRACKET sentencias RETURN valorreturn RBRACKET
    '''

def p_imprimircadena(p):
    'imprimircadena : PRINT LPAREN CADENA RPAREN SEMICOLON'

def p_imprimirvariable(p):
    'imprimirvariable : PRINT LPAREN ID RPAREN SEMICOLON'

def p_imprimirexpresion(p):
    'imprimirexpresion : PRINT LPAREN expresion RPAREN SEMICOLON'

def p_expresionaritmetica(p):
    '''exprearitmetica : valoresnumericos PLUS valoresnumericos
                        | valoresnumericos MINUS valoresnumericos
                        | valoresnumericos TIMES valoresnumericos
                        | valoresnumericos DIVIDE valoresnumericos
                        | ID TIMES ID
                        | ID DIVIDE ID
    '''

def p_expresion(p):
    '''expresion : valor PLUS valor
                | valor MINUS valor
                | exprearitmetica
    '''

def p_parametro(p):
    'parametro : tipodato ID'

def p_parametros(p):
    '''parametros : parametro
                    | parametros COMA parametro
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
    '''sentenciaif : IF LPAREN exp_logica RPAREN LBRACKET sentencias RETURN valorreturn RBRACKET
                    | IF LPAREN exp_logica RPAREN LBRACKET sentencias RBRACKET
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

def p_valor(p):
    '''
    valor : ID
            | valoresnumericos
            | CADENA
    '''

#Lambda function

def p_lambda_function(p):
    '''
    lambda_function : tipodato ID  LPAREN parametros RPAREN LAMBDA expresion SEMICOLON
    '''

#expresiones relacionales
def p_condition(p):
    '''
    condition : valor comparador valor
              | valorbool comparador valorbool
              | valor comparador valorbool
              | valorbool comparador valor
    '''

#expresiones logicas


def p_exp_logica(p):
    '''
    exp_logica : exp_logica OR exp_logica
                | exp_logica AND exp_logica
                | NOT exp_logica
                | LPAREN exp_logica RPAREN
                | condition
                | valorbool
                | ID
    '''

#Estructura de datos: SET

def p_elements(p):
    '''
    elements : valor
            | elements COMA valor
    '''

def p_set_literal(p):
    '''
    set_literal : LBRACKET RBRACKET
                | LBRACKET elements RBRACKET
    '''

def p_set_declare(p):
    '''
    set_declare : VAR ID IGUAL MENORQUE tipodato MAYORQUE set_literal SEMICOLON
                | SET MENORQUE tipodato MAYORQUE ID IGUAL set_literal SEMICOLON
    '''

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