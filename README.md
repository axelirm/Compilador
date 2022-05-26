# Lenguaje Team++

_El proyecto consiste en implementar un lenguaje de programación orientado
a objetos, que tenga mecanismos que soporten la definición y manipulación
de clases, sus atributos, métodos y herencia simple._

## Avances hasta el momento

_Lo que se tiene hasta el momento son el lexer y parser para identificar
que el léxico y la sintaxis de un programa sean válidos. Se tiene especificada
la semántica para todos los diagramas. También se implementó el cubo semántico.
Se creó la clase general para generar cuadruplos y ya se generan los cuadruplos
para los condicionales, ciclos, expresiones, imprimir y leer. 
Se estan agregando las direcciones virtuales a las variables, constantes, temporales, etc. 
Se agregó el goto
al main, cuadruplos de funciones, llamadas y se comenzaron los de clases._

## Comenzando 🚀

_Para poder correr el programa se necesita correr el siguiente comando:_

```
python3 parser.py ../test/archivo1.txt
```
_Se requiere tener instalado numpy y ply, lo cual se puede realizar con los siguientes comandos:_

```
pip install numpy
pip install ply
```

### Pre-requisitos 📋

_Para hacer uso de los programas se necesita tener instalado python3. Para verificar la version
que tiene utilice el siguiente comando:_

```
python --version
```

## Construido con 🛠️

* [PLY](https://www.dabeaz.com/ply/) - Implementación de herramientas yacc y lex

## Autores ✒️

* **Axel Rodríguez** - *Documentación y programación* -
* **Carolina Medina** - *Documentación y programación* - 

