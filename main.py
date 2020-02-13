import sys

inp = (sys.argv[1]).replace(" ", "")

def check(inp, first):
    plus = False
    minus = False
    print(first)
    for i in range(len(inp)):
        if inp[i]=="+" or inp[i]=="-":

            if inp[i]=="+":
                plus = True
                minus = False
                
            if inp[i]=="-":
                minus = True
                plus = False
        
        if minus ==  True:
            return(int(inp[:i])-int(inp[i+1:]))

        if plus == True:
            return(int(inp[:i])+int(inp[i+1:]))

        else: 
            if not first:
                return inp

            else:
                print("num")

print(check(inp,True))