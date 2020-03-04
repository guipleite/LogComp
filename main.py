import sys

class Token():

    def __init__(self,tokenType,tokenValue):
        self.tokenType = tokenType
        self.tokenValue = tokenValue

class Tokenizer(code):

    def __init__(self,origin,position,actual):
        self.origin = origin
        self.positon = position
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
    def parseExression(tokens):

        if Parser.Tokenizer.actual.tokenType.isDigit():
            result = Parser.Tokenizer.actual.tokenValue

            Parser.Tokenizer.selectNext()

            while Parser.Tokenizer.actual.tokenType == "+" or Parser.Tokenizer.actual.tokenType == "-":
                if Parser.Tokenizer.actual.tokenType =="+":
                    Parser.Tokenizer.selectNext()

                    if Parser.Tokenizer.actual.tokenType.isDigit():
                        result+=Parser.Tokenizer.actual.tokenValue
                    else: 
                         raise Exception("Erro, verifique a exprecao")        

                if Parser.Tokenizer.actual.tokenType =="-":
                    Parser.Tokenizer.actual.Tokenizer.selectNext()

                    if Parser.Tokenizer.actual.tokenType.isDigit():
                        result-=Parser.Tokenizer.actual.tokenValue
                    else: 
                        raise Exception("Erro, verifique a exprecao")        
            
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