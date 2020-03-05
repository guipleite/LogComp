import sys

class Token():

    def __init__(self,tokenType,tokenValue):
        self.tokenType = tokenType
        self.tokenValue = tokenValue

class Tokenizer():

    def __init__(self,origin):
        self.origin = origin
        self.positon = 0
        self.actual = None
        #self.selectNext()
    
    def selectNext(self,tokens):

        if self.positon==(len(self.origin)-1):
            self.actual = Token('','EOF')
            return None

        if self.origin[self.positon] == " " and self.positon<(len(self.origin)):
            while self.origin[self.positon] == " " and self.positon<(len(self.origin)-1):
                print(self.positon)
                self.positon+=1

        if self.origin[self.positon] == "+":
            self.actual = "+"
            self.positon+=1

        elif self.origin[self.positon] == "-":
            self.actual = "-"
            self.positon+=1

        elif self.origin[self.positon].isdigit():
            num = ''
            
            while self.origin[self.positon].isdigit():
                num+=self.origin[self.positon]
                
                if self.positon==(len(self.origin)-1):
                    break
                else:
                    self.positon+=1

            self.actual = int(num)
            
        else:
            print("asdas",self.origin[self.positon], "asda")
            raise Exception("Erro, verifique a exprecao 1")        

class Parser():

    def __init__(self,tokens):
        self.tokens = tokens

    @staticmethod
    def parseExpression(tokens):

        Parser.tokens.selectNext(tokens)
        print("1-     ",Parser.tokens.actual)
        if str(Parser.tokens.actual).isdigit():
            result = int(Parser.tokens.actual)

            Parser.tokens.selectNext(tokens)

            if str(Parser.tokens.actual).isdigit():
                raise Exception("Erro, verifique a exprecao 2")   

            while Parser.tokens.actual == "+" or Parser.tokens.actual == "-":
                print("2-      ",Parser.tokens.actual)    

                if Parser.tokens.actual =="+":
                    Parser.tokens.selectNext(tokens)
                    print("3-        ",Parser.tokens.actual)

                    if str(Parser.tokens.actual).isdigit():
                        result+=int(Parser.tokens.actual)
                    else: 
                         raise Exception("Erro, verifique a exprecao 3") 
                    print("result",result)       

                elif Parser.tokens.actual =="-":
                    Parser.tokens.selectNext(tokens)

                    if str(Parser.tokens.actual).isdigit():
                        result-=int(Parser.tokens.actual)
                    else: 
                        raise Exception("Erro, verifique a exprecao 4")      
                
                elif Parser.tokens.actual.isdigit():##
                    raise Exception("Erro, verifique a exprecao 5")     
            
                Parser.tokens.selectNext(tokens) ##

            return result

        else: 
            raise Exception("Erro, verifique a exprecao")        

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        parsed = Parser.parseExpression(Parser.tokens)

        return parsed


def main():

    inp = sys.argv[1]

    #try:
    print(Parser.run(inp))
        
    #except :
    #   raise Exception("Erro, verifique a exprecao")        


if __name__ == '__main__':
    main()