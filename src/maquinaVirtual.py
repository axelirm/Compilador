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

dirs = [dir.varGlobal(), dir.varTemps(), dir.varTempsPointer(), dir.varConst(), dir.varLocal()]
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
                return int(stackS[curFunc][0].int[dir - dirs[4].limIIntVar])
            elif(dir >= dirs[4].limIFloatVar and dir <= dirs[4].limSFloatVar):
                return float(stackS[curFunc][0].float[dir - dirs[4].limIFloatVar])
            elif(dir >= dirs[4].limIStringVar and dir <= dirs[4].limSStringVar):
                return str(stackS[curFunc][0].string[dir - dirs[4].limIStringVar])
            elif(dir >= dirs[4].limIBoolVar and dir <= dirs[4].limSBoolVar):
                return bool(stackS[curFunc][0].bool[dir - dirs[4].limIBoolVar])
    else: # no es local
        for i in range(4):            
            if (dir >= dirs[i].limIInt and dir <= dirs[i].limSInt):
                if dir > 29550:
                    try:
                        res = dataS[i].int[dir - dirs[i].limIInt]
                        return int(dataS[0].int[res - dirs[0].limIInt])
                    except:
                        print("Error: Variable has no value assigned", dir)
                    exit(1)
                try:
                    return int(dataS[i].int[dir - dirs[i].limIInt])
                except:
                    print("Error: Variable has no value assigned", dir)
                    exit(1)
            elif (dir >= dirs[i].limIFloat and dir <= dirs[i].limSFloat):
                try:
                    return float(dataS[i].float[dir - dirs[i].limIFloat])
                except:
                    print("Error: Variable has no value assigned")
                    exit(1)
            elif (dir >= dirs[i].limIString and dir <= dirs[i].limSString):
                try:
                    return str(dataS[i].string[dir - dirs[i].limIString])
                except:
                    print("Error: Variable has no value assigned")
                    exit(1)
            elif (dir >= dirs[i].limIBool and dir <= dirs[i].limSBool):
                try:
                    return bool(dataS[i].bool[dir - dirs[i].limIBool])
                except:
                    print("Error: Variable has no value assigned")
                    exit(1)

def fetchType(dir):
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
    else: # no es local
        for i in range(4):
            if (dir >= dirs[i].limIInt and dir <= dirs[i].limSInt):
                if (dir > 29550 and op == '='):
                    res = dataS[i].int[dir - dirs[i].limIInt]
                    dataS[0].int[res - dirs[0].limIInt] = value
                else:
                    dataS[i].int[dir - dirs[i].limIInt] = value
            elif (dir >= dirs[i].limIFloat and dir <= dirs[i].limSFloat):
                dataS[i].float[dir - dirs[i].limIFloat] = value
            elif (dir >= dirs[i].limIString and dir <= dirs[i].limSString):
                dataS[i].string[dir - dirs[i].limIString] = value
            elif (dir >= dirs[i].limIBool and dir <= dirs[i].limSBool):
                dataS[i].bool[dir - dirs[i].limIBool] = value

def boolValues(string):
    if string.lower() in ('true'):
        return True
    elif string.lower() in ('false'):
        return False
    else:
        exit(1)

# asignar recursos de funcion dentro del stack segment
stackS = []
def createMem(recursos, constantes):
    memFunc = [tipos(), tipos(), tipos()]
    contador = 0
    print(recursos)
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
        if (i >= dirs[4].limIIntConst and i <= dirs[4].limSIntConst):
            memFunc[2].int.insert(i-dirs[4].limIIntConst, 0)
        elif (i >= dirs[4].limIFloatConst and i <= dirs[4].limSFloatConst):
            memFunc[2].float.insert(i-dirs[4].limIFloatConst, 0)
        elif (i >= dirs[4].limIStringConst and i <= dirs[4].limSStringConst):
            memFunc[2].string.insert(i-dirs[4].limIStringConst, 0)
        elif (i >= dirs[4].limIBoolConst and i <= dirs[4].limSBoolConst):
            memFunc[2].bool.insert(i-dirs[4].limIBoolConst, 0)
    stackS.append(memFunc)

# read dirFunc
f = open('dirF.txt','r')
dirFuncStr = f.readline()
f.close()
dirFunc = ast.literal_eval(dirFuncStr)
    
# operaciones
print("-----maquina virtual-----")
ip = 1
saveIP = ip
contParam = contFuncs()
numCuadruplos = len(codeS)
while ip < numCuadruplos:
    codigoOperacion = codeS[ip][0]
    if codigoOperacion == 'goto':
        try:
            ip = codeS[ip][3] - 1
        except:
            pass
    elif codigoOperacion == 'gotoF':    
        if (fetchDir(codeS[ip][1]) == False):
            try:
                ip = codeS[ip][3] - 1
            except:
                pass
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
        print(codeS[ip][1])
        print(fetchDir(codeS[ip][1]))
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
            print("Error: Type mismatch of input and variable in read()")
            exit(1)
    elif codigoOperacion == 'verifica':
        if (fetchDir(codeS[ip][1]) < codeS[ip][2] or fetchDir(codeS[ip][1]) > codeS[ip][3]):
            print('Error: array index out of bounds')
            exit(1)
    elif codigoOperacion == 'era':
        recursos = dirFunc.get(codeS[ip][3])
        createMem(recursos[0], recursos[1])
    elif codigoOperacion == 'gosub':
        print(stackS)
        saveIP = ip
        ip = codeS[ip][3] - 1
        contParam.contFunc += 1
    elif codigoOperacion == 'endfunc':
        ip = saveIP
        stackS.pop()
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


    
    """ faltan:
    elif op == "return":
        self.generarCuadruplo('return', '', '', res)
    """