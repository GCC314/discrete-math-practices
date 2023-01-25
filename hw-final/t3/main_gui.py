import tkinter as tk
import tkinter.messagebox
import automata as AT
import graph as GPH

class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("将正则表达式转化为DFA")
        self.window.geometry("800x600")
        self.window.resizable(width=False, height=False)
        parentFrame = tk.Frame(self.window, width=780, height=580)
        parentFrame.grid(stick = tk.E+tk.W+tk.N+tk.S)

        regexFrame = tk.Frame(parentFrame)
        regexLabel = tk.Label(regexFrame, text="输入只含a,b,*,|和括号的合法正则表达式:")
        self.regexVar = tk.StringVar()
        regexField = tk.Entry(regexFrame, width=50, textvariable=self.regexVar)
        buildBtn = tk.Button(regexFrame, text="构造", width=10, command=self.handleBuildBtn)
        regexLabel.grid(row=0, column=0, sticky=tk.W)
        regexField.grid(row=1, column=0, sticky=tk.W)
        buildBtn.grid(row=1, column=1, padx=5)
        regexFrame.grid(row=0, column=0, sticky=tk.W, padx=(50,0))

        testFrame = tk.Frame(parentFrame)
        testLabel = tk.Label(testFrame, text="输入测试字符串:")
        self.testVar = tk.StringVar()
        testField = tk.Entry(testFrame, width=50, textvariable=self.testVar)
        self.testBtn = tk.Button(testFrame, text="测试", width=10, command=self.handleTestBtn)
        testLabel.grid(row=0, column=0, sticky=tk.W)
        testField.grid(row=1, column=0, sticky=tk.W)
        self.testBtn.grid(row=1, column=1, padx=5)
        testFrame.grid(row=1, column=0, sticky=tk.W, padx=(50,0))

        canvasFrame = tk.Frame(parentFrame, height=100, width=100)
        self.myCanvas = tk.Canvas(canvasFrame, bg="#FFFFFF", width=740, height=400, scrollregion=(0,0,740,400))
        hbar = tk.Scrollbar(canvasFrame, orient=tk.HORIZONTAL)
        hbar.pack(side=tk.BOTTOM, fill=tk.X)
        hbar.config(command=self.myCanvas.xview)
        vbar = tk.Scrollbar(canvasFrame, orient=tk.VERTICAL)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        vbar.config(command=self.myCanvas.yview)
        self.myCanvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.myCanvas.pack()
        canvasFrame.grid(row=2, column=0, sticky=tk.W+tk.S+tk.E+tk.N, padx=(30,0), pady=10)

        self.testBtn.config(state=tk.DISABLED)

    def handleBuildBtn(self):
        self.myCanvas.delete(tk.ALL)
        self.imgCache = []
        self.yPtr = 10
        self.xMax = 780
        self.yMax = 580
        
        try:
            self.nfa, self.ed, self.st = AT.Regex2NFA(self.regexVar.get())
        except AT.InputException as err:
            tkinter.messagebox.showerror(title="错误", message=str(err))
            return
        
        self.appendText("对应的NFA:")
        self.appendText("初始状态: %d" % (self.st, ))
        self.appendText("终止状态: %d" % (self.ed, ))
        self.appendText("")
        for i, node in enumerate(self.nfa):
            self.appendText("节点 %d" % (i, ))
            self.appendText(str(node))
        GPH.Save_NFA_Graph(self.nfa)
        self.appendText("NFA 图像:")
        self.appendImage("./nfa.png")

        try:
            self.dfa = AT.NFA2DFA(self.nfa, self.st)
        except AT.InputException as err:
            tkinter.messagebox.showerror(title="错误", message=str(err))
            return

        self.appendText("对应的DFA:")
        self.appendText("初始状态: 0")
        endSet = [u for u in range(len(self.dfa)) if self.dfa[u].fin]
        self.appendText("终止状态: " + str(endSet))
        self.appendText("")
        for i, node in enumerate(self.dfa):
            self.appendText("节点 %d" % (i, ))
            self.appendText(str(node))
        GPH.Save_DFA_Graph(self.dfa)
        self.appendText("DFA 图像:")
        self.appendImage("./dfa.png")

        self.testBtn.config(state=tk.NORMAL)

    def handleTestBtn(self):
        try:
            fin, output = AT.DFAMatch(self.dfa, self.testVar.get(), verbose=False)
            self.appendText("测试字串: " + self.testVar.get())
            self.appendText("匹配成功!" if fin else "匹配失败!")
            self.appendText(output)
            if fin: tkinter.messagebox.showinfo(title="成功!", message="匹配成功!")
            else: tkinter.messagebox.showinfo(title="失败!", message="匹配失败!")
            self.myCanvas.yview_moveto(1.0)
            self.myCanvas.config(scrollregion=(0,0,self.xMax,self.yMax))
        except AT.InputException as err:
            tkinter.messagebox.showerror(title="错误", message=str(err))
            return

    def appendImage(self, fname):
        self.imgCache.append(tk.PhotoImage(file=fname))
        iObj = self.myCanvas.create_image((10, self.yPtr), image=self.imgCache[-1], anchor="nw")
        x1, y1, x2, y2 = self.myCanvas.bbox(iObj)
        self.yPtr = y2 + 5
        self.xMax = max(x2 + 10, self.xMax)
        self.yMax = max(y2 + 10, self.yMax)
        self.myCanvas.config(scrollregion=(0,0,self.xMax,self.yMax))

    def appendText(self, text):
        tObj = self.myCanvas.create_text((10, self.yPtr), text=text, anchor="nw")
        x1, y1, x2, y2 = self.myCanvas.bbox(tObj)
        self.yPtr = y2 + 5
        self.xMax = max(x2 + 10, self.xMax)
        self.yMax = max(y2 + 10, self.yMax)
        self.myCanvas.config(scrollregion=(0,0,self.xMax,self.yMax))

    def Run(self):
        self.window.mainloop()

if __name__ == "__main__":
    gui = GUI()
    gui.Run()