import dirVir as dir
import ast

# abrir archivo intermedio
f = open('intermedio.txt','r')

# funcion para leer data segment
class tipos:
    def __init__(self):
        self.int = []
        self.float = []
        self.string = []
        self.bool = []
        self.obj = []

class contFuncs:
    def __init__(self):
        self.contInt = 0
        self.contFloat = 0
        self.contStr = 0
        self.contBool = 0
        self.contFunc = 0
    def reset(self):
        self.contInt = 0
        self.contFloat = 0
        self.contStr = 0
        self.contBool = 0        

dirs = [dir.varGlobal(), dir.varTemps(), dir.varTempsPointer(), dir.varConst(), dir.varLocal(), dir.varClases()]
dataS = [tipos(), tipos(), tipos(), tipos()]
def readAndSaveData(table):
    line = f.readline()
    pos = line.find(':')
    while pos != -1:
        dir = int(line[1:pos])
        line = line[pos+1:]
        pos = line.find(',')
        value = line[1:pos]
        line = line[pos+1:]
        if (dir >= dirs[table].limIInt and dir <= dirs[table].limSInt):
            dataS[table].int.insert(dir-dirs[table].limIInt, value)
        elif (dir >= dirs[table].limIFloat and dir <= dirs[table].limSFloat):
            dataS[table].float.insert(dir-dirs[table].limIFloat, value)
        elif (dir >= dirs[table].limIString and dir <= dirs[table].limSString):
            if(table == 3):
                value = value[1:-1]
            dataS[table].string.insert(dir-dirs[table].limIString, value)
        elif (dir >= dirs[table].limIBool and dir <= dirs[table].limSBool):
            dataS[table].bool.insert(dir-dirs[table].limIBool, value)
        elif (table == 0 and dir >= dirs[table].limIObj and dir <= dirs[table].limSObj):
            dataS[table].obj.insert(dir-dirs[table].limIObj, value)
        pos = line.find(':')
    
# leer la tabla de vars globales
readAndSaveData(0)
# leer la tabla de temps globales
readAndSaveData(1)
# leer la tabla de temps pointer
readAndSaveData(2)
# leer la tabla de constantes globales
readAndSaveData(3)

# leer cuadruplos, code segment
codeS = []
line = f.readline()
codeS.append(line)
lines = f.read().splitlines()
for line in lines:
    values = []
    while len(line) > 1:
        pos = line.find(',')
        try:
            values.append(int(line[:pos]))
        except:
            values.append(line[:pos])
        line = line[pos+2:]
    codeS.append(values)

f.close()
    
# regresa valor, faltan los objetos
def fetchDir(dir):
    if(dir > 10000 and dir < 14001): # es local
        curFunc = len(stackS) - 1
        if(dir > 10000 and dir < 12001): # es temporal local
            if(dir >= dirs[4].limIIntTemp and dir <= dirs[4].limSIntTemp):
                return int(stackS[curFunc][1].int[dir - dirs[4].limIIntTemp])
            elif(dir >= dirs[4].limIFloatTemp and dir <= dirs[4].limSFloatTemp):
                return float(stackS[curFunc][1].float[dir - dirs[4].limIFloatTemp])
            elif(dir >= dirs[4].limIStringTemp and dir <= dirs[4].limSStringTemp):
                return str(stackS[curFunc][1].string[dir - dirs[4].limIStringTemp])
            elif(dir >= dirs[4].limIBoolTemp and dir <= dirs[4].limSBoolTemp):
                return bool(stackS[curFunc][1].bool[dir - dirs[4].limIBoolTemp])
        elif(dir > 12000 and dir < 13001): # es constante local
            if(dir >= dirs[4].limIIntConst and dir <= dirs[4].limSIntConst):
                return int(stackS[curFunc][2].int[dir - dirs[4].limIIntConst])
            elif(dir >= dirs[4].limIFloatConst and dir <= dirs[4].limSFloatConst):
                return float(stackS[curFunc][2].float[dir - dirs[4].limIFloatConst])
            elif(dir >= dirs[4].limIStringConst and dir <= dirs[4].limSStringConst):
                return str(stackS[curFunc][2].string[dir - dirs[4].limIStringConst])
            elif(dir >= dirs[4].limIBoolConst and dir <= dirs[4].limSBoolConst):
                return bool(stackS[curFunc][2].bool[dir - dirs[4].limIBoolConst])
        elif(dir > 13000 and dir < 14001): # es variable local
            if(dir >= dirs[4].limIIntVar and dir <= dirs[4].limSIntVar):
                res = stackS[curFunc][0].int[dir - dirs[4].limIIntVar]
                if(res != None):
                    return int(res)
                else:
                    try:
                        return int(stackS[curFunc-1][0].int[dir - dirs[4].limIIntVar])
                    except:
                        print("Error: Se usa variable que aun no ha sido asignada", dir)
                        exit(1)
            elif(dir >= dirs[4].limIFloatVar and dir <= dirs[4].limSFloatVar):
                res = stackS[curFunc][0].float[dir - dirs[4].limIFloatVar]
                if(res != None):
                    return float(res)
                else:
                    try:
                        return float(stackS[curFunc-1][0].float[dir - dirs[4].limIFloatVar])                        
                    except:
                        print("Error: Se usa variable que aun no ha sido asignada", dir)
                        exit(1)
            elif(dir >= dirs[4].limIStringVar and dir <= dirs[4].limSStringVar):
                res = stackS[curFunc][0].string[dir - dirs[4].limIStringVar]
                if(res != None):
                    return str(res)
                else:
                    try:
                        return str(stackS[curFunc-1][0].string[dir - dirs[4].limIStringVar])                        
                    except:
                        print("Error: Se usa variable que aun no ha sido asignada", dir)
                        exit(1)
            elif(dir >= dirs[4].limIBoolVar and dir <= dirs[4].limSBoolVar):
                res = stackS[curFunc][0].bool[dir - dirs[4].limIBoolVar]
                if(res != None):
                    return bool(res)
                else:
                    try:
                        return bool(stackS[curFunc-1][0].bool[dir - dirs[4].limIBoolVar])
                    except:
                        print("Error: Se usa variable que aun no ha sido asignada", dir)
                        exit(1)
    elif(dir > 26000 and dir < 29551 ): # es var de clase
        global curObj
        if(dir >= dirs[5].limIInt and dir <= dirs[5].limSInt):
            try:
                return int(objS[curObj][1].int[dir - dirs[5].limIInt])
            except:
                print("Error: Se usa variable que aun no ha sido asignada", dir)
                exit(1)
        elif(dir >= dirs[5].limIFloat and dir <= dirs[5].limSFloat):
            try:
                return float(objS[curObj][1].float[dir - dirs[5].limIFloat])
            except:
                print("Error: Se usa variable que aun no ha sido asignada", dir)
                exit(1)
        elif(dir >= dirs[5].limIString and dir <= dirs[5].limSString):
            try:
                return str(objS[curObj][1].string[dir - dirs[5].limIString])
            except:
                print("Error: Se usa variable que aun no ha sido asignada", dir)
                exit(1)
        elif(dir >= dirs[5].limIBool and dir <= dirs[5].limSBool):
            try:
                return bool(objS[curObj][1].bool[dir - dirs[5].limIBool])
            except:
                print("Error: Se usa variable que aun no ha sido asignada", dir)
                exit(1)
        elif(dir >= dirs[5].limIObj and dir <= dirs[5].limSObj):
            try:
                return int(objS[curObj][1].obj[dir - dirs[5].limIObj])
            except:
                print("Error: Se usa variable que aun no ha sido asignada", dir)
                exit(1)
    else: # no es local
        for i in range(4):            
            if (dir >= dirs[i].limIInt and dir <= dirs[i].limSInt):
                if (dir > 29550):
                    res = dataS[i].int[dir - dirs[i].limIInt]
                    if(res >= dirs[0].limIInt and res <= dirs[0].limSInt):
                        try:
                            return int(dataS[0].int[res - dirs[0].limIInt])
                        except:
                            print("Error: Se usa variable que aun no ha sido asignada", dir)
                        exit(1)
                    elif(res >= dirs[0].limIFloat and res <= dirs[0].limSFloat):
                        try:
                            return float(dataS[0].float[res - dirs[0].limIFloat])
                        except:
                            print("Error: Se usa variable que aun no ha sido asignada", dir)
                        exit(1)
                    elif(res >= dirs[0].limIString and res <= dirs[0].limSString):
                        try:
                            return str(dataS[0].string[res - dirs[0].limIString])
                        except:
                            print("Error: Se usa variable que aun no ha sido asignada", dir)
                        exit(1)
                    elif(res >= dirs[0].limIBool and res <= dirs[0].limSBool):
                        try:
                            return bool(dataS[0].bool[res - dirs[0].limIBool])
                        except:
                            print("Error: Se usa variable que aun no ha sido asignada", dir)
                        exit(1)
                else:
                    try:
                        return int(dataS[i].int[dir - dirs[i].limIInt])
                    except:
                        print("Error: Se usa variable que aun no ha sido asignada", dir)
                        exit(1)
            elif (dir >= dirs[i].limIFloat and dir <= dirs[i].limSFloat):
                try:
                    return float(dataS[i].float[dir - dirs[i].limIFloat])
                except:
                    print("Error: Se usa variable que aun no ha sido asignada")
                    exit(1)
            elif (dir >= dirs[i].limIString and dir <= dirs[i].limSString):
                try:
                    return str(dataS[i].string[dir - dirs[i].limIString])
                except:
                    print("Error: Se usa variable que aun no ha sido asignada")
                    exit(1)
            elif (dir >= dirs[i].limIBool and dir <= dirs[i].limSBool):
                try:
                    return bool(dataS[i].bool[dir - dirs[i].limIBool])
                except:
                    print("Error: Se usa variable que aun no ha sido asignada")
                    exit(1)

def fetchType(dir):
    if(dir > 10000 and dir < 14001): # es local
        if(dir > 10000 and dir < 12001): # es temporal local
            if(dir >= dirs[4].limIIntTemp and dir <= dirs[4].limSIntTemp):
                return 'int'
            elif(dir >= dirs[4].limIFloatTemp and dir <= dirs[4].limSFloatTemp):
                return 'float'
            elif(dir >= dirs[4].limIStringTemp and dir <= dirs[4].limSStringTemp):
                return 'str'
            elif(dir >= dirs[4].limIBoolTemp and dir <= dirs[4].limSBoolTemp):
                return 'bool'
        elif(dir > 12000 and dir < 13001): # es constante local
            if(dir >= dirs[4].limIIntConst and dir <= dirs[4].limSIntConst):
                return 'int'
            elif(dir >= dirs[4].limIFloatConst and dir <= dirs[4].limSFloatConst):
                return 'float'
            elif(dir >= dirs[4].limIStringConst and dir <= dirs[4].limSStringConst):
                return 'str'
            elif(dir >= dirs[4].limIBoolConst and dir <= dirs[4].limSBoolConst):
                return 'bool'
        elif(dir > 13000 and dir < 14001): # es variable local
            if(dir >= dirs[4].limIIntVar and dir <= dirs[4].limSIntVar):
                return 'int'
            elif(dir >= dirs[4].limIFloatVar and dir <= dirs[4].limSFloatVar):
                return 'float'
            elif(dir >= dirs[4].limIStringVar and dir <= dirs[4].limSStringVar):
                return 'str'
            elif(dir >= dirs[4].limIBoolVar and dir <= dirs[4].limSBoolVar):
                return 'bool'
    elif(dir > 26000 and dir < 29551 ): # es var de clase
        if(dir >= dirs[5].limIInt and dir <= dirs[5].limSInt):
            return 'int'
        elif(dir >= dirs[5].limIFloat and dir <= dirs[5].limSFloat):
            return 'float'
        elif(dir >= dirs[5].limIString and dir <= dirs[5].limSString):
            return 'str'
        elif(dir >= dirs[5].limIBool and dir <= dirs[5].limSBool):
            return 'bool'
        elif(dir >= dirs[5].limIObj and dir <= dirs[5].limSObj):
            return 'obj'
    else: # es var global
        for i in range(4):
            if (dir >= dirs[i].limIInt and dir <= dirs[i].limSInt):
                return 'int'
            elif (dir >= dirs[i].limIFloat and dir <= dirs[i].limSFloat):
                return 'float'
            elif (dir >= dirs[i].limIString and dir <= dirs[i].limSString):
                return 'str'
            elif (dir >= dirs[i].limIBool and dir <= dirs[i].limSBool):
                return 'bool'

# escribe valor, faltan los objetos
def execDir(dir, value, op):
    try:
        if(dir > 10000 and dir < 14001): # es local
            curFunc = len(stackS) - 1
            if(dir > 10000 and dir < 12001): # es temporal local
                if(dir >= dirs[4].limIIntTemp and dir <= dirs[4].limSIntTemp):
                    stackS[curFunc][1].int[dir - dirs[4].limIIntTemp] = value
                elif(dir >= dirs[4].limIFloatTemp and dir <= dirs[4].limSFloatTemp):
                    stackS[curFunc][1].float[dir - dirs[4].limIFloatTemp] = value
                elif(dir >= dirs[4].limIStringTemp and dir <= dirs[4].limSStringTemp):
                    stackS[curFunc][1].string[dir - dirs[4].limIStringTemp] = value
                elif(dir >= dirs[4].limIBoolTemp and dir <= dirs[4].limSBoolTemp):
                    stackS[curFunc][1].bool[dir - dirs[4].limIBoolTemp] = value
            elif(dir > 12000 and dir < 13001): # es constante local
                if(dir >= dirs[4].limIIntConst and dir <= dirs[4].limSIntConst):
                    stackS[curFunc][2].int[dir - dirs[4].limIIntConst] = value
                elif(dir >= dirs[4].limIFloatConst and dir <= dirs[4].limSFloatConst):
                    stackS[curFunc][2].float[dir - dirs[4].limIFloatConst] = value
                elif(dir >= dirs[4].limIStringConst and dir <= dirs[4].limSStringConst):
                    stackS[curFunc][2].string[dir - dirs[4].limIStringConst] = value
                elif(dir >= dirs[4].limIBoolConst and dir <= dirs[4].limSBoolConst):
                    stackS[curFunc][2].bool[dir - dirs[4].limIBoolConst] = value
            elif(dir > 13000 and dir < 14001): # es variable local
                if(dir >= dirs[4].limIIntVar and dir <= dirs[4].limSIntVar):
                    stackS[curFunc][0].int[dir - dirs[4].limIIntVar] = value
                elif(dir >= dirs[4].limIFloatVar and dir <= dirs[4].limSFloatVar):
                    stackS[curFunc][0].float[dir - dirs[4].limIFloatVar] = value
                elif(dir >= dirs[4].limIStringVar and dir <= dirs[4].limSStringVar):
                    stackS[curFunc][0].string[dir - dirs[4].limIStringVar] = value
                elif(dir >= dirs[4].limIBoolVar and dir <= dirs[4].limSBoolVar):
                    stackS[curFunc][0].bool[dir - dirs[4].limIBoolVar] = value
        elif(dir > 26000 and dir < 29551 ): # es var de clase
            global curObj
            if(dir >= dirs[5].limIInt and dir <= dirs[5].limSInt):
                objS[curObj][1].int[dir - dirs[5].limIInt] = value
            elif(dir >= dirs[5].limIFloat and dir <= dirs[5].limSFloat):
                objS[curObj][1].float[dir - dirs[5].limIFloat] = value
            elif(dir >= dirs[5].limIString and dir <= dirs[5].limSString):
                objS[curObj][1].string[dir - dirs[5].limIString] = value
            elif(dir >= dirs[5].limIBool and dir <= dirs[5].limSBool):
                objS[curObj][1].bool[dir - dirs[5].limIBool] = value
            elif(dir >= dirs[5].limIObj and dir <= dirs[5].limSObj):
                objS[curObj][1].obj[dir - dirs[5].limIObj] = value
        else: # no es local
            for i in range(4):
                if (dir >= dirs[i].limIInt and dir <= dirs[i].limSInt):
                    if (dir > 29550 and op == '='):
                        res = dataS[i].int[dir - dirs[i].limIInt]
                        if(res >= dirs[0].limIInt and res <= dirs[0].limSInt):
                            dataS[0].int[res - dirs[0].limIInt] = value
                        elif(res >= dirs[0].limIFloat and res <= dirs[0].limSFloat):
                            dataS[0].float[res - dirs[0].limIFloat] = value
                        elif(res >= dirs[0].limIString and res <= dirs[0].limSString):
                            dataS[0].string[res - dirs[0].limIString] = value
                        elif(res >= dirs[0].limIBool and res <= dirs[0].limSBool):
                            dataS[0].bool[res - dirs[0].limIBool] = value
                    else:
                        dataS[i].int[dir - dirs[i].limIInt] = value
                elif (dir >= dirs[i].limIFloat and dir <= dirs[i].limSFloat):
                    dataS[i].float[dir - dirs[i].limIFloat] = value
                elif (dir >= dirs[i].limIString and dir <= dirs[i].limSString):
                    dataS[i].string[dir - dirs[i].limIString] = value
                elif (dir >= dirs[i].limIBool and dir <= dirs[i].limSBool):
                    dataS[i].bool[dir - dirs[i].limIBool] = value
    except:
        print("Variable no puede ser asignada")
        exit(1)

def boolValues(string):
    if string.lower() in ('true'):
        return True
    elif string.lower() in ('false'):
        return False
    else:
        exit(1)

# asignar recursos de funcion dentro del stack segment
stackS = []
def createMem(recursos, constantes, dirV):
    memFunc = [tipos(), tipos(), tipos(), dirV]
    contador = 0
    for i in recursos: # variables (parametros) y temporales
        if (contador < 4):
            if (contador == 0):
                memFunc[0].int = [None] * int(i)
            elif (contador == 1):
                memFunc[0].float = [None] * int(i)
            elif (contador == 2):
                memFunc[0].string = [None] * int(i)
            elif (contador == 3):
                memFunc[0].bool = [None] * int(i)
        else:
            if (contador == 4):
                memFunc[1].int = [None] * int(i)
            elif (contador == 5):
                memFunc[1].float = [None] * int(i)
            elif (contador == 6):
                memFunc[1].string = [None] * int(i)
            elif (contador == 7):
                memFunc[1].bool = [None] * int(i)
        contador += 1
    for i in constantes: # constantes
        valor = constantes.get(i)
        if (i >= dirs[4].limIIntConst and i <= dirs[4].limSIntConst):
            memFunc[2].int.insert(i-dirs[4].limIIntConst, valor)
        elif (i >= dirs[4].limIFloatConst and i <= dirs[4].limSFloatConst):
            memFunc[2].float.insert(i-dirs[4].limIFloatConst, valor)
        elif (i >= dirs[4].limIStringConst and i <= dirs[4].limSStringConst):
            memFunc[2].string.insert(i-dirs[4].limIStringConst, valor)
        elif (i >= dirs[4].limIBoolConst and i <= dirs[4].limSBoolConst):
            memFunc[2].bool.insert(i-dirs[4].limIBoolConst, valor)
    stackS.append(memFunc)

# asignar recursos de objetos dentro del object segment
objS = {}
def createMemObj(dirV, clase, atributos, funciones):
    memObj = [clase, tipos(), funciones]
    contador = 0
    for i in atributos: # variables del objeto
        if (contador == 0):
            memObj[1].int = [None] * int(i)
        elif (contador == 1):
            memObj[1].float = [None] * int(i)
        elif (contador == 2):
            memObj[1].string = [None] * int(i)
        elif (contador == 3):
            memObj[1].bool = [None] * int(i)
        contador += 1
    objAux = {dirV : memObj}
    objS.update(objAux)

# read dirFuncs
f = open('dirF.txt','r')
dirFuncStr = f.readline()
dirFuncClasesStr = f.readline()
f.close()
dirFunc = ast.literal_eval(dirFuncStr)
dirFuncClases = ast.literal_eval(dirFuncClasesStr)

# read dirObj
f = open('dirObj.txt','r')
dirObjStr = f.readline()
f.close()
dirObj = ast.literal_eval(dirObjStr)
    
# operaciones
print("-----maquina virtual-----")
ip = 1
saveIP = [ip]
curObj = 0
contParam = contFuncs()
numCuadruplos = len(codeS)
while ip < numCuadruplos:
    codigoOperacion = codeS[ip][0]
    if codigoOperacion == 'goto':
        ip = codeS[ip][3] - 1
    elif codigoOperacion == 'gotoF':    
        if (fetchDir(codeS[ip][1]) == False):
            ip = codeS[ip][3] - 1
    elif codigoOperacion == '=':
        execDir(codeS[ip][3], fetchDir(codeS[ip][1]), codigoOperacion)
    elif codigoOperacion == '*':
        execDir(codeS[ip][3], fetchDir(codeS[ip][1]) * fetchDir(codeS[ip][2]), codigoOperacion)
    elif codigoOperacion == '/':
        execDir(codeS[ip][3], fetchDir(codeS[ip][1]) / fetchDir(codeS[ip][2]), codigoOperacion)
    elif codigoOperacion == '+':
        execDir(codeS[ip][3], fetchDir(codeS[ip][1]) + fetchDir(codeS[ip][2]), codigoOperacion)
    elif codigoOperacion == '-':
        execDir(codeS[ip][3], fetchDir(codeS[ip][1]) - fetchDir(codeS[ip][2]), codigoOperacion)
    elif codigoOperacion == '||':
        execDir(codeS[ip][3], fetchDir(codeS[ip][1]) or fetchDir(codeS[ip][2]), codigoOperacion)
    elif codigoOperacion == '&&':
        execDir(codeS[ip][3], fetchDir(codeS[ip][1]) and fetchDir(codeS[ip][2]), codigoOperacion)
    elif codigoOperacion == '<':
        execDir(codeS[ip][3], fetchDir(codeS[ip][1]) < fetchDir(codeS[ip][2]), codigoOperacion)
    elif codigoOperacion == '>':
        execDir(codeS[ip][3], fetchDir(codeS[ip][1]) > fetchDir(codeS[ip][2]), codigoOperacion)
    elif codigoOperacion == '==':
        execDir(codeS[ip][3], fetchDir(codeS[ip][1]) == fetchDir(codeS[ip][2]), codigoOperacion)
    elif codigoOperacion == '!=':
        execDir(codeS[ip][3], fetchDir(codeS[ip][1]) != fetchDir(codeS[ip][2]), codigoOperacion)
    elif codigoOperacion == 'print':
        print(fetchDir(codeS[ip][3]))
    elif codigoOperacion == 'read':
        aux = input('read: ')
        try:
            tipo = fetchType(codeS[ip][3])
            if tipo == 'int':
                aux = int(aux)
            elif tipo == 'float':
                aux = float(aux)
            elif tipo == 'str':
                aux = str(aux)
            elif tipo == 'bool':
                aux = boolValues(aux)
            execDir(codeS[ip][3], aux, codigoOperacion)
        except:
            print("Error: El tipo de dato del input y de la variable en read() no coinciden")
            exit(1)
    elif codigoOperacion == 'verifica':
        if (fetchDir(codeS[ip][1]) < codeS[ip][2] or fetchDir(codeS[ip][1]) > codeS[ip][3]):
            print('Error: Indice de arreglo fuera de limites')
            exit(1)
    elif codigoOperacion == 'era':
        recursos = dirFunc.get(codeS[ip][3])
        recursos2 = dirFuncClases.get(codeS[ip][3])
        if(recursos != None):
            createMem(recursos[0], recursos[1], recursos[2])
        else:
            createMem(recursos2[0], recursos2[1], recursos2[2])
        contParam.reset()
    elif codigoOperacion == 'eraObjeto':
        curObj = codeS[ip][3]
        recursos = dirObj.get(curObj)
        verifica = objS.get(curObj)
        if (verifica == None):
            createMemObj(curObj, recursos[0], recursos[1], recursos[2])
        contParam.reset()
    elif codigoOperacion == 'return':
        execDir(stackS[contParam.contFunc-1][3], fetchDir(codeS[ip][3]), '=')
    elif codigoOperacion == 'gosub':
        saveIP.append(ip)
        ip = codeS[ip][3] - 1
        contParam.contFunc += 1
    elif codigoOperacion == 'endfunc':
        ip = saveIP.pop()
        stackS.pop()
        contParam.contFunc -= 1
    elif codigoOperacion == 'endProgram':
        print("-----maquina virtual-----\nEjecucion finalizada.")
    elif codigoOperacion == 'param':
        tipo = fetchType(codeS[ip][1])
        if tipo == 'int':
            stackS[contParam.contFunc][0].int[contParam.contInt] = fetchDir(codeS[ip][1])
            contParam.contInt += 1
        elif tipo == 'float':
            stackS[contParam.contFunc][0].float[contParam.contFloat] = fetchDir(codeS[ip][1])
            contParam.contFloat += 1
        elif tipo == 'str':
            stackS[contParam.contFunc][0].string[contParam.contStr] = fetchDir(codeS[ip][1])
            contParam.contStr += 1
        elif tipo == 'bool':
            stackS[contParam.contFunc][0].bool[contParam.contBool] = fetchDir(codeS[ip][1])
            contParam.contBool += 1
            
    ip = ip + 1

