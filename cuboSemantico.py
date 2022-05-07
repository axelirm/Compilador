import numpy as np

# Tipo de dato
# int      --> 0
# float    --> 1
# string   --> 2
# bool     --> 3

# Operandos
# +        --> 0
# -        --> 1
# *        --> 2
# /        --> 3
# >        --> 4
# <        --> 5
# ==       --> 6
# !=       --> 7
# &&       --> 8
# ||       --> 9
# =        --> 10

#cubo[tipo1, tipo2, operador] = tipo
#      int     int       +   --> int
# si es un error entonces en la casilla se encontrara
# un cero

class CuboSemantico:
  def __init__(self):
    self.cubo = np.full((4,4,11), 11)
    # suma de enteros
    self.cubo[0,0,0] = 0
    self.cubo[0,1,0] = 1
    # resta de enteros
    self.cubo[0,0,1] = 0
    self.cubo[0,1,1] = 1
    # multiplicacion
    self.cubo[0,0,2] = 0
    self.cubo[0,1,2] = 1
    # division de enteros
    self.cubo[0,0,3] = 0
    self.cubo[0,1,3] = 1
    # mayor que de enteros
    self.cubo[0,0,4] = 3
    # menor que de enteros
    self.cubo[0,0,5] = 3
    # igual que de enteros
    self.cubo[0,0,6] = 3
    # diferente que de enteros
    self.cubo[0,0,7] = 3
    # and de enteros
    self.cubo[0,0,8] = 3
    # or de enteros
    self.cubo[0,0,9] = 3
    # eq de enteros
    self.cubo[0,0,10] = 0
    self.cubo[0,1,10] = 1
    
    # suma de flotantes
    self.cubo[1,1,0] = 1
    self.cubo[1,0,0] = 1
    # resta de flotantes
    self.cubo[0,0,1] = 1
    self.cubo[1,0,1] = 1
    # multiplicacion
    self.cubo[0,0,2] = 1
    self.cubo[1,0,2] = 1
    # division de flotantes
    self.cubo[0,0,3] = 1
    self.cubo[1,0,3] = 1
    # mayor que de flotantes
    self.cubo[0,0,4] = 3
    # menor que de flotantes
    self.cubo[0,0,5] = 3
    # igual que de flotantes
    self.cubo[0,0,6] = 3
    # diferente que de flotantes
    self.cubo[0,0,7] = 3
    # and de flotantes
    self.cubo[0,0,8] = 3
    # or de flotantes
    self.cubo[0,0,9] = 3
    # eq de flotantes
    self.cubo[0,0,10] = 1
    self.cubo[1,0,10] = 1

    
    # igual que de string
    self.cubo[2,2,6] = 3
    # diferente que de string
    self.cubo[2,2,7] = 3
    # eq de string
    self.cubo[2,2,10] = 2

    # mayor que de bool
    self.cubo[3,3,4] = 3
    # menor que de bool
    self.cubo[3,3,5] = 3
    # igual que de bool
    self.cubo[3,3,6] = 3
    # diferente que de bool
    self.cubo[3,3,7] = 3
    # and de bool
    self.cubo[3,3,8] = 3
    # or de bool
    self.cubo[3,3,9] = 3
    # eq de bool
    self.cubo[3,3,10] = 3

  def getTipo(self, tipo):
    if tipo == "int":
      return 0
    elif tipo == "float":
      return 1
    elif tipo == "string":
      return 2
    elif tipo == "bool":
      return 3

  def getNumeroTipo(self, tipo):
    if tipo == 0:
      return "int"
    elif tipo == 1:
      return "float"
    elif tipo == 2:
      return "string"
    elif tipo == 3:
      return "bool"

  def getOperando(self, operando):
    if operando == '+':
      return 0
    elif operando == '-':
      return 1
    elif operando == '*':
      return 2
    elif operando == '/':
      return 3
    elif operando == '>':
      return 4
    elif operando == '<':
      return 5
    elif operando == '==':
      return 6
    elif operando == '!=':
      return 7
    elif operando == '&&':
      return 8
    elif operando == '||':
      return 9
    elif operando == '=':
      return 10