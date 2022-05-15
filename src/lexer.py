import ply.lex as lex

tokens = (
    'ID', 'CTEI', 'CTEF', 'CTESTR', 'CTEB',
    'INT', 'FLOAT', 'STRING', 'BOOL', 'VOID',
    'IF', 'ELSE', 'FROM', 'TO', 'WHILE', 'DO',
    'CLASS', 'RETURN', 'WRITE', 'READ', 'VAR',
    'MAIN', 'FUNCTION', 'PROGRAM', 'ATTRIBUTES',
    'METHODS', 'INHERITS', 'LPAR', 'RPAR', 'LCBRAC',
    'RCBRAC', 'LSBRAC', 'RSBRAC', 'SEMICOLON',
    'COLON', 'COMMA', 'DOT', 'LT', 'GT', 'PLUS',
    'MINUS', 'MULT', 'DIV', 'AND', 'OR', 'COMP',
    'NOTEQ', 'EQ'
    )

# Tokens
t_LPAR      =   r'\('
t_RPAR      =   r'\)'
t_LCBRAC    =   r'\{'
t_RCBRAC    =   r'\}'
t_LSBRAC    =   r'\['
t_RSBRAC    =   r'\]'
t_SEMICOLON =   r'\;'
t_COLON     =   r'\:'
t_COMMA     =   r'\,'
t_DOT       =   r'\.'
t_LT        =   r'\<'
t_GT        =   r'\>'
t_PLUS      =   r'\+'
t_MINUS     =   r'\-'
t_MULT      =   r'\*'
t_DIV       =   r'\/'
t_AND       =   r'\&\&'
t_OR        =   r'\|\|'
t_COMP      =   r'\=\='
t_NOTEQ     =   r'\!\='
t_EQ        =   r'\='
t_CTESTR    =   r'["].*?["]'
t_ignore    =   " \t"

keywords = {
    'int'           :   'INT',
    'float'         :   'FLOAT',
    'string'        :   'STRING',
    'bool'          :   'BOOL',
    'void'          :   'VOID',
    'if'            :   'IF',
    'else'          :   'ELSE',
    'from'          :   'FROM',
    'to'            :   'TO',
    'while'         :   'WHILE',
    'do'            :   'DO',
    'class'         :   'CLASS',
    'return'        :   'RETURN',
    'write'         :   'WRITE',
    'read'          :   'READ',
    'var'           :   'VAR',
    'main'          :   'MAIN',
    'function'      :   'FUNCTION',
    'program'       :   'PROGRAM',
    'attributes'    :   'ATTRIBUTES',
    'methods'       :   'METHODS',
    'inherits'      :   'INHERITS'
}

def t_CTEB(t):
    r'([Tt][Rr][Uu][Ee]|[Ff][Aa][Ll][Ss][Ee])'
    return t
    
def t_ID(t):
    r'[a-zA-Z]([a-zA-Z0-9_])*'
    t.type = keywords.get(t.value, 'ID')
    return t

def t_CTEF(t):
    r'\-?[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t
  
def t_CTEI(t):
    r'\-?[0-9]+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Error lexico \"", t.value[0], "\" en la linea ", t.lineno)
    exit(1)

lex.lex()