import sys
import ply.yacc as yacc
import tablaSimbolos as tablaSimbolos
import semantica as s
import tablaSimbolos as ts
import cuboSemantico as cuboS
from lexer import tokens
import dirVir as dir

# stacks para crear los cuadruplos
PilaO = []
POper = []
PilaTipos = []
PilaSaltos = []
# contador para temporales
cont = 0
# contador para cuadruplos
contCuad = 1
# saber si se esta dentro de declaracion de clase o funcion
dentroClase = False
dentroFuncion = False

sem = s.Semantica()
# para saber que estas declarando vars y funcs de una clase
tablaLocalVars = ts.tabla_simbolos_vars()
tablaLocalFuncs = ts.tabla_simbolos_funcs()
tablaLocalConsts = ts.tabla_memoria_vars()
tablaLocalTemps = ts.tabla_memoria_vars()
tablaVarsClase = ts.tabla_simbolos_vars()
tablaObjClase = ts.tabla_memoria_objetos()

# tablas globales
tablaVariables = ts.tabla_simbolos_vars()
tablaFunciones = ts.tabla_simbolos_funcs()
tablaClases = ts.tabla_simbolos_clases()
tablaTemporales = ts.tabla_memoria_vars()
tablaConstantes = ts.tabla_memoria_vars()
tablaTempPointers = ts.tabla_memoria_vars()
tablaObjetos = ts.tabla_memoria_objetos()
cubo = cuboS.CuboSemantico()
contGlobal = dir.varGlobal()
contLocal = dir.varLocal()
contTemps = dir.varTemps()
contTPointers = dir.varTempsPointer()
contConst = dir.varConst()
contClase = dir.varClases()

# para arreglos
arreglo = ts.arreglos()


#*********** programa ***********
def p_programa(t):
    'programa : PROGRAM ID SEMICOLON goto_main clase vars funcion main'
    t[0] = "COMPILADO"
    sem.intermediario("endProgram", None, None, None)
    global contCuad
    contCuad = contCuad + 1

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
idClase = None
padreClase = None

def p_clase(t):
    '''clase : CLASS inicializar_clase clase1 LCBRAC clase2 clase3 RCBRAC  reiniciar_clase clase
    | e'''
    if(t[1] == None):
      global dentroClase
      dentroClase = False

def p_inicializar_clase(t):
    '''inicializar_clase : ID'''
    global dentroClase, contClase
    dentroClase = True
    tablaVarsClase.dict = {}
    tablaObjClase.dict = {}
    tablaLocalFuncs.dict = {}
    contClase.contInt = 0
    contClase.contFloat = 0
    contClase.contString = 0
    contClase.contBool = 0
    global idClase, padreClase
    idClase = t[1]
    padreClase = None
    t[0] = t[1]

def p_reiniciar_clase(t):
    '''reiniciar_clase : e'''
    global padreClase, idClase
    dentroClase = False
    existe = tablaClases.buscar(idClase)
    if(existe != None):
      print("Error: doble declaracion de clase ", idClase)
      exit(1)
    else:
      # insertar contador donde empieza la clase
      tablaClases.insertar(idClase, tablaVarsClase.dict, tablaLocalFuncs.dict, padreClase, contClase.contInt, contClase.contFloat, contClase.contString, contClase.contBool, None, tablaObjClase.dict)
  
def p_clase1(t):
    '''clase1 : LT INHERITS ID GT
    | e'''
    global padreClase, idClase
    if(t[1] != None):
      padreClase = t[3]
      existe = tablaClases.buscar(padreClase)
      if(existe != None):
        # buscar que el padre no tenga padre
        if(existe[2] != None):
          print("Error en herencia de clases: las clases solo pueden tener un padre ", idClase)
          exit(1)
        else:
          # agregar tabla de funciones y variables al hijo
          tablaVarsPadre = existe[0]
          tablaFuncsPadre = existe[1]
          tablaObjPadre = existe[8]
          contClase.contInt = existe[3]
          contClase.contFloat = existe[4]
          contClase.contString = existe[5]
          contClase.contBool = existe[6]
          for i in tablaVarsPadre:
            valores = tablaVarsPadre.get(i)
            dict = {i : valores}
            tablaVarsClase.dict.update(dict)
          for i in tablaFuncsPadre:
            valores = tablaFuncsPadre.get(i)
            dict = {i : valores}
            tablaLocalFuncs.dict.update(dict)
          for i in tablaObjPadre:
            valores = tablaObjPadre.get(i)
            ditct = {i : valores}
            tablaObjClase.dict.update(dict)
            contClase.contObj = contClase.contObj + 1
            
      else:
        print("Error en herencia de clases: el padre no existe ", idClase)
        exit(1)

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

def p_declaraciones(t):
    '''declaraciones : declaracion declaraciones
    | e'''
  
#********* declaracion *********
pilaVars = []
clase = False

def p_declaracion(t):
    'declaracion : declaracion1 COLON declaracion5 SEMICOLON'
    global clase
    if(clase == False):
      PilaTipos.pop()
    clase = False
  
def p_declaracion1(t):
    'declaracion1 : inserta_declaracion declaracion2 declaracion4'
    
def p_inserta_declaracion(t):
    'inserta_declaracion : ID'
    if (dentroClase):
      existe = tablaVarsClase.insertar(t[1], None, None, None, None)
      existe2 = tablaObjClase.buscar(t[1])
      if(existe and existe2 == None):
        pilaVars.append(t[1])
      else:
        print("Variable ya declarada: ", t[1])
        exit(1)
    else:
      existe = tablaVariables.insertar(t[1], None, None, None, None)
      existe2 = tablaObjetos.buscar(t[1])
      if(existe and existe2 == None):
        pilaVars.append(t[1])
      else:
        print("Variable ya declarada: ", t[1])
        exit(1)

def p_declaracion2(t):
    '''declaracion2 : LSBRAC assign_limit RSBRAC declaracion3
    | e'''
    if (t[1] == None):
        global size
        size = 1

def p_assign_limit(t):
    'assign_limit : CTEI'
    arreglo.limSupD1 = t[1] - 1
    
def p_declaracion3(t):
    '''declaracion3 : LSBRAC CTEI RSBRAC
    | e'''
    if (t[1] != None):
        arreglo.limSupD2 = t[2] - 1
        arreglo.m1 = t[2]
    nombre = pilaVars[-1]
    tablaVariables.actualizar(nombre, None, None, None, ts.arreglos())
    tablaVariables.buscar(nombre)[3].set(arreglo)
    arreglo.__init__()

def p_declaracion4(t):
    '''declaracion4 : COMMA declaracion1
    | e'''

def p_declaracion5(t):
    '''declaracion5 : tipo
    | ID'''
    if(dentroClase):
      global contClase, clase
      while(len(pilaVars) > 0):
          if(t[1] == None):
            tablaVarsClase.actualizar(pilaVars.pop(), PilaTipos[-1], None)
          else:
            # variables globales que no son clases
            if(t[1] == 'int' and contClase.contInt < contClase.limSInt):
              if(contClase.contInt + contClase.limIInt > contClase.limSInt):
                print("Exceso de memoria para variables enteras en clases")
                exit(1)
              tablaVarsClase.actualizar(pilaVars.pop(), t[1], None, contClase.limIInt + contClase.contInt, None)
              contClase.contInt = contClase.contInt + 1
              
            elif(t[1] == 'float' and contClase.contFloat < contClase.limSFloat):
              if(contClase.contFloat + contClase.limIFloat > contClase.limSFloat):
                print("Exceso de memoria para variables flotantes en clases")
                exit(1)
              tablaVarsClase.actualizar(pilaVars.pop(), t[1], None, contClase.limIFloat + contClase.contFloat, None)
              contClase.contFloat = contClase.contFloat + 1
              
            elif(t[1] == 'string' and contClase.contString < contClase.limSString):
              if(contClase.contString + contClase.limIString > contClase.limString):
                print("Exceso de memoria para variables string en clases")
                exit(1)
              tablaVarsClase.actualizar(pilaVars.pop(), t[1], None, contClase.limIString + contClase.contString, None)
              contClase.contString = contClase.contString + 1
            elif(t[1] == 'bool' and contClase.contBool < contClase.limSBool):
              if(contClase.contBool + contClase.limIBool > contClase.limSBool):
                print("Exceso de memoria para variables booleanas en clases")
                exit(1)
              tablaVarsClase.actualizar(pilaVars.pop(), t[1], None, contClase.limIBool + contClase.contBool, None)
              contClase.contBool = contClase.contBool + 1
            else:
            #es un objeto, checar que la clase exista
              existe = tablaClases.buscar(t[1])
              if(existe != None):
                if(contClase.contObj + contClase.limIObj > contClase.limSObj):
                  print("Exceso de memoria para variables de tipo objeto en clases")
                  exit(1)
                else:
                  nombre = pilaVars.pop()
                  existe2 = tablaObjClase.buscar(nombre)
                  if(existe2 != None):
                    print("Variable ya declarada: ", nombre)
                    exit(1)
                  else:
                    nombresFuncs = []
                    for i in existe[1]:
                      nombresFuncs.append(i)
                    tablaObjClase.insertar(nombre, t[1], existe[0], nombresFuncs, contClase.limIObj + contClase.contObj)
                    contClase.contObj = contClase.contObj + 1
                    clase = True
              else:
                print("Error en declaracion de variables - tipo de dato inexistente")
                exit(1)
    else:
        global contGlobal
        while(len(pilaVars) > 0):
          # variables globales que son clases
          if(t[1] == None):
            nombre = pilaVars.pop()
            valores = tablaVariables.buscar(nombre)
            tablaVariables.actualizar(nombre, PilaTipos[-1], None, None, valores[3])
            print(tablaVariables)
          else:
            # variables globales que no son clases
            if(t[1] == 'int' and contGlobal.contInt < contGlobal.limSInt):
              if(contGlobal.contInt + contGlobal.limIInt > contGlobal.limSInt):
                print("Exceso de memoria para variables enteras globales")
                exit(1)
              nombre = pilaVars.pop()
              valores = tablaVariables.buscar(nombre)
              tablaVariables.actualizar(nombre, t[1], None, contGlobal.limIInt + contGlobal.contInt, valores[3])
              if(valores[3] != None):
                contGlobal.contInt = contGlobal.contInt + (valores[3].limSupD1 + 1) * valores[3].m1
              else:
                contGlobal.contInt = contGlobal.contInt + 1
            elif(t[1] == 'float' and contGlobal.contFloat < contGlobal.limSFloat):
              if(contGlobal.contFloat + contGlobal.limIFloat > contGlobal.limSFloat):
                print("Exceso de memoria para variables flotantes globales")
                exit(1)
              nombre = pilaVars.pop()
              valores = tablaVariables.buscar(nombre)
              tablaVariables.actualizar(nombre, t[1], None, contGlobal.limIFloat + contGlobal.contFloat, valores[3])
              if(valores[3] != None):
                contGlobal.contFloat = contGlobal.contFloat + (valores[3].limSupD1 + 1) * valores[3].m1
              else:
                contGlobal.contFloat = contGlobal.contFloat + 1
            elif(t[1] == 'string' and contGlobal.contString < contGlobal.limSString):
              if(contGlobal.contString + contGlobal.limIString > contGlobal.limSString):
                print("Exceso de memoria para variables string globales")
                exit(1)
              nombre = pilaVars.pop()
              valores = tablaVariables.buscar(nombre)
              tablaVariables.actualizar(nombre, t[1], None, contGlobal.limIString + contGlobal.contString, valores[3])
              if(valores[3] != None):
                contGlobal.contString = contGlobal.contString + (valores[3].limSupD1 + 1) * valores[3].m1
              else:
                contGlobal.contString = contGlobal.contString + 1
                
            elif(t[1] == 'bool' and contGlobal.contBool < contGlobal.limSBool):
              if(contGlobal.contBool + contGlobal.limIBool > contGlobal.limSBool):
                print("Exceso de memoria para variables booleanas globales")
                exit(1)
              nombre = pilaVars.pop()
              valores = tablaVariables.buscar(nombre)
              tablaVariables.actualizar(nombre, t[1], None, contGlobal.limIBool + contGlobal.contBool, valores[3])
              if(valores[3] != None):
                contGlobal.contBool = contGlobal.contBool + (valores[3].limSupD1 + 1) * valores[3].m1
              else:
                contGlobal.contBool = contGlobal.contBool + 1
            else: 
              # variables de tipo objeto
              existe = tablaClases.buscar(t[1])
              if(existe != None):
                if(contGlobal.contObj + contGlobal.limIObj > contGlobal.limSObj):
                  print("Exceso de memoria para variables de tipo objeto globales")
                  exit(1)
                else:
                  # checar que el objeto no exista en la tabla 
                  nombre = pilaVars.pop()
                  
                  existe2 = tablaObjetos.buscar(nombre)
                  nombresFuncs = []
                  for i in existe[1]:
                    nombresFuncs.append(i)
                  tablaObjetos.insertar(nombre, t[1], existe[0], nombresFuncs, contGlobal.limIObj + contGlobal.contObj)
                  contGlobal.contObj = contGlobal.contObj + 1
                  clase = True
              else:
                print("Error en declaracion de variables - tipo de dato inexistente")
                exit(1)

#*********** funcion ***********
parametros = []
vars = [] # (var, dirV)
idFunc = ""
def p_funcion(t):
    '''funcion : funcion1 FUNCTION guardar_id LPAR funcion2 RPAR bloque_return reiniciar_func funcion
    | e'''

def  p_guardar_id(t):
    'guardar_id : ID'
    global idFunc, dentroFuncion
    idFunc = t[1]
    dentroFuncion = True

def p_reiniciar_func(t):
    'reiniciar_func : e'
    global idFunc, parametros, dentroFuncion, contLocal, contCuad
    tipo = PilaTipos.pop()
    if(dentroClase):
      if (tipo != None):
          if (tablaLocalFuncs.buscar(idFunc) == None):
              if(tipo != 'void'):
                  if(tipo == 'int'):
                    if(contClase.contInt + contClase.limIInt < contClase.limSInt):
                      if(tipo == PilaTipos.pop()):
                        tablaVarsClase.insertar(idFunc, tipo, PilaO.pop(), contClase.contInt + contClase.limIInt, None)
                        contClase.contInt = contClase.contInt + 1
                    else:
                      print("Memoria excedida por numero de variables enteras para la clase")
                      exit(1)
                      
                  if(tipo == 'float'):
                    if(contClase.contFloat + contClase.limIFloat < contClase.limSFloat):
                      if(tipo == PilaTipos.pop()):
                        tablaVarsClase.insertar(idFunc, tipo, PilaO.pop(), contClase.contFloat + contClase.limIFloat, None)
                        contClase.contFloat = contClase.contFloat + 1
                    else:
                      print("Memoria excedida por numero de variables flotantes para la clase")
                      exit(1)
                  if(tipo == 'string'):
                    if(contClase.contString + contClase.limIString < contClase.limSString):
                      if(tipo == PilaTipos.pop()):
                        tablaVarsClase.insertar(idFunc, tipo, PilaO.pop(), contClase.contString + contClase.limIString, None)
                        contClase.contString = contClase.contString + 1
                    else:
                      print("Memoria excedida por numero de variables string para la clase")
                      exit(1)
                      
                  if(tipo == 'bool'):
                    if(contClase.contBool + contClase.limIBool < contClase.limSBool):
                      if(tipo == PilaTipos.pop()):
                        tablaVarsClase.insertar(idFunc, tipo, PilaO.pop(), contClase.contBool + contClase.limIBool, None)
                        contClase.contBool = contClase.contBool + 1
                    else:
                      print("Memoria excedida por numero de variables booleanas para la clase")
                      exit(1)
              
              tablaLocalFuncs.insertar(idFunc, tipo, parametros, PilaSaltos.pop(), tablaLocalVars.dict, contLocal.contIntVar, contLocal.contFloatVar, contLocal.contStringVar, contLocal.contBoolVar, contLocal.contIntTemp, contLocal.contFloatTemp, contLocal.contStringTemp, contLocal.contBoolTemp, tablaLocalConsts.dict)
              sem.intermediario("endfunc", None, None, None)
              contCuad = contCuad + 1
          else:
            print("Error de semantica: doble declaracion de funciones")
            exit(1)
    else: # funcion fuera de una clase
      if (tipo != None):
          if (tablaFunciones.buscar(idFunc) == None):
              if(tipo != 'void'):
                if(tipo == 'int'):
                  if(contGlobal.contInt + contGlobal.limIInt < contGlobal.limSInt):
                    if(tipo == PilaTipos.pop()): # checa que regrese un tipo correcto
                      tablaVariables.insertar(idFunc, tipo, PilaO.pop(), contGlobal.contInt + contGlobal.limIInt, None)
                      contGlobal.contInt = contGlobal.contInt + 1
                  else:
                    print("Memoria excedida por numero de variables enteras")
                    exit(1)
                if(tipo == 'float'):
                  if(contGlobal.contFloat + contGlobal.limIFloat < contGlobal.limSFloat):
                    if(tipo == PilaTipos.pop()):
                      tablaVariables.insertar(idFunc, tipo, PilaO.pop(), contGlobal.contFloat + contGlobal.limIFloat, None)
                      contGlobal.contFloat = contGlobal.contFloat + 1
                  else:
                    print("Memoria excedida por numero de variables enteras")
                    exit(1)
                    
                if(tipo == 'string'):
                  if(contGlobal.contString + contGlobal.limIString < contGlobal.limSString):
                    if(tipo == PilaTipos.pop()):
                      tablaVariables.insertar(idFunc, tipo, PilaO.pop(), contGlobal.contString + contGlobal.limIString, None)
                      contGlobal.contString = contGlobal.contString + 1
                  else:
                    print("Memoria excedida por numero de variables enteras")
                    exit(1)

                if(tipo == 'bool'):
                  if(contGlobal.contBool + contGlobal.limIBool < contGlobal.limSBool):
                    if(tipo == PilaTipos.pop()):
                      tablaVariables.insertar(idFunc, tipo, PilaO.pop(), contGlobal.contBool + contGlobal.limIBool, None)
                      contGlobal.contBool = contGlobal.contBool + 1
                  else:
                    print("Memoria excedida por numero de variables enteras")
                    exit(1)
              tablaFunciones.insertar(idFunc, tipo, parametros, PilaSaltos.pop(), tablaLocalVars.dict, contLocal.contIntVar, contLocal.contFloatVar, contLocal.contStringVar, contLocal.contBoolVar, contLocal.contIntTemp, contLocal.contFloatTemp, contLocal.contStringTemp, contLocal.contBoolTemp, tablaLocalConsts.dict)
              sem.intermediario("endfunc", None, None, None)
              contCuad = contCuad + 1
          else:
             print("Error de semantica: doble declaracion")
             exit(1)
    tablaLocalVars.inversa()
    tablaLocalVars.dict = {}
    parametros = []
    dentroFuncion = False
    contLocal.contIntTemp = 0
    contLocal.contFloatTemp = 0
    contLocal.contStringTemp = 0
    contLocal.contBoolTemp = 0
    tablaLocalTemps.dict = {}
    tablaLocalConsts.dict = {}
    contLocal.contIntConst = 0
    contLocal.contFloatConst = 0
    contLocal.contStringConst = 0
    contLocal.contBoolConst = 0
    contLocal.contIntVar = 0
    contLocal.contFloatVar = 0
    contLocal.contStringVar = 0
    contLocal.contBoolVar = 0

def p_funcion1(t):
    '''funcion1 : tipo
    | VOID funcion_void'''
    global contCuad
    PilaSaltos.append(contCuad)
    t[0] = t[1]

def p_funcion_void(t):
    'funcion_void : e'
    PilaTipos.append("void")

def p_funcion2(t):
    '''funcion2 : ID COLON tipo funcion3
    | e'''
    if(t[1] != None):
        tipo_param = PilaTipos.pop()
        parametros.insert(0,tipo_param)
        vars.insert(0,(t[1], None)) #checar: vars nos sirve?
        existe = tablaVariables.buscar(t[1])
        if(existe != None):
          print("Error - variable global ya declarada: ", t[1])
          exit(1)
        elif(dentroClase):
          existe = tablaVarsClase.buscar(t[1])
          if(existe != None):
            print("Error - variable de clase ya declarada: ", t[1])
            exit(1)

        if(t[3] == 'int'):
          if(contLocal.contIntVar + contLocal.limIIntVar <= contLocal.limSIntVar):
            existe = tablaLocalVars.insertar(t[1], t[3], None, contLocal.contIntVar + contLocal.limIIntVar, None)
            contLocal.contIntVar = contLocal.contIntVar + 1
          else:
              print("Error: exceso de memoria en variables locales enteras")
              exit(1)
        if(t[3] == 'float'):
          if(contLocal.contFloatVar +contLocal.limIFloatVar <= contLocal.limSFloatVar):
            existe = tablaLocalVars.insertar(t[1], t[3], None, contLocal.contFloatVar + contLocal.limIFloatVar, None)
            contLocal.contFloatVar = contLocal.contFloatVar + 1
          else:
            print("Error: exceso de memoria en variables locales flotantes")
            exit(1)
        if(t[3] == 'string'):
          if(contLocal.contStringVar +contLocal.limIStringVar <= contLocal.limSStringVar):
            existe = tablaLocalVars.insertar(t[1], t[3], None, contLocal.contStringVar + contLocal.limIStringVar, None)
            contLocal.contStringVar = contLocal.contStringVar + 1
          else:
            print("Error: exceso de memoria en variables locales string")
            exit(1)
        if(t[3] == 'bool'):
          if(contLocal.contBoolVar +contLocal.limIBoolVar <= contLocal.limSBoolVar):
            existe = tablaLocalVars.insertar(t[1], t[3], None, contLocal.contBoolVar + contLocal.limIBoolVar, None)
            contLocal.contBoolVar = contLocal.contBoolVar + 1
          else:
            print("Error: exceso de memoria en variables locales bool")
            exit(1)
        if(existe == False):
          print("Error - variable ya declarada en parametros: ", t[1])
          exit(1)

def p_funcion3(t):
    '''funcion3 : COMMA ID COLON tipo funcion3
    | e'''
    if(t[1] != None):
        tipo_param = PilaTipos.pop()
        parametros.insert(0,tipo_param)
        vars.insert(0,(t[2], None))
        existe = tablaVariables.buscar(t[2])
        if(existe != None):
          print("Error - variable global ya declarada: ", t[2])
          exit(1)
        elif(dentroClase):
          existe = tablaVarsClase.buscar(t[2])
          if(existe != None):
            print("Error - variable de clase ya declarada: ", t[2])
            exit(1)

        if(t[4] == 'int'):
          if(contLocal.contIntVar + contLocal.limIIntVar <= contLocal.limSIntVar):
            existe = tablaLocalVars.insertar(t[2], t[4], None, contLocal.contIntVar + contLocal.limIIntVar, None)
            contLocal.contIntVar = contLocal.contIntVar + 1
          else:
            print("Error: exceso de memoria en variables locales enteras")
            exit(1)
        if(t[4] == 'float'):
          if(contLocal.contFloatVar +contLocal.limIFloatVar <= contLocal.limSFloatVar):
            existe = tablaLocalVars.insertar(t[2], t[4], None, contLocal.contFloatVar + contLocal.limIFloatVar, None)
            contLocal.contFloatVar = contLocal.contFloatVar + 1
          else:
            print("Error: exceso de memoria en variables locales flotantes")
            exit(1)
        if(t[4] == 'string'):
          if(contLocal.contStringVar +contLocal.limIStringVar <= contLocal.limSStringVar):
            existe = tablaLocalVars.insertar(t[2], t[4], None, contLocal.contStringVar + contLocal.limIStringVar, None)
            contLocal.contStringVar = contLocal.contStringVar + 1
          else:
            print("Error: exceso de memoria en variables locales string")
            exit(1)
        if(t[4] == 'bool'):
          if(contLocal.contBoolVar +contLocal.limIBoolVar <= contLocal.limSBoolVar):
            existe = tablaLocalVars.insertar(t[2], t[4], None, contLocal.contBoolVar + contLocal.limIBoolVar, None)
            contLocal.contBoolVar = contLocal.contBoolVar + 1
          else:
            print("Error: exceso de memoria en variables locales bool")
            exit(1)
        if(existe == False):
          print("Error - variable ya declarada en parametros: ", t[2])
          exit(1)
      
        
  
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

def p_bloque_return(t):
    '''bloque_return : LCBRAC estatutos regresar RCBRAC 
    | LCBRAC estatutos regresar_void RCBRAC'''

def p_estatutos(t):
    '''estatutos : estatuto estatutos
    | e '''

#*********** estatuto ***********
def p_estatuto(t):
    '''estatuto : asignacion
    | condicion
    | llamada_void SEMICOLON
    | leer
    | escribir
    | ciclo_w
    | ciclo_f'''

#*********** asignacion ***********
def p_asignacion(t):
    'asignacion : variable EQ expresion SEMICOLON atomic_assign'

def p_atomic_assign(t):
    'atomic_assign : e'
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
        
#************ variable ************
curVar = None
isArr = False
def p_variable(t):
    'variable : var_id variable1 variable2'

def p_var_id(t):
    'var_id : ID'
    global curVar
    curVar = t[1]
    existe = tablaVariables.buscar(t[1])
    existeLocal = tablaLocalVars.buscar(t[1])
    existeClase = tablaVarsClase.buscar(t[1])
    if(existeLocal != None):
        PilaO.append(existeLocal[2])
        PilaTipos.append(existeLocal[0])
    elif(dentroClase and existeClase != None):
        PilaO.append(existeClase[2])
        PilaTipos.append(existeClase[0]) 
    elif(existe != None):
        PilaO.append(existe[2])
        PilaTipos.append(existe[0])
    else:
        print("Error de semantica: variable no declarada: ", t[1])
        exit(1)

def p_variable1(t):
    '''variable1 : QUESTION ID 
    | e'''
    if (t[1] == '?'):
        existe = tablaObjetos.buscar(curVar)
        if(existe != None):
            existeVar = existe[1].get(t[2])
            if(existeVar != None):
                PilaO.pop() # saca el append anterior en caso de que sea una variable de objeto
                PilaTipos.pop()
                PilaO.append(existeVar[2])
                PilaTipos.append(existeVar[0])
                sem.intermediario('eraObjeto', None, None, existe[3])
                global contCuad
                contCuad += 1
            else:
                print("Error de semantica: variable de clase no declarada: ", t[2])
                exit(1)
        else:
            print("Error de semantica: variable no declarada: ", t[2])
            exit(1)

def p_variable2(t):
    '''variable2 : LSBRAC expresion verifica_d1 push_mult pop_operador RSBRAC variable3 push_plus pop_operador push_plus push_arr pop_operador
    | e'''
    # multiplicar valD1 m1 temp1
    # sumar temp1 valD2 temp2
    # sumar temp2 dirBase temp3

def p_push_arr(t):
    'push_arr : e'
    global isArr
    isArr = True
    v1 = PilaO.pop()
    v2 = PilaO.pop()
    PilaO.append(contTPointers.contInt + contTPointers.limIInt)
    if(contConst.contInt + contConst.limIInt < contConst.limSInt):
        tablaConstantes.insertar(contConst.contInt + contConst.limIInt, v2)
        PilaO.append(contConst.contInt + contConst.limIInt)
        contConst.contInt = contConst.contInt + 1
    else: 
        print("Limite de memoria excedido para constantes")
        exit(1)
    PilaO.append(v1)

def p_verifica_d1(t):
    'verifica_d1 : e'
    exp_type = PilaTipos[-1]
    global contCuad
    if (exp_type == 'int'):
        exp_value = PilaO[-1]
        valores = tablaVariables.buscar(curVar)
        sem.intermediario('verifica', exp_value, valores[3].limInfD1, valores[3].limSupD1)
        contCuad += 1
        if(contConst.contInt + contConst.limIInt < contConst.limSInt):
          tablaConstantes.insertar(contConst.contInt + contConst.limIInt, valores[3].m1)
          PilaO.append(contConst.contInt + contConst.limIInt)
          PilaTipos.append("int")
          contConst.contInt = contConst.contInt + 1
        else: 
          print("Limite de memoria excedido para constantes")
          exit(1)

def p_variable3(t):
    '''variable3 : LSBRAC expresion verifica_d2 RSBRAC
    | e'''
    if (t[1] != '['):
        if(contConst.contInt + contConst.limIInt < contConst.limSInt):
          tablaConstantes.insertar(contConst.contInt + contConst.limIInt, 0)
          PilaO.append(contConst.contInt + contConst.limIInt)
          PilaTipos.append("int")
          contConst.contInt = contConst.contInt + 1
        else: 
          print("Limite de memoria excedido para constantes")
          exit(1)

def p_verifica_d2(t):
    'verifica_d2 : e'
    exp_type = PilaTipos[-1]
    global contCuad
    if (exp_type == 'int'):
        exp_value = PilaO[-1]
        valores = tablaVariables.buscar(curVar)
        sem.intermediario('verifica', exp_value, valores[3].limInfD1, valores[3].limSupD1)
        contCuad += 1

#*********** llamada ************
contadorParam = 0

def p_llamada(t):
    'llamada : validar_id llamada1 LPAR llamada2 RPAR'
    if(t[1][0] != 'none'):
        global contadorParam, tipos_param, contCuad
        if(t[1][0] == 'iter objeto'):
            obj = tablaObjetos.buscar(t[1][1])
            claseNom = obj[0]
            clase = tablaClases.buscar(claseNom)
            func = clase[1].get(t[2])
            if(contadorParam == len(tipos_param)):
                sem.intermediario("gosub", None, None, func[2])
                contCuad = contCuad + 1
            else:
                print("Error: el numero de parametros no coincide", t[2])
                exit(1)
        else:
            if(contadorParam == len(tipos_param)):
                funcStart = tablaFunciones.buscar(t[1][0])
                sem.intermediario("gosub", None, None, funcStart[2])
                contCuad = contCuad + 1
            else:
                print("La cantidad de parametros de la llamada no coincide con la cantidad de parametros que recibe la funcion: ", t[1][0])
                exit(1)

def p_llamada_void(t):
    'llamada_void : validar_id llamada1 LPAR llamada2 RPAR'
    # checar que el tipo de funcion es void
    if(t[1][0] != 'none'):
        global contadorParam, tipos_param, contCuad
        if(t[1][0] == 'iter objeto'):
            obj = tablaObjetos.buscar(t[1][1])
            claseNom = obj[0]
            clase = tablaClases.buscar(claseNom)
            func = clase[1].get(t[2])
            tipoFunc = func[0]
            if(contadorParam == len(tipos_param)):
                if(tipoFunc == 'void'):
                    sem.intermediario("gosub", None, None, func[2])
                    contCuad = contCuad + 1
                else:
                    print("Error: se esperaba una llamada a una funcion void o asignar un valor a una variable")
                    exit(1)
            else:
                print("Error: el numero de parametros no coincide", t[2])
                exit(1)
        else:
            funcStart = tablaFunciones.buscar(t[1][0])
            tipoFunc = funcStart[0]
            if(contadorParam == len(tipos_param)):
                if(tipoFunc == 'void'):
                    sem.intermediario("gosub", None, None, funcStart[2])
                    contCuad = contCuad + 1
                else:
                    print("Error: se esperaba una llamada a una funcion void o asignar un valor a una variable")
                    exit(1)
            else:
                print("Error: el numero de parametros no coincide", t[1][0])
                exit(1)
        
tipos_param = []
def p_validar_id(t):
    'validar_id : ID'
    obj = tablaObjetos.buscar(t[1])
    func = tablaFunciones.buscar(t[1])
    if(obj != None):
        PilaO.append(t[1])
        PilaO.append(obj)
        PilaO.append(obj[0])
        t[0] = ['iter objeto', t[1]]
    elif(func != None):
        global contCuad, contadorParam, tipos_param
        sem.intermediario("era", None, None, t[1])
        contCuad = contCuad + 1        
        contadorParam = 0
        funcStart = tablaFunciones.buscar(t[1])
        tipos_param = funcStart[1]
        try:
          valores = tablaVariables.buscar(t[1])
          PilaO.append(valores[1])
          PilaTipos.append(valores[0])
        except:
          pass
        t[0] = [t[1], None]
    else:
        print("Function not declared")
        t[0] = ['none', None]

def p_llamada1(t):
    '''llamada1 : DOT ID
    | e'''
    if(t[1] == '.'):
        clase = PilaO.pop()
        objeto = PilaO.pop()
        objetoNom = PilaO.pop()
        dirVObj = tablaObjetos.buscar(objetoNom)[3]
        valoresClase = tablaClases.buscar(clase)
        funciones = valoresClase[1]
        existe = funciones.get(t[2])
        if(existe != None):
            global contCuad, contadorParam, tipos_param
            sem.intermediario("eraObjeto", None, None, dirVObj )
            contCuad = contCuad + 1
            sem.intermediario("era", None, None, t[2])
            contCuad = contCuad + 1
            contadorParam = 0
            tipos_param = existe[1]
            try:
              valores = objeto[1].get(t[2])
              PilaO.append(valores[1])
              PilaTipos.append(valores[0])
            except:
              pass
            t[0] = t[2]
        else:
          print("Function not declared")

def p_llamada2(t):
    '''llamada2 : expresion cuad_param llamada3
    | e'''
  

def p_cuad_param(t):
    'cuad_param : e'
    global contCuad, contadorParam, tipos_param
    sendParam = PilaO.pop()
    sendParamType = PilaTipos.pop()
    if(sendParam == None):
        sendParam = 'Array'
    if(contadorParam >= len(tipos_param)):
        print("Error: el numero de parametros no coincide ")
        exit(1)
    else:
        if(tipos_param[contadorParam] == sendParamType):
            contadorParam = contadorParam + 1
            sem.intermediario("param", sendParam, None, contadorParam)
            contCuad = contCuad + 1
        else:
            print("Error: type mismatch en parametros: ", sendParam)
            exit(1)

def p_llamada3(t):
    '''llamada3 : COMMA expresion cuad_param llamada3
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
    global tablaConstantes, contConst, tablaLocalConst, contLocal
    if(dentroFuncion):
      if(contLocal.contStringConst + contLocal.limIStringConst < contLocal.limSStringConst):
        cteStr = str(t[1]).replace('"', '')
        tablaLocalConst.insertar(contLocal.contStringConst + contLocal.limIStringConst, cteStr)
        PilaO.append(contLocal.contStringConst + contLocal.limIStringConst)
        PilaTipos.append("string")
        contLocal.contStringConst = contLocal.contStringConst + 1
      else: 
        print("Limite de memoria excedido para constantes")
        exit(1)
    else:
      if(contConst.contString + contConst.limIString < contConst.limSString):
        cteStr = str(t[1]).replace('"', '')
        tablaConstantes.insertar(contConst.contString + contConst.limIString, cteStr)
        PilaO.append(contConst.contString + contConst.limIString)
        PilaTipos.append("string")
        contConst.contString = contConst.contString + 1
      else: 
        print("Limite de memoria excedido para constantes")
        exit(1)

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
    sem.cuadruplos[salida].res = contCuad

#*********** ciclo_f ************
def p_ciclo_f(t):
    'ciclo_f : FROM LPAR variable asign_aux EQ expresion atomic_assign save_aux TO for_temp asign_aux2 expresion atomic_assign save_aux2 migaja push_lt pop_operador gotoF RPAR DO save_aux bloque update_fill_go'

def p_for_temp(t):
    'for_temp : e'
    if(dentroFuncion):
        if(contLocal.contIntTemp + contLocal.limIIntTemp < contLocal.limSIntTemp):
            temporal = contLocal.contIntTemp + contLocal.limIIntTemp
            temporalTipo = PilaTipos[-1]
            PilaO.append(temporal)
            PilaTipos.append(temporalTipo)
            tablaLocalTemps.insertar(temporal, None)
            contLocal.contIntTemp += 1
        else:
            print("Error: limite de memoria excedido")
            exit(1)
    else: # for afuera de funcion
        if(contTemps.contInt + contTemps.limIInt < contTemps.limSInt):
            temporal = contTemps.contInt + contTemps.limIInt
            temporalTipo = PilaTipos[-1]
            PilaO.append(temporal)
            PilaTipos.append(temporalTipo)
            tablaTemporales.insertar(temporal, None)
            contTemps.contInt += 1
        else:
            print("Error: limite de memoria excedido")
            exit(1)

def p_migaja(t):
    'migaja : e'
    global contCuad
    PilaSaltos.append(contCuad)

def p_update_fill_go(t):
    'update_fill_go : save_aux push_plus push1 pop_operador  atomic_assign'
    global contCuad
    fill = PilaSaltos.pop() - 1
    ret = PilaSaltos.pop()
    sem.intermediario("goto", None, None, ret)
    contCuad = contCuad + 1
    sem.cuadruplos[fill].res = contCuad    

foraux1 = 0
foraux1Tipo = ''
def p_asign_aux(t):
    'asign_aux : e'
    global foraux1, foraux1Tipo
    foraux1 = PilaO[-1]
    foraux1Tipo = PilaTipos[-1]
    
foraux2 = 0
foraux2Tipo = ''
def p_asign_aux2(t):
    'asign_aux2 : e'
    global foraux2, foraux2Tipo
    foraux2 = PilaO[-1]
    foraux2Tipo = PilaTipos[-1]

def p_push1(t):
    'push1 : e'
    cons = contConst.contInt + contConst.limIInt
    PilaO.append(cons)
    PilaTipos.append("int")
    tablaConstantes.insertar(cons, 1)
    contConst.contInt += 1

def p_save_aux(t):
    'save_aux : e'
    global foraux1, foraux1Tipo
    PilaO.append(foraux1)
    PilaTipos.append(foraux1Tipo)
    
def p_save_aux2(t):
    'save_aux2 : e'
    global foraux2, foraux2Tipo
    PilaO.append(foraux2)
    PilaTipos.append(foraux2Tipo)

#*********** regresar ***********      
def p_regresar(t):
    'regresar : RETURN expresion SEMICOLON'
    #checar tipo exp vs funcion
    tipo_exp = PilaTipos.pop()
    tipo_func = PilaTipos.pop()
    if(tipo_exp != tipo_func):
      print("Error de tipo de dato de retorno y funcion")
      exit(1)
    else:
      valRet = PilaO.pop()
      sem.intermediario('return', None, None, valRet)
      PilaTipos.append(tipo_func)
      PilaO.append(valRet)
      PilaTipos.append(tipo_exp)
      global contCuad
      contCuad = contCuad+1

def p_regresar_void(t):
    'regresar_void : RETURN SEMICOLON'
    tipo_func = PilaTipos.pop()
    if(tipo_func == 'void'):
        PilaTipos.append(tipo_func)
  
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
    global cont, contCuad, contTemps, tablaTemporales
    global tablaLocalTemps, contLocal, isArr
    if(rechazar == 0):
      if(dentroFuncion):
        if(contLocal.contIntTemp + contLocal.limIIntTemp < contLocal.limSIntTemp):
          sem.intermediario(str(operador), str(left_op), str(right_op), contLocal.contIntTemp + contLocal.limIIntTemp)
          contCuad = contCuad + 1
          PilaO.append(contLocal.contIntTemp + contLocal.limIIntTemp)
          tipo = cubo.getNumeroTipo(rechazar)
          PilaTipos.append(tipo)
          tablaLocalTemps.insertar(contLocal.contIntTemp + contLocal.limIIntTemp, None)
          contLocal.contIntTemp = contLocal.contIntTemp + 1
        else:
          print("Error: limite de memoria excedido")
          exit(1)
      elif (isArr):
          isArr = False
          sem.intermediario(str(operador), str(left_op), str(right_op), contTPointers.contInt + contTPointers.limIInt)
          contCuad = contCuad + 1
          tipo = cubo.getNumeroTipo(rechazar)
          PilaTipos.append(tipo)
          tablaTempPointers.insertar(contTPointers.contInt + contTPointers.limIInt, None)
          contTPointers.contInt += 1
      else:
        if(contTemps.contInt + contTemps.limIInt < contTemps.limSInt):
          sem.intermediario(str(operador), str(left_op), str(right_op), contTemps.contInt + contTemps.limIInt)
          contCuad = contCuad + 1
          PilaO.append(contTemps.contInt + contTemps.limIInt)
          tipo = cubo.getNumeroTipo(rechazar)
          PilaTipos.append(tipo)
          tablaTemporales.insertar(contTemps.contInt + contTemps.limIInt, None)
          contTemps.contInt = contTemps.contInt + 1
        else:
          print("Error: limite de memoria excedido")
          exit(1)
        
    elif(rechazar == 1):
      if(dentroFuncion):
        if(contLocal.contFloatTemp + contLocal.limIFloatTemp < contLocal.limSFloatTemp):
          sem.intermediario(str(operador), str(left_op), str(right_op), contLocal.contFloatTemp + contLocal.limIFloatTemp)
          contCuad = contCuad + 1
          PilaO.append(contLocal.contFloatTemp + contLocal.limIFloatTemp)
          tipo = cubo.getNumeroTipo(rechazar)
          PilaTipos.append(tipo)
          tablaLocalTemps.insertar(contLocal.contFloatTemp + contLocal.limIFloatTemp, None)
          contLocal.contFloatTemp = contLocal.contFloatTemp + 1
        else:
          print("Error: limite de memoria excedido")
          exit(1)
      else:
        if(contTemps.contFloat + contTemps.limIFloat < contTemps.limSFloat):
          sem.intermediario(str(operador), str(left_op), str(right_op), contTemps.contFloat + contTemps.limIFloat)
          contCuad = contCuad + 1
          PilaO.append(contTemps.contFloat + contTemps.limIFloat)
          tipo = cubo.getNumeroTipo(rechazar)
          PilaTipos.append(tipo)
          tablaTemporales.insertar(contTemps.contFloat + contTemps.limIFloat, None)
          contTemps.contFloat = contTemps.contFloat + 1
        else:
          print("Error: limite de memoria excedido")
          exit(1)
          
        
    elif(rechazar == 2):
      if(dentroFuncion):
        if(contLocal.contStringTemp + contLocal.limIStringTemp < contLocal.limSStringTemp):
          sem.intermediario(str(operador), str(left_op), str(right_op), contLocal.contStringTemp + contLocal.limIStringTemp )
          contCuad = contCuad + 1
          PilaO.append(contLocal.contStringTemp + contLocal.limIStringTemp )
          tipo = cubo.getNumeroTipo(rechazar)
          PilaTipos.append(tipo)
          tablaLocalTemps.insertar(contLocal.contStringTemp + contLocal.limIStringTemp , None)
          contLocal.contStringTemp = contLocal.conStringTemp + 1
        else:
          print("Error: limite de memoria excedido")
          exit(1)
      else:
        if(contTemps.contString + contTemps.limIString < contTemps.limSString):
          sem.intermediario(str(operador), str(left_op), str(right_op), contTemps.contString + contTemps.limIString )
          contCuad = contCuad + 1
          PilaO.append(contTemps.contString + contTemps.limIString )
          tipo = cubo.getNumeroTipo(rechazar)
          PilaTipos.append(tipo)
          tablaTemporales.insertar(contTemps.contString + contTemps.limIString , None)
          contTemps.contString = contTemps.conString + 1
        else:
          print("Error: limite de memoria excedido")
          exit(1)
        
    elif(rechazar == 3):
      if(dentroFuncion):
        if(contLocal.contBoolTemp + contLocal.limIBoolTemp < contLocal.limSBoolTemp):
          sem.intermediario(str(operador), str(left_op), str(right_op), contLocal.contBoolTemp + contLocal.limIBoolTemp)
          contCuad = contCuad + 1
          PilaO.append(contLocal.contBoolTemp + contLocal.limIBoolTemp)
          tipo = cubo.getNumeroTipo(rechazar)
          PilaTipos.append(tipo)
          tablaLocalTemps.insertar(contLocal.contBoolTemp + contLocal.limIBoolTemp, None)
          contLocal.contBoolTemp = contLocal.contBoolTemp + 1
        else:
          print("Error: limite de memoria excedido")
          exit(1) 
      else:
        if(contTemps.contBool + contTemps.limIBool < contTemps.limSBool):
          sem.intermediario(str(operador), str(left_op), str(right_op), contTemps.contBool + contTemps.limIBool)
          contCuad = contCuad + 1
          PilaO.append(contTemps.contBool + contTemps.limIBool)
          tipo = cubo.getNumeroTipo(rechazar)
          PilaTipos.append(tipo)
          tablaTemporales.insertar(contTemps.contBool + contTemps.limIBool, None)
          contTemps.contBool = contTemps.contBool + 1
        else:
          print("Error: limite de memoria excedido")
          exit(1) 
        
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
    global PilaTipos, tablaLocalConst
    tipo = PilaTipos.pop()
    if(tipo == 'int'):
      if(dentroFuncion):
        if(contLocal.contIntConst + contLocal.limIIntConst < contLocal.limSIntConst):
          tablaLocalConsts.insertar(contLocal.contIntConst + contLocal.limIIntConst, t[1])
          PilaO.append(contLocal.contIntConst + contLocal.limIIntConst)
          PilaTipos.append("int")
          contLocal.contIntConst = contLocal.contIntConst + 1
        else: 
          print("Limite de memoria excedido para constantes")
          exit(1)
      else:
        if(contConst.contInt + contConst.limIInt < contConst.limSInt):
          tablaConstantes.insertar(contConst.contInt + contConst.limIInt, t[1])
          PilaO.append(contConst.contInt + contConst.limIInt)
          PilaTipos.append("int")
          contConst.contInt = contConst.contInt + 1
        else: 
          print("Limite de memoria excedido para constantes")
          exit(1)
      
    elif(tipo == 'float'):
      if(dentroFuncion):
        if(contLocal.contFloatConst + contLocal.limIFloatConst < contLocal.limSFloatConst):
          tablaLocalConsts.insertar(contLocal.contFloatConst + contLocal.limIFloatConst, t[1])
          PilaO.append(contLocal.contFloatConst + contLocal.limIFloatConst)
          PilaTipos.append("float")
          contLocal.contFloatConst = contLocal.contFloatConst + 1
        else: 
          print("Limite de memoria excedido para constantes")
          exit(1)
      else:
        if(contConst.contFloat + contConst.limIFloat < contConst.limSFloat):
          tablaConstantes.insertar(contConst.contFloat + contConst.limIFloat, t[1])
          PilaO.append(contConst.contFloat + contConst.limIFloat)
          PilaTipos.append("float")
          contConst.contFloat = contConst.contFloat + 1
        else: 
          print("Limite de memoria excedido para constantes")
          exit(1)

    elif(tipo == 'string'):
      if(dentroFuncion):
        if(contLocal.contStringConst + contLocal.limIStringConst < contLocal.limSStringConst):
          tablaLocalConsts.insertar(contLocal.contStringConst + contLocal.limIStringConst, t[1])
          PilaO.append(contLocal.contStringConst + contLocal.limIStringConst)
          PilaTipos.append("string")
          contLocal.contStringConst = contLocal.contStringConst + 1
        else: 
          print("Limite de memoria excedido para constantes")
          exit(1)
      else:
        if(contConst.contString + contConst.limIString < contConst.limSString):
          cteStr = str(t[1]).replace('"', '')
          tablaConstantes.insertar(contConst.contString + contConst.limIString, cteStr)
          PilaO.append(contConst.contString + contConst.limIString)
          PilaTipos.append("string")
          contConst.contString = contConst.contString + 1
        else: 
          print("Limite de memoria excedido para constantes")
          exit(1)

    elif(tipo == 'bool'):
      if(dentroFuncion):
        if(contLocal.contBoolConst + contLocal.limIBoolConst < contLocal.limSBoolConst):
          tablaLocalConsts.insertar(contLocal.contBoolConst + contLocal.limIBoolConst, t[1])
          PilaO.append(contLocal.contBoolConst + contLocal.limIBoolConst)
          PilaTipos.append("bool")
          contLocal.contBoolConst = contLocal.contBoolConst + 1
        else: 
          print("Limite de memoria excedido para constantes")
          exit(1)
      else:
        if(contConst.contBool + contConst.limIBool < contConst.limSBool):
          tablaConstantes.insertar(contConst.contBool + contConst.limIBool, t[1])
          PilaO.append(contConst.contBool + contConst.limIBool)
          PilaTipos.append("bool")
          contConst.contBool = contConst.contBool + 1
        else: 
          print("Limite de memoria excedido para constantes")
          exit(1)
    
    t[0]=t[1]

def p_ctei(t):
    'ctei : e'
    PilaTipos.append('int')

def p_ctef(t):
    'ctef : e'
    PilaTipos.append('float')

def p_ctestr(t):
    'ctestr : e'
    PilaTipos.append('string')

def p_cteb(t):
    'cteb : e'
    PilaTipos.append('bool')

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
    exit(1)

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
    print(PilaO)
    print(PilaTipos)
    print(PilaSaltos)
    
    # crear directorio de funciones y lo guarda
    dirFunc = {}
    for i in tablaFunciones.dict:
      auxFunc = tablaFunciones.buscar(i)
      # parametros, inicio, [vi, vf, vs, vb, ti, tf, ts, tb], tablaConst
      # nuevo {nombreFunc: [[recursos], [constantes]]}
      func = {i : [auxFunc[4], auxFunc[5]]}
      dirFunc.update(func)
    f = open('dirF.txt','w')
    f.write(str(dirFunc))
    f.close()

    # codigo intermedio (objeto)
    f = open('intermedio.txt','w')
    tablaVars = {}
    for i in tablaVariables.dict:
      dictAux = {}
      dirB = tablaVariables.dict[i][2]
      if tablaVariables.dict[i][3] != None: # es var dimensionada
        tam = tablaVariables.dict[i][3].limSupD1 * tablaVariables.dict[i][3].m1
        for i in range(tam+1):
          dictAux = {dirB + i: None}
          tablaVars.update(dictAux)
      else:
          dictAux = {dirB: None}
          tablaVars.update(dictAux)
    f.write(str(tablaVars)[:-1] + ',')
    f.write('\n' + str(tablaTemporales.dict)[:-1] + ',')
    f.write('\n' + str(tablaTempPointers.dict)[:-1] + ',')
    f.write('\n' + str(tablaConstantes.dict)[:-1] + ',')
    f.write('\n' + "#cuadruplos,")
    for i in sem.cuadruplos:
      f.write('\n' + str(i.operation) + ', ' + str(i.arg1) + ', ' + str(i.arg2) + ', ' + str(i.res) + ',')
    f.close()