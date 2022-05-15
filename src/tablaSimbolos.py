class tabla_simbolos_vars:
  def __init__(self):
    #self.nombre = nombre
    self.dict = {}

  def insertar(self, nombre, tipo, valor):
    dict2 = {nombre : [tipo, valor] }
    self.dict.update(dict2)

  def buscar(self, nombre):
    valores = self.dict.get(nombre)
    return valores

class tabla_simbolos_funcs:
  def __init__(self):
    self.dict = {}

  def insertar(self, nombre, retorno, parametros, inicio, size, vars):
    dict2 = {nombre : [retorno, parametros, inicio, size, vars] }
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

