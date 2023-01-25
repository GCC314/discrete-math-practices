from graphviz import Digraph

def Save_NFA_Graph(nfa):
    G = Digraph('NFA', format="png")
    for u in range(len(nfa)):
        if(nfa[u].fin):
            G.node(str(u), str(u), shape="doublecircle")
        else:
            G.node(str(u), str(u), shape="circle")
    for u in range(len(nfa)):
        for v in nfa[u].eps: G.edge(str(u), str(v), 'e')
        for c in nfa[u].tr:
            for v in nfa[u].tr[c]: G.edge(str(u), str(v), c)
    G.render('nfa')

def Save_DFA_Graph(dfa):
    G = Digraph('DFA', format="png")
    for u in range(len(dfa)):
        if(dfa[u].fin):
            G.node(str(u), str(u), shape="doublecircle")
        else:
            G.node(str(u), str(u), shape="circle")
    for u in range(len(dfa)):
        for c in dfa[u].tr:
            G.edge(str(u), str(dfa[u].tr[c]), c)
    G.render('dfa')