import ply.yacc as yacc
from AnalizadorLexDart import tokens, lexer, errores_lexicos

# --- GESTIÓN DE SALIDAS PARA INTERFAZ ---
resultados_analisis = []


def log_resultado(mensaje):
    """Guarda los mensajes en lugar de imprimir"""
    resultados_analisis.append(mensaje)


# TABLA DE SIMBOLOS
tabla_simbolos = {
    'variables': {},
    'funciones': {},
    'tipos': {
        'str_funciones': ['split', 'contains', 'startsWith', 'endsWith', 'toUpperCase', 'toLowerCase', 'substring',
                          'trim', 'replaceAll', 'toString', 'isEmpty', 'length']
    }
}

start = 'sentencias'


# --- HELPER PARA EVITAR CRASHES ---
def normalizar_token(token):
    if isinstance(token, dict): return token
    if isinstance(token, str):
        tipo = tabla_simbolos['variables'].get(token, 'ERROR')
        if tipo == 'ERROR' and (token.startswith("'") or token.startswith('"')):
            tipo = 'STRING'
        # Intento de inferencia básica para listas
        if tipo == 'ERROR' and token.startswith('['):
            tipo = 'LIST'
        return {'type': tipo, 'value': token}
    return {'type': 'ERROR', 'value': str(token)}


def contiene_return(sentencias):
    if not sentencias: return False
    if isinstance(sentencias, str): return 'return' in sentencias
    if isinstance(sentencias, dict):
        if sentencias.get('type') == 'RETURN': return True
        for v in sentencias.values():
            if contiene_return(v): return True
        return False
    if isinstance(sentencias, list):
        for s in sentencias:
            if contiene_return(s): return True
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
                | return_void
                | return_valor
                | class_declare
                | abstract_class
                | llamada_funcion_sentencia
    '''
    p[0] = p[1]


# Permite llamadas a funciones como sentencias sueltas (void)
def p_llamada_funcion_sentencia(p):
    'llamada_funcion_sentencia : ID LPAREN argumentos RPAREN SEMICOLON'
    log_resultado(f"Llamada a función: {p[1]}(...)")
    p[0] = {'type': 'VOID'}


def p_asignacion_variables(p):
    'asignacion_variables : ID IGUAL expresion SEMICOLON'
    nombre = p[1]
    valor_dict = normalizar_token(p[3])

    if nombre in tabla_simbolos['variables']:
        tipo_existente = tabla_simbolos['variables'][nombre]

        # Validación laxa para listas y genéricos
        if 'LIST' in str(tipo_existente).upper() and 'LIST' in str(valor_dict['type']).upper():
            log_resultado(f"Asignación de Lista: {nombre} = {valor_dict.get('value')}")
        elif str(tipo_existente).upper() == str(valor_dict['type']).upper():
            log_resultado(f"Asignación correcta: {nombre} = {valor_dict.get('value')}")
        elif tipo_existente == 'FLOAT' and valor_dict['type'] == 'INT':
            log_resultado(f"Asignación (Cast INT->FLOAT): {nombre} = {valor_dict.get('value')}")
        else:
            # Fallback para casos complejos no resueltos por el parser simple
            log_resultado(
                f"Asignación (Posible): {nombre} = {valor_dict.get('value')} (Tipos: {tipo_existente} vs {valor_dict['type']})")
    else:
        log_resultado(f"Error Semántico: Variable '{nombre}' no declarada.")


def p_declaracion_variables(p):
    '''declaracion_variables : tipodato ID IGUAL expresion SEMICOLON
                            | VAR ID IGUAL expresion SEMICOLON
                            | FINAL ID IGUAL expresion SEMICOLON
                            | CONST ID IGUAL expresion SEMICOLON'''

    tipo_variable = p[1]
    nombre = p[2]
    valor = normalizar_token(p[4])

    # Registro en tabla de símbolos
    tabla_simbolos['variables'][nombre] = tipo_variable
    log_resultado(f"Declaración: {nombre} de tipo {tipo_variable}")


def p_declaracion_func_void(p):
    '''declara_func_void : VOID ID LPAREN RPAREN LBRACKET sentencias RBRACKET
                        | VOID ID LPAREN parametros RPAREN LBRACKET sentencias RBRACKET
    '''
    nombre = p[2]
    if len(p) == 8:
        parametros = []
        sentencias = p[6]
    else:
        parametros = p[4] or []
        sentencias = p[7]

    tabla_simbolos['funciones'][nombre] = {'tipo': 'VOID', 'parametros': parametros}
    log_resultado(f"Función VOID declarada: {nombre}")
    p[0] = {'node': 'funcion', 'nombre': nombre, 'tipo': 'VOID'}


def p_declaracion_func_retorno(p):
    '''declaracion_func_retorno : tipodato ID LPAREN RPAREN LBRACKET sentencias RETURN valorreturn RBRACKET
                                | tipodato ID LPAREN parametros RPAREN LBRACKET sentencias RETURN valorreturn RBRACKET'''

    # Manejo de índices dependiendo si tiene parámetros
    idx_nombre = 2
    idx_sentencias = 6
    idx_return = 8

    if p[4] != ')':  # Tiene parámetros
        idx_sentencias = 7
        idx_return = 9

    nombre = p[idx_nombre]
    tipo_retorno = p[1]

    tabla_simbolos['funciones'][nombre] = {'tipo': str(tipo_retorno).upper()}
    log_resultado(f"Función declarada: {nombre} retorna {tipo_retorno}")
    p[0] = {'node': 'funcion', 'nombre': nombre, 'tipo': str(tipo_retorno).upper()}


def p_sentenciawhile(p):
    '''sentenciawhile : WHILE LPAREN exp_logica RPAREN LBRACKET sentencias RBRACKET
    '''
    log_resultado("Sentencia WHILE analizada.")


def p_imprimircadena(p):
    'imprimircadena : PRINT LPAREN CADENA RPAREN SEMICOLON'
    log_resultado(f"Consola: {p[3]}")
    p[0] = {'type': 'VOID'}


def p_imprimirvariable(p):
    'imprimirvariable : PRINT LPAREN ID RPAREN SEMICOLON'
    # Esta regla a veces entra en conflicto con exp_aritmetica -> ID, pero se mantiene por precedencia
    nombre = p[3]
    log_resultado(f"Consola (Variable): {nombre}")


def p_imprimirexpresion(p):
    'imprimirexpresion : PRINT LPAREN expresion RPAREN SEMICOLON'
    # Captura general para print("texto $var") que entra como String complejo o concatenación
    log_resultado(f"Consola: {p[3].get('value')}")


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
        p[0] = normalizar_token(p[1])
    elif len(p) == 4:
        if p[1] == '(':
            p[0] = p[2]
        else:
            op1 = normalizar_token(p[1])
            op2 = normalizar_token(p[3])
            p[0] = {'type': 'NUM', 'value': f"{op1.get('value')} {p[2]} {op2.get('value')}"}


def p_expresion(p):
    '''expresion : valor PLUS valor
                | valor MINUS valor
                | expresionaritmetica
                | concatenarcadenas
                | valor
    '''
    p[0] = p[1]


def p_concatenarcadenas(p):
    'concatenarcadenas : valor PLUS valor'
    p[0] = {'type': 'STRING', 'value': "Concatenacion"}


def p_parametro(p):
    'parametro : tipodato ID'
    # Registramos el parametro como variable local para que el cuerpo de la funcion lo reconozca
    tabla_simbolos['variables'][p[2]] = p[1]
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
    p[0] = {'type': 'RETURN', 'value': normalizar_token(p[2])}


def p_valorreturn(p):
    '''valorreturn : ID SEMICOLON
                    | valor SEMICOLON
    '''
    p[0] = normalizar_token(p[1])


def p_valoresnumericos(p):
    '''valoresnumericos : NUMBER
                        | FLOAT_NUMBER
    '''
    if p.slice[1].type == "NUMBER":
        p[0] = {'type': 'INT', 'value': p[1]}
    else:
        p[0] = {'type': 'FLOAT', 'value': p[1]}


# Queue structures (simplified)
def p_factoryqueue(p):
    ''' factoryqueue : QUEUE MENORQUE tipodato MAYORQUE ID IGUAL QUEUE MENORQUE tipodato MAYORQUE LPAREN RPAREN SEMICOLON
    '''
    p[0] = p[1]


def p_explicitqueue(p):
    ''' explicitqueue : LIST_QUEUE MENORQUE tipodato MAYORQUE ID IGUAL LIST_QUEUE MENORQUE tipodato MAYORQUE LPAREN RPAREN SEMICOLON
    '''
    p[0] = p[1]


# --- MANEJO DE LISTAS Y ARGUMENTOS ---

def p_valoresenlistados(p):
    '''valoresenlistados : valor COMA valor
                        | valor COMA valoresenlistados
                        | valor
    '''
    # Simplificación: retorna un string representativo
    p[0] = "lista_elementos"


def p_argumentos(p):
    '''argumentos : valor
                  | argumentos COMA valor
                  | empty'''
    pass


def p_empty(p):
    'empty :'
    pass


# --- FOR LOOP ---
def p_for_init(p):
    '''for_init : VAR ID IGUAL NUMBER
                | INT ID IGUAL NUMBER'''
    tabla_simbolos['variables'][p[2]] = 'INT'
    p[0] = p[2]


def p_sentenciafor(p):
    '''sentenciafor : FOR LPAREN for_init SEMICOLON exp_logica SEMICOLON ID forunarios RPAREN LBRACKET sentencias RBRACKET
                    | FOR LPAREN VAR ID IN ID RPAREN LBRACKET sentencias RBRACKET
                    | FOR LPAREN tipodato ID IN ID RPAREN LBRACKET sentencias RBRACKET'''

    # En el caso 2 y 3 (for-in), registramos la variable iteradora
    if len(p) == 11:
        nombre_var = p[3]  # VAR ID
        if p[3] != 'var': nombre_var = p[4]  # tipodato ID
        tabla_simbolos['variables'][nombre_var] = 'ITERATOR'

    log_resultado("Sentencia FOR válida.")


# --- TIPOS DE DATOS (INCLUYENDO LISTAS GENÉRICAS) ---
def p_tipodato(p):
    '''tipodato : STRING
                    | INT
                    | FLOAT
                    | BOOL
                    | LIST MENORQUE tipodato MAYORQUE
                    | LIST
    '''
    if len(p) == 5:  # List<int>
        p[0] = f"List<{p[3]}>"
    else:
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
    log_resultado("Sentencia IF válida.")


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


# --- VALOR: EL NÚCLEO DE EXPRESIONES ---
def p_valor(p):
    '''
    valor : valoresnumericos
            | CADENA
            | ID
            | valorbool
            | ID PUNTO ID LPAREN RPAREN
            | ID PUNTO ID
            | ID LPAREN argumentos RPAREN
            | ID LPAREN RPAREN
            | ID LCORCH valor RCORCH
            | LCORCH valoresenlistados RCORCH
            | LCORCH RCORCH
    '''
    # ID.metodo()
    if len(p) == 6 and p[2] == '.':
        p[0] = {'type': 'UNKNOWN', 'value': f"{p[1]}.{p[3]}()"}
    # ID.propiedad (ej: lista.isEmpty)
    elif len(p) == 4 and p[2] == '.':
        p[0] = {'type': 'BOOL', 'value': f"{p[1]}.{p[3]}"}  # Asumimos bool para isEmpty
    # ID(args) - Llamada funcion
    elif len(p) == 5 and p[2] == '(':
        p[0] = {'type': 'UNKNOWN', 'value': f"{p[1]}(...)"}
    # ID()
    elif len(p) == 4 and p[2] == '(':
        p[0] = {'type': 'UNKNOWN', 'value': f"{p[1]}()"}
    # ID[index] - Acceso array
    elif len(p) == 5 and p[2] == '[':
        p[0] = {'type': 'UNKNOWN', 'value': f"{p[1]}[...]"}
    # [1, 2] - Literal lista
    elif len(p) == 4 and p[1] == '[':
        p[0] = {'type': 'LIST', 'value': "ListLiteral"}
    # [] - Lista vacia
    elif len(p) == 3 and p[1] == '[':
        p[0] = {'type': 'LIST', 'value': "EmptyList"}
    # Valores simples
    elif len(p) == 2:
        token_type = p.slice[1].type
        if token_type == "ID":
            p[0] = normalizar_token(p[1])
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
    # Simplificado para evitar errores semánticos estrictos en demo
    p[0] = {'type': 'BOOL', 'value': "condicion"}


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
    p[0] = {'type': 'BOOL', 'value': 'logica'}


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
    if p:
        log_resultado(f"Error de sintaxis: token inesperado '{p.value}' en la linea {p.lineno}")
    else:
        log_resultado("Error de sintaxis: se encontró el final inesperado de la entrada.")


# Estructuras de Control adicionales
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


# Clases Abstractas y Clases
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


# Conversiones y métodos
def p_conversion_explicita(p):
    '''valor : valor AS tipodato'''
    p[0] = {'type': 'CAST', 'value': "cast"}


parser = yacc.yacc()


def analizar_codigo(texto):
    global resultados_analisis
    resultados_analisis = []
    errores_lexicos.clear()
    tabla_simbolos['variables'] = {}
    tabla_simbolos['funciones'] = {}

    lexer.input(texto)
    # Tokenizar todo primero para llenar errores léxicos si los hay
    tokens_leidos = []
    while True:
        tok = lexer.token()
        if not tok: break
        tokens_leidos.append(tok)

    # Reiniciar lexer para el parser
    lexer.input(texto)
    parser.parse(texto, lexer=lexer)

    salida = ""
    if errores_lexicos:
        salida += "--- ERRORES LÉXICOS ---\n" + "\n".join(errores_lexicos) + "\n\n"
    if resultados_analisis:
        salida += "--- ANÁLISIS SINTÁCTICO / SEMÁNTICO ---\n" + "\n".join(resultados_analisis)

    if not salida:
        salida = "Análisis completado sin observaciones."

    return salida