#define a token class to hold the token type and value
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"{self.value},{self.type}\n"
        # return "Token({type}, {value})".format(type=self.type, value=self.value)


#dictionary of all tokens in tiny language and their corresponding values
tokens = {
    "ID": "IDENTIFIER",
    "NUM": "NUMBER",
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'TIMES',
    '/': 'DIVIDE',
    '(': 'OPENBRACKET',
    ')': 'CLOSEBRACKET',
    ';': 'SEMICOLON',
    '=': 'EQUALS',
    ':=': 'ASSIGN',
    '<': 'LESSTHAN',
    '>': 'GREATERTHAN',
    '=': 'EQUAL',
    '!=': 'NOTEQUAL',
    '<=': 'LESSTHANEQUAL',
    '>=': 'GREATERTHANEQUAL',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'end': 'END',
    'repeat': 'REPEAT',
    'until': 'UNTIL',
    'read': 'READ',
    'write': 'WRITE',
}

class Lexer:

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.string_value_accumulator = ""

    def error(self):
        print("Invalid character: " + self.current_char)
        # raise Exception("Invalid character")

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def isspace(self):
        if self.current_char == " " or self.current_char == "\n":
            return True
        else:
            return False

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            # PLUS
            elif self.current_char == "+":
                self.advance()
                return Token(tokens['+'],'+')
            
            # MINUS
            elif self.current_char == "-":
                self.advance()
                return Token(tokens['-'],'-')
            
            # TIMES
            elif self.current_char == "*":
                self.advance()
                return Token(tokens['*'],'*')
            
            # DIVIDE
            elif self.current_char == "/":
                self.advance()
                return Token(tokens['/'],'/')
            
            # LPAREN
            elif self.current_char == "(":
                self.advance()
                return Token(tokens['('],'(')
            
            # RPAREN
            elif self.current_char == ")":
                self.advance()
                return Token(tokens[')'],')')
            
            # SEMICOLON
            elif self.current_char == ";":
                self.advance()
                return Token(tokens[';'],';')
            
            # ASSIGN
            elif self.current_char == ":":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Token(tokens[':='],':=')
                else:
                    self.error()
            
            # Equals
            elif self.current_char == "=":
                self.advance()
                return Token(tokens['='],'=')

            # LT & LEQ
            elif self.current_char == "<":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Token(tokens['<='],'<=')
                else:
                    return Token(tokens['<'],'<')
            
            # GT & GEQ
            elif self.current_char == ">":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Token(tokens['>='],'>=')
                else:
                    return Token(tokens['>'],'>')
            
            # NEQ
            elif self.current_char == "!":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Token(tokens['!='],'!=')
                else:
                    self.error()
            
            # IF
            elif self.current_char == "i" and self.text[self.pos +1] == "f" and (self.pos + 2 == len(self.text) or self.text[self.pos + 2] == " " or self.text[self.pos + 2] == "\n"):
                self.advance()
                self.advance()
                self.advance()
                return Token(tokens['if'],'if')
            
            # THEN
            elif self.current_char == "t" and self.text[self.pos +1] == "h" and self.text[self.pos + 2] == "e" and self.text[self.pos + 3] == "n" and (self.pos + 4 == len(self.text) or self.text[self.pos + 4] == " " or self.text[self.pos + 4] == "\n"): 
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                return Token(tokens['then'],'then')
            
            # ELSE
            elif self.current_char == "e" and self.text[self.pos +1] == "l" and self.text[self.pos + 2] == "s" and self.text[self.pos + 3] == "e" and (self.pos + 4 == len(self.text) or self.text[self.pos + 4] == " " or self.text[self.pos + 4] == "\n"):
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                return Token(tokens['else'],'else')
            
            # END
            elif self.current_char == "e" and self.text[self.pos +1] == "n" and self.text[self.pos + 2] == "d" and (self.pos + 3 == len(self.text) or self.text[self.pos + 3] == " " or self.text[self.pos + 3] == "\n"):
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                return Token(tokens['end'],'end')

            # REPEAT
            elif self.current_char == "r" and self.text[self.pos +1] == "e" and self.text[self.pos + 2] == "p" and self.text[self.pos + 3] == "e" and self.text[self.pos + 4] == "a" and self.text[self.pos + 5] == "t" and (self.pos + 6 == len(self.text) or self.text[self.pos + 6] == " " or self.text[self.pos + 6] == "\n"):
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                return Token(tokens['repeat'],'repeat')

            # UNTIL
            elif self.current_char == "u" and self.text[self.pos +1] == "n" and self.text[self.pos + 2] == "t" and self.text[self.pos + 3] == "i" and self.text[self.pos + 4] == "l" and (self.pos + 5 == len(self.text) or self.text[self.pos + 5] == " " or self.text[self.pos + 5] == "\n"):
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                return Token(tokens['until'], 'until')

            # READ
            elif self.current_char == "r" and self.text[self.pos +1] == "e" and self.text[self.pos + 2] == "a" and self.text[self.pos + 3] == "d" and (self.pos + 4 == len(self.text) or self.text[self.pos + 4] == " " or self.text[self.pos + 4] == "\n"):
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                return Token(tokens['read'],'read')
            
            # WRITE
            elif self.current_char == "w" and self.text[self.pos +1] == "r" and self.text[self.pos + 2] == "i" and self.text[self.pos + 3] == "t" and self.text[self.pos + 4] == "e" and (self.pos + 5 == len(self.text) or self.text[self.pos + 5] == " " or self.text[self.pos + 5] == "\n"):
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                return Token(tokens['write'],'write')
            
            # ID
            elif self.current_char.isalpha():
                result = self.current_char
                self.advance()

                while self.current_char.isalpha() or self.current_char.isnumeric():
                    result += self.current_char
                    self.advance()
                return Token(tokens['ID'],result)
            
            # NUM
            elif self.current_char.isnumeric():
                result = self.current_char
                self.advance()
                while self.current_char.isnumeric():
                    result += self.current_char
                    self.advance()
                return Token(tokens['NUM'],result)

            # Comemnt
            elif self.current_char == "{":
                while self.current_char != "}":
                    self.advance()
                self.advance()
            
            else:
                self.error()


# def read_file(filename):
#     with open(filename, 'r') as file:
#         return file.read()

# lex = Lexer(read_file('test2.txt'))
        

# # write into file
# def write_file(filename, text):
#     with open(filename, 'w') as file:
#         s = ""
#         vals = []
#         types = []
#         while lex.pos < len(lex.text):
#             token = lex.get_next_token()
#             s += token.__str__()
#             print(token)
#             vals.append(token.value)
#             types.append(token.type)
#             file.write(token.__str__())

# write_file('output.txt', lex)
