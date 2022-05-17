import sys
import ply.yacc as yacc
import tablaSimbolos as tablaSimbolos
import semantica as s
import tablaSimbolos as ts
import cuboSemantico as cuboS
from lexer import tokens

# stacks para crear los cuadruplos
PilaO = []
POper = []
PilaTipos = []
PilaSaltos = []
# contador para temporales
cont = 0
# contador para cuadruplos
contCuad = 1
# saber si se esta dentro de declaracion de clase
dentroClase = False

sem = s.Semantica()
tablaVariables = ts.tabla_simbolos_vars()
tablaLocalVars = ts.tabla_simbolos_vars()
tablaLocalFuncs = ts.tabla_simbolos_funcs()
tablaFunciones = ts.tabla_simbolos_funcs()
tablaClases = ts.tabla_simbolos_clases()
cubo = cuboS.CuboSemantico()

#*********** programa ***********
def p_programa(t):
    'programa : PROGRAM ID SEMICOLON goto_main clase vars funcion main'
    t[0] = "COMPILADO"

def p_goto_main(t):
    'goto_main : e'
    sem.intermediario("goto", None, None, None)
    global contCuad
    contCuad = contCuad + 1
    #tablaFunciones.insertar("program_"+t[2], "programa", None, 0, None, vars)

#************ main *************
def p_main(t):
    'main : MAIN LPAR RPAR main_start bloque'

def p_main_start(t):
    'main_start : e'
    sem.cuadruplos[0].res = contCuad

#*********** clase **************
def p_clase(t):
    '''clase : CLASS inicializar_clase ID clase1 LCBRAC clase2 clase3 RCBRAC  clase
    | e'''
    #if(t[1] != None):
      #if(tablaClases.buscar(t[2]) == None):
        #tablaClases.insert()

def p_inicializar_clase(t):
    '''inicializar_clase : e'''
    global dentroClase
    dentroClase = True
    tablaLocalVars.dict = {}
    tablaLocalFuncs.dict = {}
  
def p_clase1(t):
    '''clase1 : LT INHERITS ID GT
    | e'''

def p_clase2(t):
    '''clase2 : ATTRIBUTES declaracion atributos asign
    | e'''

def p_atributos(t):
    '''atributos : declaracion atributos
    | e'''
  
def p_asign(t):
    '''asign : asignacion asign
    | e'''

def p_clase3(t):
    '''clase3 : METHODS funcion metodos
    | e'''
  

def p_metodos(t):
    '''metodos : funcion metodos
    | e'''
  
#************ vars ************
def p_vars(t):
    '''vars : VAR declaracion declaraciones
    | e'''
    if(t[1] == "var"):
      PilaTipos.pop()

def p_declaraciones(t):
    '''declaraciones : declaracion declaraciones
    | e'''
  
#********* declaracion 
pilaVars = []

def p_declaracion(t):
    'declaracion : declaracion1 COLON declaracion5 SEMICOLON'
  
def p_declaracion1(t):
    'declaracion1 : ID declaracion2 declaracion4'
    if (dentroClase):
      tablaLocalVars.insertar(t[1], None, None)
      pilaVars.append(t[1])
      print("----------------")
      print(tablaLocalVars.dict)
    else:
      tablaVariables.insertar(t[1], None, None)
      pilaVars.append(t[1])

def p_declaracion2(t):
    '''declaracion2 : LSBRAC CTEI RSBRAC declaracion3
    | e'''

def p_declaracion3(t):
    '''declaracion3 : LSBRAC CTEI RSBRAC
    | e'''

def p_declaracion4(t):
    '''declaracion4 : COMMA declaracion1
    | e'''

def p_declaracion5(t):
    '''declaracion5 : tipo
    | ID'''
    if(dentroClase):
      while(len(pilaVars) > 0):
          if(t[1] == None):
            tablaLocalVars.insertar(pilaVars.pop(), PilaTipos[-1], None)
          else:
            tablaLocalVars.insertar(pilaVars.pop(), t[1], None)
    else:
        while(len(pilaVars) > 0):
          if(t[1] == None):
            tablaVariables.insertar(pilaVars.pop(), PilaTipos[-1], None)
          else:
            tablaVariables.insertar(pilaVars.pop(), t[1], None)

#*********** funcion ***********
parametros = []
vars = [] # (var, dirV)
def p_funcion(t):
    '''funcion : funcion1 FUNCTION ID inicio LPAR funcion2 RPAR bloque funcion
    | e'''
    if (t[1] != None):
      if (tablaFunciones.buscar(t[3]) == None):
        global contCuad
        tablaFunciones.insertar(t[3], PilaTipos.pop(), parametros, t[4], None, vars)
        sem.intermediario("gosub", None, None, None)
        contCuad = contCuad + 1
        sem.intermediario("goto", None, None, None)
        PilaSaltos.append(contCuad)
        contCuad = contCuad + 1
      else:
       print("Error de semantica: doble declaracion")
       exit(1)

def p_funcion1(t):
    '''funcion1 : tipo
    | VOID funcion_void'''
    t[0] = t[1]

def p_funcion_void(t):
    'funcion_void : e'
    PilaTipos.append("void")

def p_inicio(t):
    'inicio : e'
    global contCuad
    t[0] = contCuad

def p_funcion2(t):
    '''funcion2 : ID COLON tipo funcion3
    | e'''
    parametros.insert(0,PilaTipos.pop())
    vars.insert(0,(t[1], None))
    tablaLocalVars.insertar(t[1], t[3], None)

def p_funcion3(t):
    '''funcion3 : COMMA ID COLON tipo funcion3
    | e'''
    if(t[1] != None):
        parametros.insert(0,PilaTipos.pop())
        vars.insert(0,(t[2], None))
        tablaLocalVars.insertar(t[1], t[4], None)
        #validacion de no repetir
  
#*********** tipo ***********
def p_tipo(t):
    '''tipo : INT
    | FLOAT 
    | STRING
    | BOOL'''
    PilaTipos.append(t[1])
    t[0] = t[1]

#*********** bloque ***********
def p_bloque(t):
    'bloque : LCBRAC estatutos RCBRAC'

def p_estatutos(t):
    '''estatutos : estatuto estatutos
    | e '''

#*********** estatuto ***********
def p_estatuto(t):
    '''estatuto : asignacion
    | condicion
    | llamada
    | leer
    | escribir
    | ciclo_w
    | ciclo_f
    | regresar'''

#*********** asignacion ***********
def p_asignacion(t):
    'asignacion : variable EQ expresion SEMICOLON'
    expresion = PilaO.pop()
    variable = PilaO.pop()
    tipoExpresion = cubo.getTipo(PilaTipos.pop())
    tipoVariable = cubo.getTipo(PilaTipos.pop())
    rechazar = cubo.cubo[tipoVariable, tipoExpresion, 10]
    if(rechazar != 11):
        sem.intermediario('=', expresion, None , variable)
        global contCuad
        contCuad = contCuad + 1
        # update tablaVariables
    else:
        print("Error semantico: error de asignacion type-mismatch: ", variable)    

#************ variable ************
def p_variable(t):
    'variable : ID variable1 variable2'
    existe = tablaVariables.buscar(t[1])
    existeLocal = tablaLocalVars.buscar(t[1])
    if(existe != None):
        PilaO.append(t[1])
        PilaTipos.append(existe[0])
    elif(existeLocal):
        PilaO.append(t[1])
        PilaTipos.append(existeLocal[0])
    else:
        print("Error de semantica: variable no declarada: ", t[1])
        #exit(1)

def p_variable1(t):
    '''variable1 : DOT ID
    | e'''

def p_variable2(t):
    '''variable2 : LSBRAC expresion RSBRAC variable3
    | e'''

def p_variable3(t):
    '''variable3 : LSBRAC expresion RSBRAC
    | e'''

#*********** condicion ***********
def p_condicion(t):
    'condicion : IF LPAR expresion RPAR gotoF bloque condicion1 fill'

def p_gotoF(t):
    'gotoF : e'
    global contCuad
    exp_tipo = PilaTipos.pop()
    if(exp_tipo == "bool" ):
      PilaSaltos.append(contCuad)
      sem.intermediario('gotoF', PilaO.pop(), None, None)
      contCuad = contCuad + 1
    else:
      print("Error semantico: type-mismatch")

def p_fill(t):
    'fill : e'
    global contCuad
    ret = PilaSaltos.pop() - 1
    sem.cuadruplos[ret].res = contCuad

def p_condicion1(t):
    '''condicion1 : ELSE goto bloque
    | e'''

def p_goto(t):
    '''goto : e'''
    global contCuad
    sem.intermediario('goto', None, None, None)
    false = PilaSaltos.pop() - 1
    PilaSaltos.append(contCuad)
    contCuad = contCuad + 1
    sem.cuadruplos[false].res = contCuad

#*********** llamada ************
def p_llamada(t):
    'llamada : ID llamada1 LPAR llamada2 RPAR SEMICOLON'
    obj = tablaVariables.buscar(t[1])
    func = tablaFunciones.buscar(t[1])
    if(obj != None):
        print("obj");
    elif(func != None):
        global contCuad
        sem.intermediario("era", None, None, func[3])
        contCuad = contCuad + 1
        #pasar parametros "param", arg1, None, num_param
        sem.intermediario("goto", None, None, func[2])
        contCuad = contCuad + 1
        fillFunc = PilaSaltos.pop() - 1
        sem.cuadruplos[fillFunc].res = contCuad
    else:
        print("Function not declared")

def p_llamada1(t):
    '''llamada1 : DOT ID
    | e'''
    if(t[1] == '.'):
        classFunc = tablaLocalFuncs.buscar(t[2])
        if(classFunc != None):
            global contCuad
            sem.intermediario("era", None, None, classFunc[3])
            contCuad = contCuad + 1
            #pasar parametros "param", arg1, None, num_param
            sem.intermediario("goto", None, None, classFunc[2])
            contCuad = contCuad + 1
            fillFunc = PilaSaltos.pop() - 1
            sem.cuadruplos[fillFunc].res = contCuad
        else:
            print("Function not declared")

def p_llamada2(t):
    '''llamada2 : expresion llamada3
    | e'''

def p_llamada3(t):
    '''llamada3 : COMMA expresion llamada3
    | e'''

#************ leer *************
def p_leer(t):
    'leer : READ LPAR variable add_read generar_cuadr RPAR SEMICOLON'

def p_add_read(t):
    '''add_read : e'''
    POper.append("read")

#*********** escribir ***********
def p_escribir(t):
    'escribir : WRITE LPAR escribir1 RPAR SEMICOLON'

def p_escribir1(t):
    '''escribir1 : texto add_print generar_cuadr escribir2
    | expresion add_print generar_cuadr escribir2'''

def p_add_print(t):
    'add_print : e'
    POper.append("print")
  
def p_escribir2(t):
    '''escribir2 : COMMA escribir1
    | e '''

def p_texto(t):
  '''texto : CTESTR '''
  PilaO.append(t[1])
  PilaTipos.append("string")

#*********** ciclo_w ************
def p_ciclo_w(t):
    'ciclo_w : WHILE push_while LPAR expresion RPAR  gotoF DO bloque return_while'

def p_push_while(t):
    'push_while : e'
    PilaSaltos.append(contCuad)

def p_return_while(t):
    'return_while : e'
    global contCuad
    salida = PilaSaltos.pop() - 1
    regreso = PilaSaltos.pop()
    sem.intermediario("goto", None, None, regreso)
    contCuad = contCuad + 1
    sem.cuadruplos[salida].res = (contCuad + 1)

#*********** ciclo_f ************
def p_ciclo_f(t):
    'ciclo_f : FROM LPAR variable EQ expresion asign_var TO expresion asign_exp migaja push_lt pop_for gotoF RPAR DO bloque update_fill_go'

# guardar valor de exp en variable
def p_asign_var(t):
    'asign_var : e'
    expresion = PilaO.pop()
    variable = PilaO.pop()
    tipoExpresion = cubo.getTipo(PilaTipos.pop())
    tipoVariable = cubo.getTipo(PilaTipos.pop())
    rechazar = cubo.cubo[tipoVariable, tipoExpresion, 10]
    if(rechazar != 11):
        sem.intermediario('=', expresion, None , variable)
        global contCuad
        contCuad = contCuad + 1
        PilaO.append(variable)
        PilaTipos.append(cubo.getNumeroTipo(tipoVariable))
        # update tablaVariables
    else:
        print("Error semantico: error de asignacion type-mismatch: ", variable)  
# guardar valor de expresion en var2
def p_asign_exp(t):
    'asign_exp : e'
    expresion = PilaO.pop()
    global contCuad
    variable = "for_" + str(contCuad)
    tipoExpresion = cubo.getTipo(PilaTipos.pop())
    tipoVariable = tipoExpresion
    PilaO.append(variable)
    PilaTipos.append(cubo.getNumeroTipo(tipoVariable))
    tablaVariables.insertar(variable, tipoExpresion, None)
    rechazar = cubo.cubo[tipoVariable, tipoExpresion, 10]
    if(rechazar != 11):
        sem.intermediario('=', expresion, None , variable)
        contCuad = contCuad + 1
        # update tablaVariables
    else:
        print("Error semantico: error de asignacion type-mismatch: ", variable)  
# comparar variable y var2 <
def p_pop_for(t):
    'pop_for : e'
    right_op = PilaO.pop()
    right_type = cubo.getTipo(PilaTipos.pop())
    left_op = PilaO.pop()
    left_type = cubo.getTipo(PilaTipos.pop())
    operador = POper.pop()
    num_oper = cubo.getOperando(operador)
    rechazar = cubo.cubo[left_type, right_type, num_oper]
    if(rechazar != 11):
        global cont, contCuad
        sem.intermediario(str(operador), str(left_op), str(right_op), "t"+str(cont))
        PilaO.append(left_op)
        PilaTipos.append(cubo.getNumeroTipo(left_type))
        PilaO.append(right_op)
        PilaTipos.append(cubo.getNumeroTipo(right_type))
        PilaO.append(left_op)
        PilaTipos.append(cubo.getNumeroTipo(left_type))
        contCuad = contCuad + 1
        PilaO.append("t"+str(cont))
        tipo = cubo.getNumeroTipo(rechazar)
        PilaTipos.append(tipo)
        cont = cont + 1
    else:
        print("Error semantico en expresiones: type mismatch")
        exit(1)
# migaja y poner gotoF fuera del ciclo
def p_migaja(t):
    'migaja : e'
    global contCuad
    PilaSaltos.append(contCuad)
# final bloque variable+1, fill gotoF y goto
def p_update_fill_go(t):
    'update_fill_go : push_plus push1 pop_operfor asign_var'
    global contCuad
    fill = PilaSaltos.pop() - 1
    ret = PilaSaltos.pop()
    sem.intermediario("goto", None, None, ret)
    contCuad = contCuad + 1
    sem.cuadruplos[fill].res = contCuad

def p_push1(t):
    'push1 : e'
    PilaO.append("1")
    PilaTipos.append("int")
    
def p_pop_operfor(t):
    'pop_operfor : e'
    right_op = PilaO.pop()
    right_type = cubo.getTipo(PilaTipos.pop())
    left_op = PilaO.pop()
    left_type = cubo.getTipo(PilaTipos.pop())
    operador = POper.pop()
    num_oper = cubo.getOperando(operador)
    rechazar = cubo.cubo[left_type, right_type, num_oper]
    if(rechazar != 11):
        global cont, contCuad
        PilaO.append(left_op)
        PilaTipos.append(cubo.getNumeroTipo(left_type))
        sem.intermediario(str(operador), str(left_op), str(right_op), "t"+str(cont))
        contCuad = contCuad + 1
        PilaO.append("t"+str(cont))
        tipo = cubo.getNumeroTipo(rechazar)
        PilaTipos.append(tipo)
        cont = cont + 1
    else:
        print("Error semantico en expresiones: type mismatch")
        exit(1)
    
#*********** regresar ***********
def p_regresar(t):
    'regresar : RETURN expresion SEMICOLON'
    #GOSUB
  
#*********** expresion ***********
def p_expresion(t):
    'expresion : a_exp exp1'
    t[0]=t[1]

def p_exp1(t):
    '''exp1 : OR push_or a_exp pop_operador exp1
    | e '''
    if t[1] != '||': t[0] = t[1]

def p_push_or(t):
    'push_or : e'
    POper.append('||')

def p_pop_operador(t):
    'pop_operador : e'
    right_op = PilaO.pop()
    right_type = cubo.getTipo(PilaTipos.pop())
    left_op = PilaO.pop()
    left_type = cubo.getTipo(PilaTipos.pop())
    operador = POper.pop()
    num_oper = cubo.getOperando(operador)
    rechazar = cubo.cubo[left_type, right_type, num_oper]
    if(rechazar != 11):
        global cont, contCuad
        sem.intermediario(str(operador), str(left_op), str(right_op), "t"+str(cont))
        contCuad = contCuad + 1
        PilaO.append("t"+str(cont))
        tipo = cubo.getNumeroTipo(rechazar)
        PilaTipos.append(tipo)
        cont = cont + 1
    else:
        print("Error semantico en expresiones: type mismatch")
        exit(1)
  
def p_a_exp(t):
    'a_exp : b_exp exp2'
    t[0]=t[1]

def p_exp2(t):
    '''exp2 : AND push_and b_exp pop_operador exp2
    | e '''
    if t[1] != '&&': t[0] = t[1]

def p_push_and(t):
    'push_and : e'
    POper.append('&&')

def p_b_exp(t):
    'b_exp : c_exp exp3'
    t[0]=t[1]

def p_exp3(t):
    '''exp3 : LT push_lt c_exp pop_operador exp3
    | GT push_gt c_exp pop_operador exp3
    | COMP push_comp c_exp pop_operador exp3
    | NOTEQ push_noteq c_exp pop_operador exp3
    | e '''
    if (t[1] != '<' and t[1] != '>' and t[1] != '==' and t[1] != '!='): t[0] = t[1]

def p_push_lt(t):
    'push_lt : e'
    POper.append('<')

def p_push_gt(t):
    'push_gt : e'
    POper.append('>')

def p_push_comp(t):
    'push_comp : e'
    POper.append('==')

def p_push_noteq(t):
    'push_noteq : e'
    POper.append('!=')

def p_c_exp(t):
    'c_exp : d_exp exp4'
    t[0]=t[1]

def p_exp4(t):
    '''exp4 : PLUS push_plus d_exp pop_operador exp4
    | MINUS push_minus d_exp pop_operador exp4
    | e '''
    if (t[1] != '+' and t[1] != '-'): t[0] = t[1]

def p_push_plus(t):
    'push_plus : e'
    POper.append('+')

def p_push_minus(t):
    'push_minus : e'
    POper.append('-')

def p_d_exp(t):
    'd_exp : e_exp exp5'
    t[0]=t[1]

def p_exp5(t):
    '''exp5 : MULT push_mult e_exp pop_operador exp5
    | DIV push_div e_exp pop_operador exp5
    | e '''
    if (t[1] != '*' and t[1] != '/'): t[0] = t[1]

def p_push_mult(t):
    'push_mult : e'
    POper.append('*')

def p_push_div(t):
    'push_div : e'
    POper.append('/')

def p_e_exp(t):
    '''e_exp : LPAR expresion RPAR
    | var_cte
    | variable
    | llamada'''
    if (t[1] == '('): t[0] = t[2]
    else: t[0] = t[1]

#*********** var_cte ***********
def p_var_cte(t):
    '''var_cte : CTEI ctei
    | CTEF ctef
    | CTESTR ctestr
    | CTEB cteb'''
    PilaO.append(t[1])
    t[0]=t[1]

def p_ctei(t):
    'ctei : e'
    PilaTipos.append("int")

def p_ctef(t):
    'ctef : e'
    PilaTipos.append("float")

def p_ctestr(t):
    'ctestr : e'
    PilaTipos.append("string")

def p_cteb(t):
    'cteb : e'
    PilaTipos.append("bool")

def p_generar_cuadr(t):
    'generar_cuadr : e'
    poper = POper.pop()
    global contCuad
    if(poper == "print"):
        arg1 = str(PilaO.pop())
        PilaTipos.pop()
        sem.intermediario(poper, None, None , arg1)
        contCuad = contCuad + 1
    if(poper == "read"):
        arg1 = str(PilaO.pop())
        PilaTipos.pop()
        sem.intermediario(poper, None, None, arg1)
        contCuad = contCuad + 1

#********* error & pass **********
def p_error(t):
    print("Error de sintaxis en la linea ", t.lineno, " cerca del caracter \"", t.value, "\"")

def p_e(t):
    'e : '
    pass

yacc.yacc()

# leer input del archivo
if __name__ == '__main__':
    if len(sys.argv) > 1:
        file = sys.argv[1]
        try:
            f = open(file, 'r')
            data = f.read()
            f.close()
            if yacc.parse(data) == "COMPILADO":
                print("Validacion completa")
        except ValueError:
            print(ValueError)
    sem.imprimirCuadruplos()