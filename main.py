import sys

class PrePro():

    @staticmethod
    def filter(text):

        text = list(text)
        i = 0

        while(i!=len(text)):
            if text[i]=="/" and text[i+1]=="*":
                j=i
                while True:
                    i+=1
                    if text[i]=="*" and text[i+1]=="/":
                        break
                for k in range(j,i+2):
                    text[k] = ''

            i+=1

        text = "".join(text)+" "

        return text

class Token():

    def __init__(self,tokenType,tokenValue):
        self.tokenType = tokenType
        self.tokenValue = tokenValue

class Node():

    def __init__(self):
        self.value = 0
        self.children = []
        self.Evaluate()

    def Evaluate(self):
        return self.value

class SymbolTable():
    def __init__(self):
        self.id_dict = {}

    def getter(self, iden):
        if identifier in self.id_dict:
            return self.id_dict[iden]

        else:
            raise Exception("Erro, verifique a exprecao identificador nao declarado")

    def setter(self, iden, value):
        self.id_dict[iden] = value

class Assignment(Node):
    def __init__(self,value,children):
        self.value = value
        self.children = children

    def Evaluate(self, SymbolTable):
        SymbolTable.setter[self.value,self.children[0].Evaluate()]

class Identifier(Node):
    def __init__(self,value):
        self.value = value

    def Evaluate(self, SymbolTable):
        result = SymbolTable.getter[self.value]
        return result
    
class Tokenizer():

    def __init__(self,origin):
        self.origin = origin
        self.positon = 0
        self.actual = None
        self.counter = 0
        self.selectNext()
    
    def selectNext(self):
        if self.origin[self.positon] == " " :
            b4 = False
            if self.origin[self.positon-1].isdigit():
                b4 = True
            while self.positon<(len(self.origin)) and  self.origin[self.positon] == " ":
                self.positon+=1
            if b4 and self.positon<(len(self.origin)):
                if self.origin[self.positon].isdigit():
                    raise Exception("Erro, espaco enter numeros")        

        if self.positon==(len(self.origin)):
            self.actual = Token('' , 'EOF')
            return None
            
        if self.origin[self.positon] == "+":
            self.actual = Token('operator' , '+')
            self.positon+=1

        elif self.origin[self.positon] == "-":
            self.actual = Token('operator' , '-')
            self.positon+=1

        elif self.origin[self.positon] == "*":
            self.actual = Token('operator' , '*')
            self.positon+=1

        elif self.origin[self.positon] == "/":
            self.actual = Token('operator' , '/')
            self.positon+=1

        elif self.origin[self.positon] == "{":
            self.actual = Token('command' , '{')
            self.positon+=1

        elif self.origin[self.positon] == "}":
            self.actual = Token('command' , '}')
            self.positon+=1

        elif self.origin[self.positon] == ";":
            self.actual = Token('endline' , ';')
            self.positon+=1

        elif self.origin[self.positon] == "$":
            var = ''
            self.positon+=1
            while self.origin[self.positon].isalpha():######
                var+=self.origin[self.positon]
                
                if self.positon==(len(self.origin)-1):
                    break
                else:
                    self.positon+=1

            self.actual = Token('iden', var)

        elif self.origin[self.positon] == "=":
            self.actual = Token('assignment' , '=')
            self.positon+=1


        elif self.origin[self.positon] == ")" :
            self.actual = Token('str' , ')')
            self.positon+=1
            self.counter-=1
            if self.counter<0:
                raise Exception("Erro, verifique a exprecao 1")      

        elif self.origin[self.positon] == "(" :
            self.actual = Token('str' , '(')
            if self.origin[self.positon-1].isdigit():
                raise Exception("Erro, verifique a exprecao 1")        

            self.positon+=1
            self.counter+=1


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

class BinOp(Node):
    
    def __init__(self, value, child):
        self.value = value
        self.children = child
        
    def Evaluate(self):

        if self.value == '+':
            result = self.children[0].Evaluate() + self.children[1].Evaluate()
            return result

        elif self.value == '-':
            result = self.children[0].Evaluate() - self.children[1].Evaluate()
            return result

        elif self.value == '*':
            result = self.children[0].Evaluate() * self.children[1].Evaluate()
            return result

        elif self.value == '/':
            result = self.children[0].Evaluate() // self.children[1].Evaluate()
            return result

class UnOp(Node):

    def __init__(self, value, child):
        self.value = value
        self.children = child

    def Evaluate(self):
        if self.value == '-':
            result = -self.children[0].Evaluate()
            return result

        else:
            return self.children[0].Evaluate()

class IntVal(Node):
    def __init__(self, value, child):
        self.value = value
        #self.children = child

    def Evaluate(self):
        return self.value

class NoOp(Node):
    def __init__(self, value, child):
        self.value = value
        #self.children = child

    def Evaluate(self):
        #return ""
        pass

class Commands(Node):
    def __init__(self,children):
        self.children = children
    
    def Evaluate(self):
        for child in self.children:
            child.Evaluate(SymbolTable)

class Parser():

    def __init__(self,tokens):
        self.tokens = tokens

    @staticmethod
    def parseBlock():
        if Parser.tokens.actual.tokenValue== "{":
            commands = []
            while Parser.tokens.actual.tokenValue != "}":
                print("1")
                Parser.tokens.selectNext()
                print("2",Parser.tokens.actual.tokenValue)

                commands.append(Parser.parseCommand())
                print("ac",commands)

            if Parser.tokens.actual.tokenValue== "}":
                # print("))",node.Evaluate())
                return Commands(commands)

            else :
                raise Exception("Erro, verifique a exprecao nao fechou }") 
        else:
            raise Exception("Erro, verifique a exprecao nao abriu {") 

    @staticmethod
    def parseCommand():

        if True:

            if Parser.tokens.actual.tokenType== "iden":
                print("3",Parser.tokens.actual.tokenValue)
                var = Parser.tokens.actual.tokenValue
                
                Parser.tokens.selectNext()
                print("4",Parser.tokens.actual.tokenValue)

                print("|",len(var),"|")

                if Parser.tokens.actual.tokenValue== "=":
                    #result = Parser.parseExpression(Parser.tokens)
                    Parser.tokens.selectNext()

                    result = Assignment(var,Parser.parseExpression(Parser.tokens))    
                else:
                    raise Exception("Erro, verifique a exprecao =") 

            elif Parser.tokens.actual.tokenValue== "echo":
                result = Parser.parseExpression(Parser.tokens)
           
            if Parser.tokens.actual.tokenValue== ";":

                 #raise Exception("Erro, verifique a exprecao ;") 
                return result

        else:
            Parser.parseBlock()

    @staticmethod
    def parseFactor():

        if str(Parser.tokens.actual.tokenValue).isdigit():
            result = IntVal(Parser.tokens.actual.tokenValue, [])
            return result
  
        elif str(Parser.tokens.actual.tokenValue)== "+":
            Parser.tokens.selectNext()
            child = [Parser.parseFactor()]
            result =  UnOp('+', child)
            return result

        elif str(Parser.tokens.actual.tokenValue)== "-":
            Parser.tokens.selectNext()
            child = [Parser.parseFactor()]
            result =  UnOp('-', child)
            return result
        
        elif Parser.tokens.actual.tokenValue=="(":
            Parser.tokens.selectNext()
            result = Parser.parseExpression(Parser.tokens)

            if Parser.tokens.actual.tokenValue!=")":
                raise Exception("Erro, verifique a exprecao nao fechou )") 
            else:
                return result
        else: 
            print("5",Parser.tokens.actual.tokenValue)

            raise Exception("Erro, verifique a exprecao a")        
       
    @staticmethod
    def parseTerm():
        node = Parser.parseFactor()
        Parser.tokens.selectNext()
        
        while Parser.tokens.actual.tokenValue == "*" or Parser.tokens.actual.tokenValue == "/" :

            if Parser.tokens.actual.tokenValue =="*":
                Parser.tokens.selectNext()
                child = [node, Parser.parseFactor()]
                node = BinOp('*', child)

            elif Parser.tokens.actual.tokenValue =="/":
                Parser.tokens.selectNext()
                child = [node, Parser.parseFactor()]
                node = BinOp('/', child)
            Parser.tokens.selectNext()

        return node   

    @staticmethod
    def parseExpression(tokens):
        node = Parser.parseTerm()
      
        while Parser.tokens.actual.tokenValue == "+" or Parser.tokens.actual.tokenValue == "-" :
            if Parser.tokens.actual.tokenValue =="+":
                Parser.tokens.selectNext()
                child = [node, Parser.parseTerm()]
                node = BinOp('+', child)

            elif Parser.tokens.actual.tokenValue =="-":
                Parser.tokens.selectNext()
                child = [node, Parser.parseTerm()]
                node = BinOp('-', child)
        
        return node

    @staticmethod
    def run(code):
        code = PrePro.filter(code)
        Parser.tokens = Tokenizer(code)
        Parser.table = SymbolTable()
        parsed = Parser.parseBlock()
        return parsed.Evaluate()

def main():

    #inp = sys.argv[1]
    import fileinput

    for line in fileinput.input():
        #process(line)
        # try:
            print(Parser.run(line))
            
        # except :
        #     raise Exception("Erro, verifique a exprecao")        

if __name__ == '__main__':
    main()