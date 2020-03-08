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
        self.selectNext()
    
    def selectNext(self):

        if self.origin[self.positon] == " " :
            while self.positon<(len(self.origin)) and  self.origin[self.positon] == " ":
                self.positon+=1

        if self.positon==(len(self.origin)):
            self.actual = Token('' , 'EOF')
            return None
            
        if self.origin[self.positon] == "+":
            self.actual = Token('str' , '+')
            self.positon+=1

        elif self.origin[self.positon] == "-":
            self.actual = Token('str' , '-')
            self.positon+=1

        elif self.origin[self.positon].isdigit():

            num = ''
            
            while self.origin[self.positon].isdigit():
                num+=self.origin[self.positon]
                
                if self.positon==(len(self.origin)-1):
                    break
                else:
                    self.positon+=1

            self.actual = Token('int', int(num))      

        else:
           raise Exception("Erro, verifique a exprecao 1")        
        
class Parser():

    def __init__(self,tokens):
        self.tokens = tokens

    @staticmethod
    def parseExpression(tokens):

        if str(Parser.tokens.actual.tokenValue).isdigit():
            result = int(Parser.tokens.actual.tokenValue)

            Parser.tokens.selectNext()

            if str(Parser.tokens.actual.tokenValue).isdigit():
                raise Exception("Erro, verifique a exprecao 2")   

            while Parser.tokens.actual.tokenValue == "+" or Parser.tokens.actual.tokenValue == "-":

                if Parser.tokens.actual.tokenValue =="+":
                    Parser.tokens.selectNext()

                    if str(Parser.tokens.actual.tokenValue).isdigit():
                        result+=int(Parser.tokens.actual.tokenValue)
                    else: 
                         raise Exception("Erro, verifique a exprecao 3") 

                elif Parser.tokens.actual.tokenValue =="-":
                    Parser.tokens.selectNext()

                    if str(Parser.tokens.actual.tokenValue).isdigit():
                        result-=int(Parser.tokens.actual.tokenValue)
                    else: 
                        raise Exception("Erro, verifique a exprecao 4")      
                
                elif str(Parser.tokens.actual.tokenValue).isdigit():
                    raise Exception("Erro, verifique a exprecao 5")     
            
                Parser.tokens.selectNext() 

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

    # try:
    print(Parser.run(inp))
        
    # except :
    #   raise Exception("Erro, verifique a exprecao")        

if __name__ == '__main__':
    main()