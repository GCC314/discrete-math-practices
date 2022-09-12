import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'TRUE',
    'FALSE',
    'NOT',
    'AND',
    'OR',
    'IFTHEN',
    'IFF',
    'LBRAC',
    'RBRAC',
    'VAR'
)

t_TRUE      = r'1'
t_FALSE     = r'0'
t_NOT       = r'!'
t_AND       = r'&'
t_OR        = r'\|'
t_IFTHEN    = r'>'
t_IFF       = r'~'
t_LBRAC     = r'\('
t_RBRAC     = r'\)'

def t_VAR(t):
    r'[a-zA-Z]'
    return t

t_ignore = ' \t'

def t_error(t):
    errorStr = "Invalid symbol \'%s\'" % (t.value[0], )
    raise Exception(errorStr)

data = input()
lexer = lex.lex()
lexer.input(data)

dic = {'a' : '1','b' : '0','c' : '1'}


precedence = (
    ('left', 'IFF', 'IFTHEN'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT')
)

def p_expression_var(p):
    'expression : VAR'
    p[0] = dic[p[1]]

def p_expression_true(p):
    'expression : TRUE'
    p[0] = p[1]

def p_expression_false(p):
    'expression : FALSE'
    p[0] = p[1]

def p_expression_brackets(p):
    'expression : LBRAC expression RBRAC'
    p[0] = p[2]

def p_expression_not(p):
    'expression : NOT expression'
    if(p[2] == '1'): p[0] = '0'
    else: p[0] = '1'

def p_expression_and(p):
    'expression : expression AND expression'
    if(p[1] == '1' and p[3] == '1'): p[0] = '1'
    else: p[0] = '0'

def p_expression_or(p):
    'expression : expression OR expression'
    if(p[1] == '0' and p[3] == '0'): p[0] = '0'
    else: p[0] = '1'

def p_expression_ifthen(p):
    'expression : expression IFTHEN expression'
    if(p[1] == '0' and p[3] == '1'): p[0] = '0'
    else: p[0] = '1'

def p_expression_iff(p):
    'expression : expression IFF expression'
    if(p[1] != p[3]): p[0] = '0'
    else: p[0] = '1'

def p_error(p):
    errorStr = "syntax error : '%s' " % (p, )
    raise Exception(errorStr)

parser = yacc.yacc()
res = parser.parse(data, lexer = lexer)
print(res)