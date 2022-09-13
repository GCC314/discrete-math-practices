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

dic = {}

precedence = (
    ('left', 'IFF', 'IFTHEN'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT')
)

def p_expression_var(p):
    'expression : VAR'
    p[0] = ('v', p[1])

def p_expression_true(p):
    'expression : TRUE'
    p[0] = ('i', 1)

def p_expression_false(p):
    'expression : FALSE'
    p[0] = ('i', 0)

def p_expression_brackets(p):
    'expression : LBRAC expression RBRAC'
    p[0] = p[2]

def p_expression_not(p):
    'expression : NOT expression'
    if(p[2][0] == 'i'): p[0] = ('i', 1 - p[2][1])
    else: p[0] = ('!', p[2])

def p_expression_and(p):
    'expression : expression AND expression'
    if(p[1][0] == 'i' and p[3][0] == 'i'):
        if(p[1][1] == 1 and p[3][1] == 1): p[0] = ('i', 1)
        else: p[0] = ('i', 0)
    else: p[0] = ('&', p[1], p[3])

def p_expression_or(p):
    'expression : expression OR expression'
    if(p[1][0] == 'i' and p[3][0] == 'i'):
        if(p[1][1] == 0 and p[3][1] == 0): p[0] = ('i', 0)
        else: p[0] = ('i', 1)
    else: p[0] = ('|', p[1], p[3])

def p_expression_ifthen(p):
    'expression : expression IFTHEN expression'
    if(p[1][0] == 'i' and p[3][0] == 'i'):
        if(p[1][1] == 0 and p[3][1] == 1): p[0] = ('i', 0)
        else: p[0] = ('i', 1)
    else: p[0] = ('>', p[1], p[3])

def p_expression_iff(p):
    'expression : expression IFF expression'
    if(p[1][0] == 'i' and p[3][0] == 'i'):
        if(p[1][1] == p[3][1]): p[0] = ('i', 1)
        else: p[0] = ('i', 0)
    else: p[0] = ('~', p[1], p[3])

def p_error(p):
    errorStr = "syntax error : '%s' " % (p, )
    raise Exception(errorStr)

lexer = lex.lex()
parser = yacc.yacc()

def Parse(expr):
    lexer.input(expr)
    return list(set([tok.value for tok in lexer if tok.type == 'VAR']))

def Generate_AST(expr):
    return parser.parse(expr, lexer = lexer)

vdic = {}

def eval(anode):
    global vdic
    if(anode[0] == 'i'):
        return anode[1]
    if(anode[0] == 'v'):
        return vdic[anode[1]]
    if(anode[0] == '!'):
        return 1 - eval(anode[1])
    if(anode[0] == '&'):
        p1, p2 = eval(anode[1]), eval(anode[2])
        if(p1 == 1 and p2 == 1): return 1
        else: return 0
    if(anode[0] == '|'):
        p1, p2 = eval(anode[1]), eval(anode[2])
        if(p1 == 0 and p2 == 0): return 0
        else: return 1
    if(anode[0] == '>'):
        p1, p2 = eval(anode[1]), eval(anode[2])
        if(p1 == 1 and p2 == 0): return 0
        else: return 1
    if(anode[0] == '~'):
        p1, p2 = eval(anode[1]), eval(anode[2])
        if(p1 == p2): return 1
        else: return 0
    return 0    # control never reaches here

def Eval_AST(ast, valDict):
    global vdic
    vdic = valDict
    return eval(ast)
