#TOKENS
###############################################

DIGITS = '0123456789'

INT_LIT             = 'INT_LIT'
# FLOAT_LIT           = 'FLOAT_LIT'
IDENT               = 'IDENT'
ASSIGN_OP           = 'ASSIGN_OP'
ADD_OP              = 'ADD_OP'
SUB_OP              = 'SUB_OP'
MULT_OP             = 'MULT_OP'
DIV_OP              = 'DIV_OP'
LEFT_PAREN          = 'LEFT_PAREN'
RIGHT_PAREN         = 'RIGHT_PAREN'
MOD_OP              = 'MOD_OP'
# COMMA               = 'COMMA'd
# SEMICOLON           = 'SEMICOLON'
# LEFT_BRACK          = 'LEFT_BRACK'
# RIGHT_BRACK         = 'RIGHT_BRACK'
# DOT                 = 'DOT'
LESS_THAN           = 'LESS_THAN'
GREATER_THAN        = 'GREATER_THAN'
LESS_THAN_EQUAL     = 'LESS_THAN_EQUAL'
GREATER_THAN_EQUAL  = 'GREATER_THAN_EQUAL'


class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: 
            return f'{self.type}: {self.value}'
        return f'{self.type}'

#LEXER
###############################################

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        # self.next_pos = 0
        self.curr_char = None
        # self.next_char = None
        self.advance()
    
    def advance(self):
        self.pos += 1
        # self.next_pos += 1
        # if self.next_pos < (len(self.text) + 1):
        #     self.next_char = self.text[self.next_pos] 
        # else:
        #     None

        self.curr_char = self.text[self.pos] if self.pos < len(self.text) else None

    def tokenize(self):
        tokens = []

        while self.curr_char != None:
            if self.curr_char in DIGITS:
                tokens.append(self.numberize())

            # if self.curr_char.isalpha():
            #     self.advance()
            #     while self.curr_char.isalpha() or self.curr_char in DIGITS:
            #         self.advance()
            #     tokens.append(Token(IDENT))
            else:    
                match self.curr_char:
                    case ' ':
                        self.advance()
                    case '\t':
                        self.advance()
                    case '+':
                        tokens.append(Token(ADD_OP, None))
                        self.advance()
                    case '-':
                        tokens.append(Token(SUB_OP, None))
                        self.advance()
                    case '*':
                        tokens.append(Token(MULT_OP, None))
                        self.advance()
                    case '/':
                        tokens.append(Token(DIV_OP, None))
                        self.advance()
                    case '%':
                        tokens.append(Token(MOD_OP, None))
                        self.advance()
                    case '<':
                        self.advance()
                        if self.curr_char == '=':
                            tokens.append(Token(LESS_THAN_EQUAL, None))
                            self.advance()
                        else:
                            tokens.append(Token(LESS_THAN, None))
                            self.advance()
                    case '>':
                        self.advance()
                        if self.curr_char == '=':
                            tokens.append(Token(GREATER_THAN_EQUAL, None))
                            self.advance()
                        else:
                            tokens.append(Token(GREATER_THAN, None))
                            self.advance()
                    # case '!':
                    #     if self.next_char == '=':
                    #         tokens.append(Token(GREATER_THAN_EQUAL))
                    #         self.advance()
                    #         self.advance()
                    #     else:
                    #         pass # <-- add code to handle '!' as an error
                    case _:
                        self.advance()

                        





        return tokens

    def numberize(self):
        num_str = ""
        while self.curr_char != None and self.curr_char in DIGITS:
            num_str += self.curr_char
            self.advance()
        return Token(INT_LIT, int(num_str))


def run(text):
    lexer = Lexer(text)
    tokens = lexer.tokenize()
    return tokens