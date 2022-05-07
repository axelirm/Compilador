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
  def __init__(self, nombre, parent):
    self.nombre = nombre
    self.dict = {}
    self.parent = parent #
    self.children = {} #

  def insertar(self, nombre, tipo, variables):
    dict2 = {nombre : [tipo, variables] }
    dict.update(dict2)

  def buscar(self, nombre):
    valores = dict[nombre]
    return valores

