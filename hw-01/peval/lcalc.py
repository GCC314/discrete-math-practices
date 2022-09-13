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


precedence = (
    ('left', 'IFF', 'IFTHEN'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT')
)

def p_expression_var(p):
    'expression : VAR'
    p[0] = 'Dic[\'' + p[1] + '\']'

def p_expression_true(p):
    'expression : TRUE'
    p[0] = 'True'

def p_expression_false(p):
    'expression : FALSE'
    p[0] = 'False'

def p_expression_brackets(p):
    'expression : LBRAC expression RBRAC'
    p[0] = '( ' + p[2] + ' )'

def p_expression_not(p):
    'expression : NOT expression'
    p[0] = '( not ' + p[2] + ' )'

def p_expression_and(p):
    'expression : expression AND expression'
    p[0] = '( ' + p[1] + ' and ' + p[3] + ' )'

def p_expression_or(p):
    'expression : expression OR expression'
    p[0] = '( ' + p[1] + ' or ' + p[3] + ' )'

def p_expression_ifthen(p):
    'expression : expression IFTHEN expression'
    p[0] = '( not ' + p[1] + ' and ' + p[3] + ' )'

def p_expression_iff(p):
    'expression : expression IFF expression'
    p[0] = '( ' + p[1] + ' == ' + p[3] + ' )'

def p_error(p):
    errorStr = "syntax error : '%s' " % (p, )
    raise Exception(errorStr)

lexer = lex.lex()
parser = yacc.yacc()

def Parse(expr):
    lexer.input(expr)
    return list(set([tok.value for tok in lexer if tok.type == 'VAR']))

def Generate_PyCode(expr):
    return parser.parse(expr, lexer = lexer)

def Eval_PyCode(code, Dic):
    if eval(code): return 1
    else: return 0
