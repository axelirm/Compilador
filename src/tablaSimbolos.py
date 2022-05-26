class tabla_simbolos_vars:
  def __init__(self):
    #self.nombre = nombre
    self.dict = {}

  def insertar(self, nombre, tipo, valor, dirV):
    existe = self.buscar(nombre)
    if(existe == None):
      dict2 = {nombre : [tipo, valor, dirV] }
      self.dict.update(dict2)
      return True
    else:
      return False

  def actualizar(self, nombre, tipo, valor, dirV):
    dict2 = {nombre : [tipo, valor, dirV] }
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

  def insertar(self, nombre, retorno, parametros, inicio, size, tablaVars):
    dict2 = {nombre : [retorno, parametros, inicio, size, vars, tablaVars] }
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
    

