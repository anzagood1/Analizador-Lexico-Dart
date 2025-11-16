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
                | if_else
                | if_else_if
                | expresionaritmetica
                | imprimircadena
                | imprimirvariable
                | imprimirexpresion
                | concatenarcadenas
                | factoryqueue
                | explicitqueue
                | funcion_asincrona
                | declaracion_con_await
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
    '''declaracion_list : tipodato ID IGUAL LCORCH RCORCH SEMICOLON
                        | VAR ID IGUAL LCORCH RCORCH SEMICOLON
                        | VAR ID IGUAL LCORCH valoresenlistados RCORCH SEMICOLON
                        | tipodato ID IGUAL LCORCH valoresenlistados RCORCH SEMICOLON
    '''

def p_sentenciawhile(p):
    '''sentenciawhile : WHILE LPAREN exp_logica RPAREN LBRACKET sentencias RBRACKET
                        | WHILE LPAREN exp_logica RPAREN LBRACKET sentencias RETURN valorreturn RBRACKET
    '''

def p_imprimircadena(p):
    'imprimircadena : PRINT LPAREN CADENA RPAREN SEMICOLON'

def p_imprimirvariable(p):
    'imprimirvariable : PRINT LPAREN ID RPAREN SEMICOLON'

def p_imprimirexpresion(p):
    'imprimirexpresion : PRINT LPAREN expresion RPAREN SEMICOLON'

def p_expresionaritmetica(p):
    '''expresionaritmetica : valoresnumericos PLUS valoresnumericos
                        | valoresnumericos MINUS valoresnumericos
                        | valoresnumericos TIMES valoresnumericos
                        | valoresnumericos DIVIDE valoresnumericos
                        | ID TIMES ID
                        | ID DIVIDE ID
    '''

def p_expresion(p):
    '''expresion : valor PLUS valor
                | valor MINUS valor
                | expresionaritmetica
    '''

def p_concatenarcadenas(p):
    'concatenarcadenas : CADENA PLUS CADENA SEMICOLON'

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
#Estructura Cola
def p_factoryqueue(p):
    ''' factoryqueue : QUEUE MENORQUE tipodato MAYORQUE ID IGUAL QUEUE MENORQUE tipodato MAYORQUE LPAREN RPAREN SEMICOLON
    '''

def p_explicitqueue(p):
    ''' explicitqueue : LIST_QUEUE MENORQUE tipodato MAYORQUE ID IGUAL LIST_QUEUE MENORQUE tipodato MAYORQUE LPAREN RPAREN SEMICOLON
        | QUEUE MENORQUE tipodato MAYORQUE ID IGUAL LIST_QUEUE MENORQUE tipodato MAYORQUE LPAREN RPAREN SEMICOLON
    '''

def p_valoresenlistados(p):
    '''valoresenlistados : valor COMA valor
                        | valor COMA valoresenlistados
    '''

def p_sentenciafor(p):
    '''sentenciafor : FOR LPAREN VAR ID IGUAL NUMBER SEMICOLON exp_logica SEMICOLON ID forunarios RPAREN LBRACKET sentencias RBRACKET
                        | FOR LPAREN INT ID IGUAL NUMBER SEMICOLON exp_logica SEMICOLON ID forunarios RPAREN LBRACKET sentencias RBRACKET
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

#Estructura if else / if else if

def p_sentencia_else(p):
    '''
    sentencia_else : ELSE LBRACKET sentencias RBRACKET
                   | ELSE LBRACKET sentencias RETURN valorreturn RBRACKET

    '''

def p_sentencia_elif(p):
    '''
    sentencia_elif : ELSE IF LPAREN exp_logica RPAREN LBRACKET sentencias RBRACKET
                   | ELSE IF LPAREN exp_logica RPAREN LBRACKET sentencias RETURN valorreturn RBRACKET
    '''
def p_elif_nest(p):
    '''
    elif_nest : sentencia_elif
              | elif_nest sentencia_elif
    '''
def p_if_else(p):
    'if_else : sentenciaif sentencia_else'

def p_if_else_if(p):
    '''
    if_else_if : sentenciaif elif_nest sentencia_else
               | sentenciaif elif_nest
    '''


#USO DE CLASES ABSTRACTAS
def p_abstract_f(p):
    '''
    abstract_f : tipodato ID LPAREN RPAREN SEMICOLON
                | VOID ID LPAREN RPAREN SEMICOLON
    '''

def p_abstract_sent(p):
    '''
    abstract_sent : abstract_f
                    | abstract_sent abstract_f
    '''
def p_abstractclass(p):
    '''
    abstract_class : ABSTRACT CLASS LBRACKET abstract_sent RBRACKET
    abstract_class: ABSTRACT CLASS LBRACKET RBRACKET
    '''

def p_class_declare(p):
    '''
    class_declare : CLASS ID LBRACKET sentencias RBRACKET
                  | CLASS ID IMPLEMENTS ID LBRACKET sentencias RBRACKET
    '''

def p_funcion_asincrona(p):
    '''
    funcion_asincrona : MENORQUE FUTURE MAYORQUE ID LPAREN RPAREN LBRACKET RETURN FUTURE RBRACKET
                        | tipodato ID LPAREN RPAREN ASYNC LBRACKET sentencia RBRACKET
    '''

def p_declaracion_con_await(p):
    '''
    declaracion_con_await : tipodato ID IGUAL AWAIT ID LPAREN RPAREN SEMICOLON
    '''


parser = yacc.yacc()

while True:
    try:
        s = input('python > ')
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    print(result)
