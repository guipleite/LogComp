import sys

def check(inp):
    index = 0
    if len(inp) == 1:
        return int(inp)

    for i in range(len(inp)):
        index+=1

        if i > 0 :
            if inp[i] == "+" or inp[i] == "-" :
                return(int(inp[:i]) + int(check(inp[i:])))

            else: 
                if len(inp) == index:
                        return int(inp)

inp = sys.argv[1]

def main(inp):
    for i in range(len(inp)):
        if inp[i] == " " and i>0:
            j=i

            while inp[j]== " ":
                j+=1

            if inp[j].isdigit() and inp[i-1].isdigit():
                raise Exception("Erro, verifique a exprecao")        

    inp = (inp).replace(" ", "")

    if not inp[0].isdigit() and inp[0]!="-":
        raise Exception("Erro, verifique a exprecao")        
    else:
        return check(inp)

try:
    print(main(inp))
except:
    raise Exception("Erro, verifique a exprecao")        
