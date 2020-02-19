class Token():

    def __init__(self,tokenType,tokenValue):
        self.tokenType = tokenType
        self.tokenValue = tokenValue

class Tokenizer():

    def __init__(self,origin,position,actual):
        self.origin = origin
        self.positon = position
        self.actual = None
        self.selectNext()
    
    def selectNext(tokens):
        
        if self.origin[self.positon] == " ":
            self.positon++

        if self.origin[self.positon] == "+":
            self.actual = "+"

        elif self.origin[self.positon] == "-":
            self.actual = "-"

        elif self.origin[self.positon].isDigit():
            num = ''
            while self.origin[self.positon].isDigit():
                num+=self.origin[self.positon]
                self.positon++

            self.actual = int(num)

        else:
            raise exeption "aaa"

class Parser():

    def __init__(self,tokens):
        self.tokens = tokens

    tokens = Tokenizer(origin,position,actual)

    @staticmethod
    def parseExression(tokens):
        pass

    @staticmethod
    def run(code):
        pass


