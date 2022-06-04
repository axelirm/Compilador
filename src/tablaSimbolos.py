class tabla_simbolos_vars:
  def __init__(self):
    #self.nombre = nombre
    self.dict = {}

  def insertar(self, nombre, tipo, valor, dirV, dim):
    existe = self.buscar(nombre)
    if(existe == None):
      dict2 = {nombre : [tipo, valor, dirV, dim] }
      self.dict.update(dict2)
      return True
    else:
      return False

  def actualizar(self, nombre, tipo, valor, dirV, dim):
    dict2 = {nombre : [tipo, valor, dirV, dim] }
    self.dict.update(dict2)

  def buscar(self, nombre):
    valores = self.dict.get(nombre)
    return valores

  def inversa(self):
    dictAux = dict(reversed(list(self.dict.items())))
    self.dict = dictAux

class tabla_simbolos_funcs:
  def __init__(self):
    self.dict = {}
    
  def insertar(self, nombre, retorno, parametros, inicio, tablaVars, intVars, floatVars, stringVars, boolVars, intTemp, floatTemp, strTemp, boolTemp, tablaConst):
    dict2 = {nombre : [retorno, parametros, inicio, tablaVars, intVars, floatVars, stringVars, boolVars, intTemp, floatTemp, strTemp, boolTemp, tablaConst] }
    self.dict.update(dict2)

  def buscar(self, nombre):
    valores = self.dict.get(nombre)
    return valores

class tabla_simbolos_clases:
  def __init__(self):
    self.dict = {}

  def insertar(self, nombre, vars, funcs, padre, size, inicio):
    dict2 = {nombre : [vars, funcs, padre, size, inicio] }
    self.dict.update(dict2)

  def buscar(self, nombre):
    valores = self.dict.get(nombre)
    return valores

  def herencia(self):
    pass

class tabla_memoria_vars:
  def __init__(self):
    self.dict = {}

  def buscar(self, direccion):
    valor = self.dict.get(direccion)
    return valor

  # usar esta funcion para actualizar valor
  def insertar(self, dirVir, valor):
    dict2 = {dirVir : valor}
    self.dict.update(dict2)
    
class arreglos:
    def __init__(self):
        self.limInfD1 = 0
        self.limSupD1 = 0
        self.m1 = 1
        self.limInfD2 = 0
        self.limSupD2 = 0
    
    def set(self, array):
        self.limInfD1 = array.limInfD1
        self.limSupD1 = array.limSupD1
        self.m1 = array.m1
        self.limInfD2 = array.limInfD1
        self.limSupD2 = array.limSupD2
        