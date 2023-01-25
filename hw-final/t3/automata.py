# lib for automata
import queue
language = ['a', 'b']
priority = {'|' : 1, '.' : 2, '*' : 3, '(' : 0, ')' : 0}

class InputException(Exception):
    def __init__(self, _type, _oth=None):
        self.type, self.oth = _type, _oth
    def __str__(self):
        if self.type == "char": return "非法字符: \"%c\"" % (self.oth)
        if self.type == "invalid": return "非法输入"
        if self.type == "bracket": return "非法括号层次"
        return "?"      # Control should never reaches here

class NFANode:
    def __init__(self):
        self.tr, self.eps, self.fin = {}, [], False
    def __str__(self):
        ret = "eps -> %s\n" % (str(self.eps), )
        for c in self.tr: ret += "%c -> %s\n" % (c, str(self.tr[c]))
        if self.fin: ret += "是终止节点"
        return ret

class DFANode:
    def __init__(self, fin = False):
        self.tr, self.fin = {}, fin
    def __str__(self):
        ret = ""
        for c in self.tr: ret += "%c -> %d\n" % (c, self.tr[c])
        if self.fin: ret += "是终止节点"
        return ret

def Regex2NFA(reg):
    # check alphabet
    for c in reg:
        if not c in language + ['*', '|', '(', ')']:
            raise InputException('char', c)

    # add concate char '.'
    reg2 = ""
    for i in range(len(reg) - 1):
        reg2 += reg[i]
        c0, c1 = reg[i], reg[i + 1]
        if c0 != '(' and c1 != ')' and c0 != '|' and c1 != '|' and c1 != '*':
            reg2 += '.'
    reg2 += reg[-1]

    # convert to postfix
    pfix = ""
    sop = []
    for c in reg2:
        if c in language: pfix += c
        elif c == '(': sop.append('(')
        elif c == ')':
            while len(sop) != 0 and sop[-1] != '(': pfix += sop.pop()
            if len(sop) == 0:
                raise InputException('bracket')
            sop.pop()
        else:
            while len(sop) != 0:
                if priority[sop[-1]] >= priority[c]: pfix += sop.pop()
                else: break
            sop.append(c)
    while len(sop) != 0: pfix += sop.pop()

    # postfix to nfa
    NFAList = []
    sauto = []
    for c in pfix:
        if c in language:
            # Character
            NFAList.append(NFANode())
            NFAList.append(NFANode())
            NFAList[-2].tr[c] = [len(NFAList) - 1]
            sauto.append(len(NFAList) - 2)
            sauto.append(len(NFAList) - 1)
        elif c == '.':
            # Concate
            if len(sauto) < 4: raise InputException("invalid")
            d,c,b,a = sauto.pop(),sauto.pop(),sauto.pop(),sauto.pop()
            NFAList[b].eps.append(c)
            sauto.append(a)
            sauto.append(d)
        elif c == '|':
            # Union
            if len(sauto) < 4: raise InputException("invalid")
            NFAList.append(NFANode())
            NFAList.append(NFANode())
            d,c,b,a = sauto.pop(),sauto.pop(),sauto.pop(),sauto.pop()
            NFAList[-2].eps.append(a)
            NFAList[-2].eps.append(c)
            NFAList[b].eps.append(len(NFAList) - 1)
            NFAList[d].eps.append(len(NFAList) - 1)
            sauto.append(len(NFAList) - 2)
            sauto.append(len(NFAList) - 1)
        else:
            # Star
            if len(sauto) < 2: raise InputException("invalid")
            NFAList.append(NFANode())
            NFAList.append(NFANode())
            b,a = sauto.pop(),sauto.pop()
            NFAList[-2].eps.append(a)
            NFAList[-2].eps.append(len(NFAList) - 1)
            NFAList[b].eps.append(a)
            NFAList[b].eps.append(len(NFAList) - 1)
            sauto.append(len(NFAList) - 2)
            sauto.append(len(NFAList) - 1)
    
    if len(sauto) != 2: raise InputException("invalid")

    NFAList[sauto[-1]].fin = True
    # return (NFA, finalstate, startstate)
    return (NFAList, sauto.pop(), sauto.pop())

def NFA2DFA(NFA, start):
    def EClosure(T):
        Te = set()
        Q = queue.Queue()
        for u in T: Q.put(u)
        while not Q.empty():
            u = Q.get()
            Te.add(u)
            for v in NFA[u].eps:
                if not v in Te: Q.put(v)
        return Te
    
    def SFin(T):
        return any(NFA[u].fin for u in T)
    
    def Move(T, c):
        U = set()
        for u in T:
            if not c in NFA[u].tr: continue
            for v in NFA[u].tr[c]: U.add(v)
        return U

    DSList = []
    def getDId(U):
        for i in range(len(DSList)):
            if(U == DSList[i]): return i
        return -1

    T0 = EClosure([start])
    DSList.append(T0)
    DFAList = []
    awaitSet = [0]
    DFAList.append(DFANode(SFin(T0)))
    while len(awaitSet) != 0:
        t = awaitSet.pop()
        for c in language:
            U = EClosure(Move(DSList[t], c))
            if len(U) == 0: continue
            if not U in DSList:
                DSList.append(U)
                awaitSet.append(len(DFAList))
                DFAList.append(DFANode(SFin(U)))
            DFAList[t].tr[c] = getDId(U)
    return DFAList

def DFAMatch(DFA, s, verbose = True):
    for c in s:
        if not c in language:
            raise InputException("char", c)
    u = 0
    output = "转移过程表:\n"
    for c in s:
        if not c in DFA[u].tr:
            output += "状态 %d 无可用转移" % (u, )
            return False, output
        v = DFA[u].tr[c]
        output += "%d   == %c ==>   %d\n" % (u, c, v)
        u = v
    if verbose: print(output)
    return DFA[u].fin, output