import dirVir as dir

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

dirs = [dir.varGlobal(), dir.varTemps(), dir.varTempsPointer(), dir.varConst()]
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
        elif (dir >= dirs[table].limIObjeto and dir <= dirs[table].limSObjeto):
            dataS[table].obj.insert(dir-dirs[table].limIObjeto, value)
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

# regresa valor, faltan los objetos
def fetchDir(dir):
    for i in range(4):
        if (dir >= dirs[i].limIInt and dir <= dirs[i].limSInt):
            if dir > 29500:
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
    for i in range(4):
        if (dir >= dirs[i].limIInt and dir <= dirs[i].limSInt):
            if (dir > 29500 and op == '='):
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

stackS = []
locales = dir.varLocal()
def createMem(recursos, constantes):
    memFunc = []
    for i in recursos:
        try:
            auxList = [None] * int(i)
            memFunc.append(auxList)
        except:
            pass
    memFunc.append(tipos())
    for i in constantes:
        pass
    stackS.append(memFunc)
    memFunc = []
    print(stackS)
        
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
        print(codeS[ip][3])
        print(codeS[ip][1])
        stri = str(codeS[ip][3]).replace('3', '12')
        createMem(stri, codeS[ip][1])
    elif codigoOperacion == 'gosub':
        print(stackS)
        saveIP = ip
        ip = codeS[ip][3] - 1
        contParam.contFunc += 1
    elif codigoOperacion == 'endfunc': # falta eliminar memoria
        ip = saveIP
    elif codigoOperacion == 'param':
        tipo = fetchType(codeS[ip][1])
        if tipo == 'int':
            stackS[contParam.contFunc][0][contParam.contInt] = fetchDir(codeS[ip][1])
            contParam.contInt += 1
        elif tipo == 'float':
            stackS[contParam.contFunc][1][contParam.contFloat] = fetchDir(codeS[ip][1])
            contParam.contFloat += 1
        elif tipo == 'str':
            stackS[contParam.contFunc][2][contParam.contStr] = fetchDir(codeS[ip][1])
            contParam.contStr += 1
        elif tipo == 'bool':
            stackS[contParam.contFunc][3][contParam.contBool] = fetchDir(codeS[ip][1])
            contParam.contBool += 1
            
    ip = ip + 1


    
    """ faltan:
    elif op == "return":
        self.generarCuadruplo('return', '', '', res)
    """