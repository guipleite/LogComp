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

class WriteFile():
    # def __init__(self):
    #     self.file_content = []

    file_content = []
    def addInstruction(instrction):
        WriteFile.file_content.append(instrction)

    def WriteToFile(filename):
        filename = filename+".asm"
        with open(filename, 'w') as output_file:
            with open("modelo.asm", 'r') as modelo:
                for line in modelo:
                     output_file.write(str(line))

            output_file.write("\n")

            for line in WriteFile.file_content:
                output_file.write(str(line) + "\n")

            output_file.write("\n" + "  ; interrupcao de saida" + "\n" + "POP EBP" + "\n" + "MOV EAX, 1" + "\n" + "INT 0x80")

class Token():

    def __init__(self,tokenType,tokenValue):
        self.tokenType = tokenType
        self.tokenValue = tokenValue

class Node():
    currentId = 0

    def __init__(self):
        self.value = 0
        self.children = []
        self.Evaluate()
        self.id = self.NodeId()

    def Evaluate(self):
        return self.value
    @staticmethod
    def NodeId():
        Node.currentId += 1
        return Node.currentId

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

        elif self.origin[self.positon] == "<" and self.origin[self.positon+1] != "?":
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

        elif self.origin[self.positon] == ".":
            self.actual = Token('concat' , '.')
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

        elif self.origin[self.positon] == '"':
            string = ''
            self.positon+=1

            while self.origin[self.positon]!='"':
                string+=self.origin[self.positon]
                self.positon+=1
                
            self.positon+=1
            self.actual = Token('str', string)

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
            self.actual = Token('close(' , ')')
            self.positon+=1
            self.counter-=1
            if self.counter<0:
                raise Exception("Erro, verifique a exprecao 1")      

        elif self.origin[self.positon] == "(" :
            self.actual = Token('open(' , '(')
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

        elif self.origin[self.positon] == "<" and self.origin[self.positon+1] == "?" and self.origin[self.positon+2] == "p" and self.origin[self.positon+3] == "h" and self.origin[self.positon+4] == "p"  :
            self.positon+=5
            self.actual = Token('<?php' , '<?php')

        elif self.origin[self.positon] == "?" and self.origin[self.positon+1] == ">" :
            self.positon+=2
            self.actual = Token('?>' , '?>')

        else:
            raise Exception("Erro, verifique a exprecao 1")        

class BinOp(Node):
    
    def __init__(self, value, child):
        self.value = value
        self.children = child
        
    def Evaluate(self,table):
        ebx = self.children[0].Evaluate(table) 
        WriteFile.addInstruction("PUSH EBX ;") # O BinOp guarda o resultado na pilha
        eax =  self.children[1].Evaluate(table)

        if self.value == '+':
            # ebx = self.children[0].Evaluate(table)[0] 
            # WriteFile.addInstruction("PUSH EBX ;") # O BinOp guarda o resultado na pilha

            # eax =  self.children[1].Evaluate(table)[0]
            WriteFile.addInstruction("POP EAX ;") # O BinOp recupera o valor da pilha em EAX
            WriteFile.addInstruction("ADD EAX, EBX ;") # O BinOp executa a operação correspondente
            WriteFile.addInstruction("MOV EBX, EAX ;") #  O BinOp retorna o valor em EBX (sempre EBX

            result = ebx[0] + eax[0]
            return (result,"int")

        elif self.value == '-':
            # ebx = self.children[0].Evaluate(table)[0] 
            # WriteFile.addInstruction("PUSH EBX ;") # O BinOp guarda o resultado na pilha

            # eax =  self.children[1].Evaluate(table)[0]
            WriteFile.addInstruction("POP EAX ;") # O BinOp recupera o valor da pilha em EAX
            WriteFile.addInstruction("SUB EAX, EBX ;") # O BinOp executa a operação correspondente
            WriteFile.addInstruction("MOV EBX, EAX ;") #  O BinOp retorna o valor em EBX (sempre EBX

            result = ebx[0] - eax[0]
            return (result,"int")

        elif self.value == '*':
            # ebx = self.children[0].Evaluate(table)[0] 
            # WriteFile.addInstruction("PUSH EBX ;") # O BinOp guarda o resultado na pilha

            # eax =  self.children[1].Evaluate(table)[0]
            WriteFile.addInstruction("POP EAX ;") # O BinOp recupera o valor da pilha em EAX
            WriteFile.addInstruction("IMUL EAX, EBX ;") # O BinOp executa a operação correspondente
            WriteFile.addInstruction("MOV EBX, EAX ;") #  O BinOp retorna o valor em EBX (sempre EBX

            result = ebx[0] * eax[0]
            return (result,"int")


        elif self.value == '/':
            # ebx = self.children[0].Evaluate(table)[0] 
            # WriteFile.addInstruction("PUSH EBX ;") # O BinOp guarda o resultado na pilha

            # eax =  self.children[1].Evaluate(table)[0]
            WriteFile.addInstruction("POP EAX ;") # O BinOp recupera o valor da pilha em EAX
            WriteFile.addInstruction("IDIV EAX, EBX ;") # O BinOp executa a operação correspondente
            WriteFile.addInstruction("MOV EBX, EAX ;") #  O BinOp retorna o valor em EBX (sempre EBX

            result = ebx[0] // eax[0]
            return (result,"int")


        elif self.value == '==':
            # ebx = self.children[0].Evaluate(table)[0] 
            # WriteFile.addInstruction("PUSH EBX ;") # O BinOp guarda o resultado na pilha

            # eax =  self.children[1].Evaluate(table)[0]
            WriteFile.addInstruction("POP EAX ;") # O BinOp recupera o valor da pilha em EAX
            WriteFile.addInstruction("CMP EAX, EBX ;") # O BinOp executa a operação correspondente
            WriteFile.addInstruction("CALL binop_je ;") #  O BinOp retorna o valor em EBX (sempre EBX

            result = ebx[0] == eax[0]
            return (result,"bool")

        elif ebx[1]!="str" and  eax[1]!="str":
            if self.value == '>':
                #WriteFile.addInstruction("PUSH EBX ;") # O BinOp guarda o resultado na pilha

                WriteFile.addInstruction("POP EAX ;") # O BinOp recupera o valor da pilha em EAX
                WriteFile.addInstruction("CMP EAX, EBX ;") # O BinOp executa a operação correspondente
                WriteFile.addInstruction("CALL binop_jg ;") #  O BinOp retorna o valor em EBX (sempre EBX

                result = ebx[0] > eax[0]
                return (result,"bool")

            elif self.value == '<':
                # ebx = self.children[0].Evaluate(table)[0] 
                # WriteFile.addInstruction("PUSH EBX ;") # O BinOp guarda o resultado na pilha

                # eax =  self.children[1].Evaluate(table)[0]
                WriteFile.addInstruction("POP EAX ;") # O BinOp recupera o valor da pilha em EAX
                WriteFile.addInstruction("CMP EAX, EBX ;") # O BinOp executa a operação correspondente
                WriteFile.addInstruction("CALL binop_jl ;") #  O BinOp retorna o valor em EBX (sempre EBX

                result = ebx[0] < eax[0]
                return (result,"bool")

            elif self.value == 'and':
                # ebx = self.children[0].Evaluate(table)[0] 
                # WriteFile.addInstruction("PUSH EBX ;") # O BinOp guarda o resultado na pilha

                # eax =  self.children[1].Evaluate(table)[0]
                WriteFile.addInstruction("POP EAX ;") # O BinOp recupera o valor da pilha em EAX
                WriteFile.addInstruction("and EAX, EBX ;") # O BinOp executa a operação correspondente
                WriteFile.addInstruction("MOV EBX, EAX ;") #  O BinOp retorna o valor em EBX (sempre EBX

                result = ebx[0] and eax[0]
                return (result,"bool")
            
            elif self.value == 'or':
                # ebx = self.children[0].Evaluate(table)[0] 
                # WriteFile.addInstruction("PUSH EBX ;") # O BinOp guarda o resultado na pilha

                # eax =  self.children[1].Evaluate(table)[0]
                WriteFile.addInstruction("POP EAX ;") # O BinOp recupera o valor da pilha em EAX
                WriteFile.addInstruction("OR EAX, EBX ;") # O BinOp executa a operação correspondente
                WriteFile.addInstruction("MOV EBX, EAX ;") #  O BinOp retorna o valor em EBX (sempre EBX

                result = ebx[0] or eax[0]
                return (result,"bool")
        
        elif self.value == '.': #####
            result = str(self.children[0].Evaluate(table)[0]) + str(self.children[1].Evaluate(table)[0])
            return (result,"str")

        else:
             raise Exception("Erro, verifique a exprecao operacao nao permitida")

class UnOp(Node):

    def __init__(self, value, child):
        self.value = value
        self.children = child

    def Evaluate(self,table):
        if self.value == '-':
            result = -self.children[0].Evaluate(table)[0]
            return (result,self.children[0].Evaluate(table)[1])

        if self.value == '!':
            result = not self.children[0].Evaluate(table)[0]
            return (result,self.children[0].Evaluate(table)[1])

        else:
            return self.children[0].Evaluate(table)

class IntVal(Node):
    def __init__(self, value, child):
        self.value = value
        #self.children = child

    def Evaluate(self,table):
        WriteFile.addInstruction("MOV EBX, "+str(self.value)+" ;")
        return (self.value,"int")

class BoolVal(Node):
    def __init__(self, value, child):
        self.value = value
        self.children = child

    def Evaluate(self,table):
        if self.value == "true":
            return (1,"bool")
        else:
            return (0,"bool")

class StringVal(Node):
    def __init__(self, value, child):
        self.value = value
        #self.children = child

    def Evaluate(self,table):
        return (self.value,"str")

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
        self.addr = 0

    def getter(self, iden):
        if iden in self.id_dict:
            return self.id_dict[iden]
        else:
            raise Exception("Erro, verifique a exprecao identificador nao declarado")

    def setter(self, iden, value):
        if iden in self.id_dict:
            self.id_dict[iden][0] = value
        else:
            self.addr+=4
            self.id_dict[iden] = [value,self.addr]
            WriteFile.addInstruction("PUSH DWORD 0 ;")

class AssignOp(Node):
    def __init__(self, value, child):
        self.value = value
        self.children = child

    def Evaluate(self,table):
        iden = self.value
        table.setter(self.value,self.children.Evaluate(table))
        result = table.getter(self.value)
        WriteFile.addInstruction("MOV [EBP-"+str(result[1])+"], EBX ;")

class IdenVal(Node):
    def __init__(self, value):
        self.value = value

    def Evaluate(self,table):
        result = table.getter(self.value)
        WriteFile.addInstruction("MOV EBX, [EBP-"+str(result[1])+"] ;")
        return result[0]

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
        print(self.children.Evaluate(table)[0])

        WriteFile.addInstruction("PUSH EBX ;") # Empilhe os argumentos
        WriteFile.addInstruction("CALL print ;") # Chamada da função
        WriteFile.addInstruction("POP EBX ;") # Desempilhe os argumentos

class WhileOp(Node):
    def __init__(self,child):
        self.children = child
        self.id = Node.NodeId()

    def Evaluate(self,table):
        WriteFile.addInstruction("LOOP_"+str(self.id)+": ;") #  o unique identifier do nó while 

        condition = self.children[0].Evaluate(table)[0]
        WriteFile.addInstruction("CMP EBX, False ;") # verifica se o teste deu falso
        WriteFile.addInstruction("JE EXIT_"+str(self.id)+" ;") # e sai caso for igual a falso.

        # for child in self.children:
        #    child.Evaluate(table)
        self.children[1].Evaluate(table)
        WriteFile.addInstruction("JMP LOOP_"+str(self.id)+" ;") # volta para testar de novo
        WriteFile.addInstruction("EXIT_"+str(self.id)+": ;")

class IfOp(Node):
    def __init__(self, child):
        self.children = child
        self.id = Node.NodeId()

    def Evaluate(self,table):
        condition = self.children[0].Evaluate(table)[0]
        WriteFile.addInstruction("CMP EBX, False ;") # verifica se o teste deu falso

        if condition:
            #spass
            return self.children[1].Evaluate(table)
        else:

            if len(self.children) == 3:
                WriteFile.addInstruction("JE ELSE_"+str(self.id)+" ;")

                for child in self.children[1]:
                    child.Evaluate(table)
                    
                WriteFile.addInstruction("JMP EXIT_"+str(self.id)+" ;") # volta para testar de novo
                WriteFile.addInstruction("ELSE_"+str(self.id)+" ;")

                for child in self.children[2]:
                    child.Evaluate(table)
            else:
                WriteFile.addInstruction("JE EXIT_"+str(self.id)+" ;") 
                for child in self.children[1]:
                    child.Evaluate(table)
                
            WriteFile.addInstruction("EXIT_"+str(self.id)+": ;")

class ReadlineOP(Node):
    def __init__(self):
        # self.children = child
        pass

    def Evaluate(self, table):
        inp = input()
        return (int(inp),"int")

class Parser():

    def __init__(self,tokens):
        self.tokens = tokens

    @staticmethod
    def parseProgram():
        if Parser.tokens.actual.tokenValue== "<?php":
            r = Parser.parseCommand()

            if Parser.tokens.actual.tokenValue== "?>":
                    return r
            else :
                raise Exception("Erro, verifique a exprecao nao fechou ?>") 
        else:
            raise Exception("Erro, verifique a exprecao nao abriu <?php") 

    @staticmethod
    def parseCommand():
        if Parser.tokens.actual.tokenValue!="{" and Parser.tokens.actual.tokenValue!="<?php":
            # result = None
            if Parser.tokens.actual.tokenType== "iden":
                var = Parser.tokens.actual.tokenValue
                Parser.tokens.selectNext()

                if Parser.tokens.actual.tokenValue== "=":
                    Parser.tokens.selectNext()
                    result = AssignOp(var,Parser.parseRelExpression(Parser.tokens))

                else:
                    raise Exception("Erro, verifique a exprecao =") 

            elif Parser.tokens.actual.tokenValue== "echo":
                Parser.tokens.selectNext()
                result = EchoOp(Parser.parseRelExpression(Parser.tokens))
                return result


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
                else:
                    raise Exception("Erro, verifique a exprecao: nao abriu (")        

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

        if Parser.tokens.actual.tokenValue=="{" or Parser.tokens.actual.tokenValue=="<?php":
            return Parser.parseBlock()
    
    @staticmethod
    def parseBlock():
        if Parser.tokens.actual.tokenValue== "{" or Parser.tokens.actual.tokenValue== "<?php" :
            commands = []
            while Parser.tokens.actual.tokenValue != "}" and Parser.tokens.actual.tokenValue != "?>":

                Parser.tokens.selectNext()
                c = Parser.parseCommand()

                if c != None:
                    commands.append(c)
                    
            if Parser.tokens.actual.tokenValue== "}" or Parser.tokens.actual.tokenValue== "?>" :
                c = Parser.parseCommand()

                if c != None:
                    commands.append(c)

                C =CommandOp(commands)
                if Parser.tokens.actual.tokenValue!= "?>":
                    Parser.tokens.selectNext() ##

                return C

            else :
                raise Exception("Erro, verifique a exprecao nao fechou }") 
        else:
            raise Exception("Erro, verifique a exprecao nao abriu {") 

    @staticmethod
    def parseFactor():

        if str(Parser.tokens.actual.tokenValue).isdigit():
            result = IntVal(Parser.tokens.actual.tokenValue, [])
            return result

        elif Parser.tokens.actual.tokenValue == "true" or Parser.tokens.actual.tokenValue == "false":
            result = BoolVal(Parser.tokens.actual.tokenValue, [])
            return result

        elif Parser.tokens.actual.tokenType == "iden":
            result = IdenVal(Parser.tokens.actual.tokenValue)
            return result
        
        elif str(Parser.tokens.actual.tokenType)== "str":
            result = StringVal(Parser.tokens.actual.tokenValue, [])
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

                    return result

        else: 
            print((Parser.tokens.actual.tokenValue))
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
      
        while Parser.tokens.actual.tokenValue == "+" or Parser.tokens.actual.tokenValue == "-" or Parser.tokens.actual.tokenValue == "or"  or Parser.tokens.actual.tokenValue == "." :
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

            elif Parser.tokens.actual.tokenValue ==".":
                Parser.tokens.selectNext()
                child = [node, Parser.parseTerm()]
                node = BinOp('.', child)
        
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
        parsed = Parser.parseProgram()
        final = parsed.Evaluate(table)
        WriteFile.WriteToFile("program")
        return final

def main():

    try:
        fileobj = open(sys.argv[1], 'r')
    except IndexError:
        fileobj = open("./test.php",'r')

    # fileobj = open("./test.php",'r')
    with fileobj:
        data = fileobj.read()

    try:
        Parser.run(data)
            
    except :
        raise Exception("Erro, verifique a exprecao")        

if __name__ == '__main__':
    main()