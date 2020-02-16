import sys

inp = (sys.argv[1]).replace(" ", "")

def check(inp):
    plus = False
    minus = False
    index = 0

    for i in range(len(inp)):
        index+=1

        if inp[i]=="+" or inp[i]=="-":

            if inp[i]=="+":
                plus = True
                minus = False
                
            if inp[i]=="-":
                minus = True
                plus = False


        if plus == True:
            return(int(inp[:i]) + int(check(inp[i+1:])))

        if minus ==  True:

            return(int(inp[:i]) - int(check(inp[i+1:])))

        else: 
            if len(inp)==index:
                return inp

print(check(inp))