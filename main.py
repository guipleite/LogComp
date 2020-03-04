import sys

class Token():

    def __init__(self,tokenType,tokenValue):
        self.tokenType = tokenType
        self.tokenValue = tokenValue

class Tokenizer(origin):

    def __init__(self,origin):
        self.origin = origin
        self.positon = 0
        self.actual = None
        self.selectNext()
    
    def selectNext(self,tokens):
        
        if self.origin[self.positon] == " ":
            self.positon+=1

        if self.origin[self.positon] == "+":
            self.actual = "+"

        elif self.origin[self.positon] == "-":
            self.actual = "-"

        elif self.origin[self.positon].isDigit():

            num = ''

            while self.origin[self.positon].isDigit():
                num+=self.origin[self.positon]
                self.positon+=1

            self.actual = int(num)

        else:
            raise Exception("Erro, verifique a exprecao")        

class Parser():

    def __init__(self,tokens):
        self.tokens = tokens

    @staticmethod
    def parseExpression(tokens):

        if Parser.tokens.actual.tokenType.isDigit():
            result = Parser.tokens.actual.tokenValue

            Parser.tokens.selectNext()
            
            if Parser.tokens.actual.tokenType.isDigit():
                 raise Exception("Erro, verifique a exprecao")   

            while Parser.tokens.actual.tokenType == "+" or Parser.tokens.actual.tokenType == "-":
                if Parser.tokens.actual.tokenType =="+":
                    Parser.tokens.selectNext()

                    if Parser.tokens.actual.tokenType.isDigit():
                        result+=Parser.tokens.actual.tokenValue
                    else: 
                         raise Exception("Erro, verifique a exprecao")        

                if Parser.tokens.actual.tokenType =="-":
                    Parser.tokens.actual.Tokenizer.selectNext()

                    if Parser.tokens.actual.tokenType.isDigit():
                        result-=Parser.tokens.actual.tokenValue
                    else: 
                        raise Exception("Erro, verifique a exprecao")      
                
                if Parser.tokens.actual.tokenType.isDigit():##
                    raise Exception("Erro, verifique a exprecao")     
            
                Parser.tokens.selectNext() ##

            return result

        else: 
            raise Exception("Erro, verifique a exprecao")        

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        parsed = Parser.parseExpression()

        return parsed


def main():

    inp = sys.argv[1]

    try:
        print(Parser.run(inp))
        
    except :
        raise Exception("Erro, verifique a exprecao")        


if __name__ == '__main__':
    main()