import ply.yacc as yacc
from AnalizadorLexDart import tokens, lexer

#TABLA DE SIMBOLOS
tabla_simbolos={
    'variables':{},
    'tipos':{
        'str_funciones':['split','contains','startsWith','endsWith','toUpperCase','toLowerCase','substring','trim','replaceAll']
    }
}

start = 'sentencias'

def contiene_return(sentencias):
    if not sentencias:
        return False
    if isinstance(sentencias, str):
        return 'return' in sentencias
    if isinstance(sentencias, dict):
        if sentencias.get('type') == 'RETURN' or sentencias.get('node') == 'RETURN':
            return True
        for v in sentencias.values():
            if contiene_return(v):
                return True
        return False
    if isinstance(sentencias, list):
        for s in sentencias:
            if contiene_return(s):
                return True
        return False
    if hasattr(sentencias, 'tiene_return'):
        try:
            return sentencias.tiene_return()
        except Exception:
            return False
    return False

def p_sentencias(p):
    '''sentencias : sentencias sentencia
                  | sentencia'''
    if len(p) == 3:
        a = p[1]
        b = p[2]
        if isinstance(a, list):
            a.append(b)
            p[0] = a
        else:
            p[0] = [a, b]
    else:
        p[0] = p[1]

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
                | declaracion_func_retorno
    '''
    p[0] = p[1]

def p_asignacion_variables(p):
    'asignacion_variables : ID IGUAL valor SEMICOLON'
    nombre = p[1]
    valor_dict = p[3]

    if nombre in tabla_simbolos['variables']:
        tipo_existente = tabla_simbolos['variables'][nombre]
        if tipo_existente.upper() == valor_dict['type'].upper():
            print(f"Asignación correcta: {nombre} = {valor_dict['value']}")
        else:
            print(f"Error Semántico: {nombre} es {tipo_existente}, no se le puede asignar {valor_dict['type']}")
    else:
        print(f"Error Semántico: Variable '{nombre}' no declarada.")


def p_declaracion_variables(p):
    '''declaracion_variables : tipodato ID IGUAL valor SEMICOLON
                            | VAR ID IGUAL valor SEMICOLON'''


    tipo_variable = p[1]
    nombre = p[2]
    valor = p[4]  # Esto ahora espera un diccionario {type, value}

    # Lógica de VAR (Inferencia de tipos)
    if tipo_variable == 'var':
        tabla_simbolos['variables'][nombre] = valor['type']
        print(f"Declaración (Inferencia): {nombre} es de tipo {valor['type']}")
        return

    # Lógica de Tipos Explícitos con Conversión
    tipo_var_upper = tipo_variable.upper()
    tipo_val_upper = valor['type'].upper()

    if tipo_var_upper == tipo_val_upper:
        # Tipos identicos todo bien
        tabla_simbolos['variables'][nombre] = tipo_variable
        print(tabla_simbolos)

    elif tipo_var_upper == 'FLOAT' and tipo_val_upper == 'INT':
        # CONVERSIÓN IMPLÍCITA: Se permite guardar int en float
        print(f"Aviso: Conversión implícita de INT a FLOAT para variable '{nombre}'")
        tabla_simbolos['variables'][nombre] = 'FLOAT'  # Se guarda como float

    else:
        print(
            f"Error Semántico: No se puede asignar '{tipo_val_upper}' a variable '{nombre}' de tipo '{tipo_var_upper}'")

def p_declaracion_func_void(p):
    '''declara_func_void : VOID ID LPAREN RPAREN LBRACKET sentencias RBRACKET
                        | VOID ID LPAREN parametros RPAREN LBRACKET sentencias RBRACKET
    '''
    nombre = p[2]
    if 'funciones' not in tabla_simbolos:
        tabla_simbolos['funciones'] = {}
    if nombre in tabla_simbolos['funciones']:
        print(f"Error semántico: funcion {nombre} ya declarada")
        p[0] = {'type': 'ERROR'}
        return
    if len(p) == 8:
        parametros = []
        sentencias = p[6]
        linea = p.lineno(1)
    else:
        parametros = p[4] or []
        sentencias = p[7]
        linea = p.lineno(1)
    tienereturn = contiene_return(sentencias)
    if tienereturn:
        print(f"Error semántico: funcion {nombre} es void y no debe retornar valores.")
    tabla_simbolos['funciones'][nombre] = {
        'tipo': 'VOID',
        'parametros': parametros,
        'sentencias': sentencias,
        'linea': linea
    }
    p[0] = {'node': 'funcion', 'nombre': nombre, 'tipo': 'VOID'}

def p_declaracion_func_retorno(p):
    'declaracion_func_retorno : tipodato ID LPAREN RPAREN LBRACKET sentencias RETURN valorreturn RBRACKET'
    nombre = p[2]
    tipo_retorno = p[1]
    valor_retorno = p[8]
    if 'funciones' not in tabla_simbolos:
        tabla_simbolos['funciones'] = {}
    if nombre in tabla_simbolos['funciones']:
        print(f"Error semántico: funcion {nombre} ya declarada")
        p[0] = {'type': 'ERROR'}
        return
    valor_tipo = None
    if isinstance(valor_retorno, dict):
        valor_tipo = valor_retorno.get('type')
    elif isinstance(valor_retorno, str):
        valor_tipo = valor_retorno.upper()
    if valor_tipo is None:
        print(f"Error semántico: no se pudo determinar tipo de retorno en funcion {nombre}")
        tabla_simbolos['funciones'][nombre] = {'tipo': 'ERROR'}
        p[0] = {'type': 'ERROR'}
        return
    if str(valor_tipo).upper() != str(tipo_retorno).upper():
        print(f"Error semántico: tipo de funcion {tipo_retorno} es diferente al tipo de valor de retorno {valor_tipo}")
    tabla_simbolos['funciones'][nombre] = {'tipo': str(tipo_retorno).upper(), 'return_type': str(valor_tipo).upper(),
                                           'sentencias': p[6], 'linea': p.lineno(1)}
    p[0] = {'node': 'funcion', 'nombre': nombre, 'tipo': str(tipo_retorno).upper()}

def p_declaracion_list(p):
    '''declaracion_list : tipodato ID IGUAL LCORCH RCORCH SEMICOLON
                        | VAR ID IGUAL LCORCH RCORCH SEMICOLON
                        | VAR ID IGUAL LCORCH valoresenlistados RCORCH SEMICOLON
                        | tipodato ID IGUAL LCORCH valoresenlistados RCORCH SEMICOLON
    '''
    p[0] = p[1]

def p_sentenciawhile(p):
    '''sentenciawhile : WHILE LPAREN exp_logica RPAREN LBRACKET sentencias RBRACKET
                       | WHILE LPAREN exp_logica RPAREN LBRACKET sentencias RETURN valorreturn RBRACKET
    '''
    condicion = p[3]
    if condicion['type'] == 'BOOL':
        print("Sentencia WHILE válida semánticamente.")
    else:
        print(
            f"Error Semántico en WHILE (línea {p.lineno(1)}): La condición debe ser booleana. Se encontró: {condicion['type']}")

def p_imprimircadena(p):
    'imprimircadena : PRINT LPAREN CADENA RPAREN SEMICOLON'
    p[0] = {'type':'VOID'}


def p_imprimirvariable(p):
    'imprimirvariable : PRINT LPAREN ID RPAREN SEMICOLON'
    nombre = p[3]
    if nombre not in tabla_simbolos['variables']:
        print(f"Error semantico: variable {nombre} no declarada")
        p[0] = {'type': 'ERROR'}
    else:
        p[0] = {'type': tabla_simbolos['variables'][nombre]}


def p_imprimirexpresion(p):
    'imprimirexpresion : PRINT LPAREN expresion RPAREN SEMICOLON'

def p_expresionaritmetica(p):
    '''expresionaritmetica : expresionaritmetica PLUS expresionaritmetica
                            | expresionaritmetica MINUS expresionaritmetica
                            | expresionaritmetica TIMES expresionaritmetica
                            | expresionaritmetica DIVIDE expresionaritmetica
                            | valoresnumericos
                            | ID
                            | LPAREN expresionaritmetica RPAREN
    '''

    if len(p) == 2:
        if isinstance(p[1], dict):
            p[0] = p[1]
        elif isinstance(p[1], str):
            tipo = tabla_simbolos['variables'].get(p[1], 'ERROR')
            p[0] = {'type' : tipo, 'value': p[1]}
        else:
            p[0] = {'type' : 'ERROR', 'value': None}

    elif len(p) == 4:
        if p[1] == '(':
            p[0] = p[2]
        else:
            op1 = p[1]
            operador = p[2]
            op2 = p[3]
            tipo_final = obtener_tipo_resultante(op1['type'], op2['type'])

            if tipo_final:
                if operador == '/':
                    tipo_final = 'FLOAT'
                p[0] = {'type': tipo_final, 'value': f"{op1['value']} {operador} {op2['value']}"}
            else:
                print(
                    f"Error Semántico: Tipos incompatibles para operación '{operador}': {op1['type']} y {op2['type']}")
                p[0] = {'type': 'ERROR', 'value': None}

def p_expresion(p):
    '''expresion : valor PLUS valor
                | valor MINUS valor
                | expresionaritmetica
                | concatenarcadenas

    '''

def p_concatenarcadenas(p):
    'concatenarcadenas : valor PLUS valor'
    op1 = p[1]
    op2 = p[3]
    if isinstance(op1, str):
        tipo1 = tabla_simbolos['variables'].get(op1, 'ERROR')
        op1 = {'type': tipo1, 'value': op1}
    if isinstance(op2, str):
        tipo2 = tabla_simbolos['variables'].get(op2, 'ERROR')
        op2 = {'type': tipo2, 'value': op2}

    if op1['type'].upper() == 'STRING' and op2['type'].upper() == 'STRING':
        p[0] = {'type': 'STRING', 'value': f"{op1['value']} + {op2['value']}"}
    else:
        print(
            f"Error Semántico: Concatenación solo permitida entre STRING, pero se recibió {op1['type']} y {op2['type']}")
        p[0] = {'type': 'ERROR', 'value': None}



def p_parametro(p):
    'parametro : tipodato ID'
    p[0] = {'tipo': str(p[1]).upper(), 'nombre': p[2]}

def p_parametros(p):
    '''parametros : parametro
                    | parametros COMA parametro
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        lst = p[1]
        lst.append(p[3])
        p[0] = lst

def p_return_void(p):
    'return_void : RETURN SEMICOLON'
    p[0] = {'type': 'RETURN', 'value': None}

def p_return_valor(p):
    'return_valor : RETURN valor SEMICOLON'
    p[0] = {'type': 'RETURN', 'value': p[2]}

def p_valorreturn(p):
    '''valorreturn : ID SEMICOLON
                    | valor SEMICOLON
    '''
    if isinstance(p[1], dict):
        p[0] = p[1]
    else:
        nombre = p[1]
        if nombre in tabla_simbolos['variables']:
            p[0] = {'type': tabla_simbolos['variables'][nombre], 'value': nombre}
        else:
            print(f"Error Semántico: Variable '{nombre}' no declarada en return")
            p[0] = {'type': 'ERROR'}

def p_valoresnumericos(p):
    '''valoresnumericos : NUMBER
                        | FLOAT_NUMBER
    '''
    if p.slice[1].type == "NUMBER":
        p[0] = {'type': 'INT', 'value': p[1]}
    elif p.slice[1].type == "FLOAT_NUMBER":
        p[0] = {'type': 'FLOAT', 'value': p[1]}

#Estructura Cola
def p_factoryqueue(p):
    ''' factoryqueue : QUEUE MENORQUE tipodato MAYORQUE ID IGUAL QUEUE MENORQUE tipodato MAYORQUE LPAREN RPAREN SEMICOLON
    '''
    p[0] = p[1]

def p_explicitqueue(p):
    ''' explicitqueue : LIST_QUEUE MENORQUE tipodato MAYORQUE ID IGUAL LIST_QUEUE MENORQUE tipodato MAYORQUE LPAREN RPAREN SEMICOLON
        | QUEUE MENORQUE tipodato MAYORQUE ID IGUAL LIST_QUEUE MENORQUE tipodato MAYORQUE LPAREN RPAREN SEMICOLON
    '''
    p[0] = p[1]

def p_valoresenlistados(p):
    '''valoresenlistados : valor COMA valor
                        | valor COMA valoresenlistados
    '''
    if len(p) == 4 and isinstance(p[3], list):
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1], p[3]]

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
    p[0] = p[1]

def p_forcomparador(p):
    '''forcomparador : MENORQUE
                       | MAYORQUE
                       | NOT IGUAL
    '''
    p[0] = p[1]

def p_forunarios(p):
    '''forunarios : PLUS PLUS
                        | MINUS MINUS
                         '''
    p[0] = p[1]


def p_sentenciaif(p):
    '''sentenciaif : IF LPAREN exp_logica RPAREN LBRACKET sentencias RETURN valorreturn RBRACKET
                    | IF LPAREN exp_logica RPAREN LBRACKET sentencias RBRACKET
    '''
    condicion = p[3]
    if condicion['type'] == 'BOOL':
        print("Sentencia IF válida semánticamente.")
    else:
        print(
            f"Error Semántico en IF (línea {p.lineno(1)}): La condición debe ser booleana. Se encontró: {condicion['type']}")

def p_valorbool(p):
    '''valorbool : TRUE
                   | FALSE
    '''
    p[0] = {'type': 'BOOL', 'value': p[1]}

def p_comparador(p):
    '''comparador : IGUAL IGUAL
                    | MAYORQUE IGUAL
                    | MENORQUE IGUAL
                    | MAYORQUE
                    | MENORQUE
                    | NOT IGUAL
    '''
    p[0] = p[1]

def p_valor(p):
    '''
    valor : valoresnumericos
            | CADENA
            | ID
    '''
    token_type = p.slice[1].type

    if token_type == "ID":
        nombre = p[1]
        if nombre not in tabla_simbolos['variables']:
            tipo_guardado = tabla_simbolos['variables'][nombre]
            p[0] = {'type': tipo_guardado, 'value': nombre}
        else:
            print(f"Error Semántico: Variable '{nombre}' no declarada")
            p[0] = {'type': 'ERROR', 'value': None}
    elif token_type == "CADENA":
        p[0] = {'type': 'STRING', 'value': p[1]}
    else:
        p[0] = p[1]

def p_lambda_function(p):
    '''
    lambda_function : tipodato ID  LPAREN parametros RPAREN LAMBDA expresion SEMICOLON
    '''

def p_condition(p):
    '''
    condition : valor comparador valor
              | valorbool comparador valorbool
              | valor comparador valorbool
              | valorbool comparador valor
    '''
    left = p[1]
    right = p[3]
    op = p[2]

    tipos_numericos = ['INT', 'FLOAT']

    es_num = (left['type'].upper() in tipos_numericos) and (right['type'].upper() in tipos_numericos)
    es_bool = (left['type'] == 'BOOL') and (right['type'] == 'BOOL')

    if es_num or es_bool:
        p[0] = {'type': 'BOOL', 'value': f"{left['value']} {op} {right['value']}"}
    else:
        print(f"Error Semántico: No se pueden comparar tipos incompatibles: {left['type']} con {right['type']}")
        p[0] = {'type': 'ERROR'}

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
    if len(p) == 4 and p[2] != '(':
        left = p[1]
        right = p[3]
        if left['type'] == 'BOOL' and right['type'] == 'BOOL':
            p[0] = {'type': 'BOOL', 'value': f"{left['value']} {p[2]} {right['value']}"}
        else:
            print(f"Error Semántico: Operación lógica requiere booleanos. Se encontró {left['type']} y {right['type']}")
            p[0] = {'type': 'ERROR'}
    elif len(p) == 3:
        op = p[2]
        if op['type'] == 'BOOL':
            p[0] = {'type': 'BOOL', 'value': f"NOT {op['value']}"}
        else:
            print("Error Semántico: NOT solo aplica a booleanos")
            p[0] = {'type': 'ERROR'}
    elif len(p) == 4 and p[1] == '(':
        p[0] = p[2]
    elif len(p) == 2 and isinstance(p[1], str):
        nombre = p[1]
        if nombre in tabla_simbolos['variables']:
            if tabla_simbolos['variables'][nombre] == 'BOOL':
                p[0] = {'type': 'BOOL', 'value': nombre}
            else:
                print(f"Error Semántico: Variable '{nombre}' no es booleana.")
                p[0] = {'type': 'ERROR'}
        else:
            p[0] = p[1]
    else:
        p[0] = p[1]

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
                   | ABSTRACT CLASS LBRACKET RBRACKET
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


def obtener_tipo_resultante(tipo1, tipo2):
    t1 = tipo1.upper()
    t2 = tipo2.upper()

    if t1 == t2:
        return t1

    if (t1 == 'INT' and t2 == 'FLOAT') or (t1 == 'FLOAT' and t2 == 'INT'):
        return 'FLOAT'

    if t1 == 'STRING' or t2 == 'STRING':
        return 'STRING'

    return None


def p_conversion_explicita(p):
    '''valor : valor AS tipodato'''

    origen = p[1]  # Diccionario {type, value}
    destino = p[3]  # String 'int', 'float', etc.

    if origen['type'].upper() == 'FLOAT' and destino.upper() == 'INT':
        p[0] = {'type': 'INT', 'value': f"({origen['value']}).toInt()"}  # O sintaxis Python int()

    elif origen['type'].upper() == 'INT' and destino.upper() == 'FLOAT':
        p[0] = {'type': 'FLOAT', 'value': f"({origen['value']}).toDouble()"}

    else:
        print(f"Error Semántico: No se puede castear {origen['type']} a {destino}")
        p[0] = {'type': 'ERROR'}


def p_string_methods(p):
    'valor : ID PUNTO ID LPAREN RPAREN SEMICOLON'
    nombre = p[1]
    metodo = p[3]
    if nombre not in tabla_simbolos['variables']:
        print(f"Error semantico: la variable {nombre} no ha sido definida.")
    elif tabla_simbolos["variables"][nombre] != 'String':
        print(f"Error semantico: la variable {nombre} no corresponde a un str.")
    else:
        if metodo in tabla_simbolos['tipos']['str_funciones']:
            p[0] = "str"
        else:
            print(f"Error semantico: el metodo {metodo} no es parte de las funciones de strings.")


parser = yacc.yacc()

def p_error(p):
    if p is None:
        print("Error de sintaxis: se encontró el final inesperado de la entrada.")
        return

    print(f"Error de sintaxis en la línea {p.lineno}: token inesperado '{p.value}'")

while True:
    try:
        s = input('dart > ')
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    print(result)
