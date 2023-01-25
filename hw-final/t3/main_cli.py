import automata as AT
import graph as GPH

regex = input("输入只含a,b,*,|和括号的合法正则表达式:")

nfa, ed, st = AT.Regex2NFA(regex)

print("-----------")
print("对应的NFA:")
print("初始状态", st)
print("终止状态", ed)
print("")

for i, node in enumerate(nfa):
    print("节点", i)
    print(node)

GPH.Save_NFA_Graph(nfa)
print("图像导出至 nfa.png")

dfa = AT.NFA2DFA(nfa, st)

print("-----------")
print("对应的DFA:")
print("初始状态", 0)
print("终止状态", [u for u in range(len(dfa)) if dfa[u].fin])
print("")

for i, node in enumerate(dfa):
    print("节点", i)
    print(node)

GPH.Save_DFA_Graph(dfa)
print("图像导出至 dfa.png")
print("")

s = input("输入匹配字符串:")
fin, output = AT.DFAMatch(dfa, s)
print("匹配成功" if fin else "匹配失败")