import sys

inp = sys.argv[1]

def check(inp):
    for i in range(len(inp)):
        if inp[i] == " " and i>0:
            j=i

            while inp[j]==" ":
                j+=1

            if inp[j].isdigit() and inp[i-1].isdigit():
                return "Erro, verifique a exprecao"

    inp = (inp).replace(" ", "")
    index = 0

    for i in range(len(inp)):
        index+=1

        if i > 0 :
            if inp[i] == "+" or inp[i] == "-" :
              
                if inp[i] == "+":
                    return(int(inp[:i]) + int(check(inp[i:])))
    
                if inp[i] == "-":
                    return(int(inp[:i]) - int(check(inp[i:])))

            else: 
                if len(inp) == index:
                        return int(inp)
                        
try:
    print(check(inp))
except:
    print("Erro, verifique a exprecao")