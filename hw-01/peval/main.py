import lcalc

def binStringify(val,n):
    # Convert the integer number to a binary string
    ret = ""
    for i in range(n):
        ret += str((val >> i) & 1)
    return ret

if __name__ == "__main__":
    exp = input("Please input an expression: ")

    varList = sorted(lcalc.Parse(exp))
    if(len(varList) != 0):
        print("The expression got %d variable(s): " % (len(varList), ), varList)
    else:
        print("The expression got no variable.")
    
    code = lcalc.Generate_PyCode(exp)

    if(len(varList) == 0):
        print("The expression always equals to", lcalc.Eval_PyCode(code, {}))
    else:
        # Print truth table
        print("\n #### Truth Table ####")
        print("".join(varList) + "\tresult")
        satisfyAssigns = []
        for bins in range(2 ** len(varList)):
            varDict = {}
            for i in range(len(varList)):
                varDict[varList[i]] = (bins >> i) & 1
            res = lcalc.Eval_PyCode(code, varDict)
            print(binStringify(bins, len(varList)) + "\t" + str(res))
            if(res == 1):
                satisfyAssigns.append(bins)
        # Print satisfying assignments
        print("\n #### Satisfying Assignments")
        print("".join(varList))
        for bins in satisfyAssigns:
            print(binStringify(bins,len(varList)))

        