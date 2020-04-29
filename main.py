import sys

reserved_words = ["echo","and","or","!","if","while","else","readline","true","false"]

class PrePro():

    @staticmethod
    def filter(text):

        text = list(text)

        i = 0

        while(i!=len(text)):
            if text[i]=="\n":
                text[i] = ''
            if text[i]=="}": ##
                text[i] = "};"
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
        
        elif self.origin[self.positon] == ">":
            self.actual = Token('operator' , '>')
            self.positon+=1

        elif self.origin[self.positon] == "<":
            self.actual = Token('operator' , '<')
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

        elif self.origin[self.positon] == "!":
            self.actual = Token('un' , '!')
            self.positon+=1

        elif self.origin[self.positon] == "$":
            var = ''
            self.positon+=1

            if  self.origin[self.positon].isalpha():
                var+=self.origin[self.positon]
                self.positon+=1
                while self.origin[self.positon].isalnum() or self.origin[self.positon]=="_":
                    var+=self.origin[self.positon]
                    
                    if self.positon==(len(self.origin)-1):
                        break
                    else:
                        self.positon+=1

                self.actual = Token('iden', var)

            else:
                raise Exception("Erro, verifique a exprecao nome de variavel invalido")  

        elif self.origin[self.positon].isalpha():
            var = self.origin[self.positon]
            self.positon+=1
            while self.origin[self.positon].isalpha():
                var+=self.origin[self.positon]
                
                if self.positon==(len(self.origin)-1):
                    break
                else:
                    self.positon+=1
            if var.lower() in reserved_words:
                self.actual = Token('res', var.lower())

        elif self.origin[self.positon] == "=":
            if (self.origin[self.positon+1]=="="):
                self.actual = Token('eq' , '==')
                self.positon+=2
            else:
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
            result = self.children[0].Evaluate(table) + self.children[1].Evaluate(table)
            return result

        elif self.value == '-':
            result = self.children[0].Evaluate(table) - self.children[1].Evaluate(table)
            return result

        elif self.value == '*':
            result = self.children[0].Evaluate(table) * self.children[1].Evaluate(table)
            return result

        elif self.value == '/':
            result = self.children[0].Evaluate(table) // self.children[1].Evaluate(table)
            return result

        elif self.value == '>':
            result = self.children[0].Evaluate(table) > self.children[1].Evaluate(table)
            return result

        elif self.value == '<':
            result = self.children[0].Evaluate(table) < self.children[1].Evaluate(table)
            return result

        elif self.value == '==':
            result = self.children[0].Evaluate(table) == self.children[1].Evaluate(table)
            return result
        
        elif self.value == 'and':
            result = self.children[0].Evaluate(table) and self.children[1].Evaluate(table)
            return result
        
        elif self.value == 'or':
            result = self.children[0].Evaluate(table) or self.children[1].Evaluate(table)
            return result

class UnOp(Node):

    def __init__(self, value, child):
        self.value = value
        self.children = child

    def Evaluate(self,table):
        if self.value == '-':
            result = -self.children[0].Evaluate(table)
            return result

        if self.value == '!':
            result = not self.children[0].Evaluate(table)
            return result

        else:
            return self.children[0].Evaluate(table)

class IntVal(Node):
    def __init__(self, value, child):
        self.value = value
        #self.children = child

    def Evaluate(self,table):
        return self.value

class NoOp(Node):
    def __init__(self, value, child):
        self.value = value
        #self.children = child

    def Evaluate(self,table):
        #return ""
        pass

class SymbolTable():
    def __init__(self):
        self.id_dict = {}

    def getter(self, iden):
        if iden in self.id_dict:
            return self.id_dict[iden]

        else:
            raise Exception("Erro, verifique a exprecao identificador nao declarado")

    def setter(self, iden, value):
        self.id_dict[iden] = value

class AssignOp(Node):
    def __init__(self, value, child):
        self.value = value
        self.children = child

    def Evaluate(self,table):
        iden = self.value
        #val  = self.children.Evaluate(table)

        table.setter(self.value,self.children.Evaluate(table))

class IdenVal(Node):
    def __init__(self, value):
        self.value = value

    def Evaluate(self,table):
        result = table.getter(self.value)
        return result

class CommandOp(Node):
    def __init__(self,child):
        self.children = child
    
    def Evaluate(self,table):
        for child in self.children:
            child.Evaluate(table)

class EchoOp(Node):
    def __init__(self,child):
        self.children = child
        
    def Evaluate(self,table):
        print(self.children.Evaluate(table))

class WhileOp(Node):
    def __init__(self,child):
        self.children = child

    def Evaluate(self,table):
        while self.children[0].Evaluate(table):
            self.children[1].Evaluate(table)

class IfOp(Node):
    def __init__(self, child):
        self.children = child

    def Evaluate(self,table):
        if self.children[0].Evaluate(table):
            return self.children[1].Evaluate(table)

        else:

            if len(self.children) == 3:
                return self.children[2].Evaluate(table)

            else:
                pass

class ReadlineOP(Node):
    def __init__(self):
        # self.children = child
        pass

    def Evaluate(self, table):
        inp = input()
        return int(inp)

class Parser():

    def __init__(self,tokens):
        self.tokens = tokens

    @staticmethod
    def parseBlock():
        if Parser.tokens.actual.tokenValue== "{":
            commands = []
            while Parser.tokens.actual.tokenValue != "}":
                Parser.tokens.selectNext()
                c = Parser.parseCommand()

                if c != None:
                    commands.append(c)
                    
            if Parser.tokens.actual.tokenValue== "}":
                # Parser.tokens.selectNext()
                c = Parser.parseCommand()

                if c != None:
                    commands.append(c)

                C =CommandOp(commands)
                Parser.tokens.selectNext() ##
                return C

            else :
                raise Exception("Erro, verifique a exprecao nao fechou }") 
        else:
            raise Exception("Erro, verifique a exprecao nao abriu {") 

    @staticmethod
    def parseCommand():
       
        if Parser.tokens.actual.tokenValue!="{":
            # result = None
            if Parser.tokens.actual.tokenType== "iden":
                var = Parser.tokens.actual.tokenValue
                Parser.tokens.selectNext()

                if Parser.tokens.actual.tokenValue== "=":
                    Parser.tokens.selectNext()
                    result = AssignOp(var,Parser.parseRelExpression(Parser.tokens))

                else:
                    print(Parser.tokens.actual.tokenValue)
                    Parser.tokens.selectNext()
                    print(Parser.tokens.actual.tokenValue)
                    Parser.tokens.selectNext()
                    print(Parser.tokens.actual.tokenValue)
                    Parser.tokens.selectNext()
                    print(Parser.tokens.actual.tokenValue)


                    raise Exception("Erro, verifique a exprecao =") 

            elif Parser.tokens.actual.tokenValue== "echo":
                Parser.tokens.selectNext()
                result = EchoOp(Parser.parseRelExpression(Parser.tokens))

            elif Parser.tokens.actual.tokenValue == "if":
                Parser.tokens.selectNext()
                children = []
                if Parser.tokens.actual.tokenValue == "(":

                    while Parser.tokens.actual.tokenValue != ")":
                        Parser.tokens.selectNext()
                        node = Parser.parseRelExpression(Parser.tokens)
                        children.append(node)

                    if Parser.tokens.actual.tokenValue == ")":
                        Parser.tokens.selectNext()
                        if Parser.tokens.actual.tokenValue=="{":
                            children.append(Parser.parseBlock())
                          
                            Parser.tokens.selectNext()
                            if Parser.tokens.actual.tokenValue == "else":
                                Parser.tokens.selectNext()
                                
                                if Parser.tokens.actual.tokenValue == "{":
                                    children.append(Parser.parseBlock())

                                elif Parser.tokens.actual.tokenValue == "if":

                                    children.append(Parser.parseCommand())
                                
                            return IfOp(children)

            elif Parser.tokens.actual.tokenValue == "while":
                Parser.tokens.selectNext()
                if Parser.tokens.actual.tokenValue == "(":

                    while Parser.tokens.actual.tokenValue != ")":
                        Parser.tokens.selectNext()
                        node = Parser.parseRelExpression(Parser.tokens)

                    if Parser.tokens.actual.tokenValue == ")":
                        Parser.tokens.selectNext()
                        if Parser.tokens.actual.tokenValue=="{":
                            result = WhileOp([node,Parser.parseBlock()])

                return result

            if Parser.tokens.actual.tokenValue== ";":
                try:
                    return result
                except:
                    pass

            
            if Parser.tokens.actual.tokenValue== "else":
                raise Exception("Erro, verifique a exprecao: else sem if")        

        if Parser.tokens.actual.tokenValue=="{":
            return Parser.parseBlock()

    @staticmethod
    def parseFactor():

        if str(Parser.tokens.actual.tokenValue).isdigit():
            result = IntVal(Parser.tokens.actual.tokenValue, [])
            return result
            
        elif Parser.tokens.actual.tokenType == "iden":
            result = IdenVal(Parser.tokens.actual.tokenValue)
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

        elif str(Parser.tokens.actual.tokenValue)== "!":
            Parser.tokens.selectNext()
            child = [Parser.parseFactor()]
            result =  UnOp('!', child)
            return result
        
        elif Parser.tokens.actual.tokenValue=="(":
            Parser.tokens.selectNext()
            result = Parser.parseRelExpression(Parser.tokens)

            if Parser.tokens.actual.tokenValue!=")":
                raise Exception("Erro, verifique a exprecao nao fechou )") 
            else:
                return result

        elif Parser.tokens.actual.tokenValue == "readline":
            Parser.tokens.selectNext()
            if Parser.tokens.actual.tokenValue == "(":
                Parser.tokens.selectNext()
                if Parser.tokens.actual.tokenValue == ")":

                    result = ReadlineOP()

                    # Parser.tokens.selectNext()
                    return result

        else: 
            raise Exception("Erro, verifique a exprecao a")        
       
    @staticmethod
    def parseTerm():
        node = Parser.parseFactor()
        Parser.tokens.selectNext()
        
        while Parser.tokens.actual.tokenValue == "*" or Parser.tokens.actual.tokenValue == "/" or Parser.tokens.actual.tokenValue == "and" :

            if Parser.tokens.actual.tokenValue =="*":
                Parser.tokens.selectNext()
                child = [node, Parser.parseFactor()]
                node = BinOp('*', child)

            elif Parser.tokens.actual.tokenValue =="/":
                Parser.tokens.selectNext()
                child = [node, Parser.parseFactor()]
                node = BinOp('/', child)

            elif Parser.tokens.actual.tokenValue =="and":
                Parser.tokens.selectNext()
                child = [node, Parser.parseFactor()]
                node = BinOp('and', child)

            Parser.tokens.selectNext()

        return node

    @staticmethod
    def parseExpression():
        node = Parser.parseTerm()
      
        while Parser.tokens.actual.tokenValue == "+" or Parser.tokens.actual.tokenValue == "-" or Parser.tokens.actual.tokenValue == "or" :
            if Parser.tokens.actual.tokenValue =="+":
                Parser.tokens.selectNext()
                child = [node, Parser.parseTerm()]
                node = BinOp('+', child)

            elif Parser.tokens.actual.tokenValue =="-":
                Parser.tokens.selectNext()
                child = [node, Parser.parseTerm()]
                node = BinOp('-', child)

            elif Parser.tokens.actual.tokenValue =="or":
                Parser.tokens.selectNext()
                child = [node, Parser.parseTerm()]
                node = BinOp('or', child)
        
        return node

    @staticmethod
    def parseRelExpression(tokens):
        node = Parser.parseExpression()
      
        while Parser.tokens.actual.tokenValue == ">" or Parser.tokens.actual.tokenValue == "<" or Parser.tokens.actual.tokenValue == "==":
            if Parser.tokens.actual.tokenValue ==">":
                Parser.tokens.selectNext()
                child = [node, Parser.parseExpression()]
                node = BinOp('>', child)

            elif Parser.tokens.actual.tokenValue =="<":
                Parser.tokens.selectNext()
                child = [node, Parser.parseExpression()]
                node = BinOp('<', child)

            elif Parser.tokens.actual.tokenValue =="==":
                Parser.tokens.selectNext()
                child = [node, Parser.parseExpression()]
                node = BinOp('==', child)
        
        return node
    
    @staticmethod
    def run(code):
        code = PrePro.filter(code)
        Parser.tokens = Tokenizer(code)
        table = SymbolTable()
        parsed = Parser.parseBlock()
        return parsed.Evaluate(table)

def main():

    try:
        fileobj = open(sys.argv[1], 'r')
    except IndexError:
        fileobj = sys.stdin

    # fileobj = open("./test.php",'r')
    with fileobj:
        data = fileobj.read()

    try:
        Parser.run(data)
            
    except :
        raise Exception("Erro, verifique a exprecao")        

if __name__ == '__main__':
    main()