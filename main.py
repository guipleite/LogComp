import sys

class PrePro():

    @staticmethod
    def filter(text):

        text = list(text)

        i = 0

        while(i!=len(text)):
            if text[i]=="\n":
                text[i] = ''
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
        print(text)
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

class AssignOp(Node):
    def __init__(self,value,child):
        self.value = value
        self.children = child

    def Evaluate(self, SymbolTable):
        print(self.value,"=",self.children.Evaluate(SymbolTable))

        SymbolTable.setter(self.value,self.children.Evaluate(SymbolTable))
    
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
        
    def Evaluate(self,table):

        if self.value == '+':
            result = self.children[0].Evaluate() + self.children[1].Evaluate()
            return result

        elif self.value == '-':
            result = self.children[0].Evaluate(table) - self.children[1].Evaluate()
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

class IdenVal(Node):
    def __init__(self, value, child):
        self.value = value
       # self.children = child

    def Evaluate(self, SymbolTable):
        result = SymbolTable.getter(self.value)
        return result

class CommandOp(Node):
    def __init__(self,child):
        self.children = child
    
    def Evaluate(self):
        for child in self.children:
            x = child.Evaluate(Parser.table)
            print ("x",Parser.table.id_dict)

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
                c = Parser.parseCommand()

                if c != None:
                    commands.append(c)
                print("ac",commands)

            if Parser.tokens.actual.tokenValue== "}":
                # print("))",node.Evaluate())
                return CommandOp(commands)

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

                if Parser.tokens.actual.tokenValue== "=":
                    Parser.tokens.selectNext()
                    result = AssignOp(var,Parser.parseExpression(Parser.tokens))    
                else:
                    raise Exception("Erro, verifique a exprecao =") 

            elif Parser.tokens.actual.tokenValue== "echo":
                result = Parser.parseExpression(Parser.tokens)
           
            if Parser.tokens.actual.tokenValue== ";":

                return result

        else:
            Parser.parseBlock()

    @staticmethod
    def parseFactor():

        if str(Parser.tokens.actual.tokenValue).isdigit():
            result = IntVal(Parser.tokens.actual.tokenValue, [])
            return result

        elif Parser.tokens.actual.tokenType == "iden":
            result = IdenVal(Parser.tokens.actual.tokenValue, [])
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
            print(Parser.tokens.actual.tokenType)

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

    try:
        fileobj = open(sys.argv[1], 'r')
    except IndexError:
        fileobj = sys.stdin

    with fileobj:
        data = fileobj.read()

    # try:
    print(Parser.run(data))
            
    # except :
    #     raise Exception("Erro, verifique a exprecao")        

if __name__ == '__main__':
    main()