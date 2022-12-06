####################### TOKENS #######################

DIGITS              = '0123456789'
ALPHAS              = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'

INT_LIT             = 'INT_LIT'
# FLOAT_LIT           = 'FLOAT_LIT'
IDENT               = 'IDENT'

ASSIGN_OP           = '='
ADD_OP              = '+'
SUB_OP              = '-'
MULT_OP             = '*'
DIV_OP              = '/'
LEFT_PAREN          = '('
RIGHT_PAREN         = ')'
MOD_OP              = '%'
# COMMA               = ','
SEMICOLON           = ';'
LEFT_BRACK          = '{'
RIGHT_BRACK         = '}'
# DOT                 = '.'
LESS_THAN           = '<'
GREATER_THAN        = '>'
LESS_THAN_EQUAL     = '<='
GREATER_THAN_EQUAL  = '>='
EQUAL_TO            = '=='
NOT_EQUAL_TO        = '!='
# NOT                 = '!'

YOINKY              = 'YOINKY' # start of program
SPLOINKY            = 'SPLOINKY' #end of program

NOCAP               = 'NOCAP' # true boolean keyword
CAP                 = 'CAP' # false keyword
CHECK               = 'CHECK' # if keyword
CASH                = 'CASH'  # else keyword
START               = 'START' # while keyword
GIVEN               = 'GIVEN' # for keyword



class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: 
            return f'{self.type}: {self.value}'
        return f'{self.type}'

class Error:
    def __init__(self, error_name):
        self.error_name = error_name

    def to_string(self):
        result = f'{self.error_name}: {self.details}'
        return result

class IllegalCharError(Error):
    def __init__(self):
        super().__init__('Illegal Character')

####################### LEXER #######################

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.curr_char = None
        self.advance()
    
    def advance(self):
        self.pos += 1
        self.curr_char = self.text[self.pos] if self.pos < len(self.text) else None

    def tokenize(self):
        tokens = []

        while self.curr_char != None:
            # integer literal conditions
            if self.curr_char in DIGITS:
                num_str = ""
                while self.curr_char != None and self.curr_char in DIGITS:
                    num_str += self.curr_char
                    self.advance()
                tokens.append(Token(INT_LIT, int(num_str)))

            # identifier and keyword conditions
            elif self.curr_char in ALPHAS:
                str_str = ""
                while self.curr_char != None and (self.curr_char in ALPHAS or self.curr_char in DIGITS):
                    str_str += self.curr_char
                    self.advance()
                if str_str == "check":
                    tokens.append(Token(CHECK, None))
                elif str_str == "cash":
                    tokens.append(Token(CASH, None))
                elif str_str == "start":
                    tokens.append(Token(START, None))
                elif str_str == "given":
                    tokens.append(Token(GIVEN, None))
                elif str_str == "NOCAP":
                    tokens.append(Token(NOCAP, None))
                elif str_str == "CAP":
                    tokens.append(Token(CAP, None))
                elif str_str == "YOINKY":
                    tokens.append(Token(YOINKY, None))
                elif str_str == "SPLOINKY":
                    tokens.append(Token(SPLOINKY, None))
                else:
                    tokens.append(Token(IDENT, None))

            # all other tokens conditions
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
                    case '>':
                        self.advance()
                        if self.curr_char == '=':
                            tokens.append(Token(GREATER_THAN_EQUAL, None))
                            self.advance()
                        else:
                            tokens.append(Token(GREATER_THAN, None))

                    case '=':
                        self.advance()
                        if self.curr_char == '=':
                            tokens.append(Token(EQUAL_TO, None))
                            self.advance()
                        else:
                            tokens.append(Token(ASSIGN_OP, None))
                    case '!':
                        self.advance()
                        if self.curr_char == '=':
                            tokens.append(Token(NOT_EQUAL_TO, None))
                            self.advance()
                        else:
                            return self.error(self.curr_char)
                    case ';':
                        tokens.append(Token(SEMICOLON, None))
                        self.advance()
                    case '{':
                        tokens.append(Token(LEFT_BRACK, None))
                        self.advance()
                    case '}':
                        tokens.append(Token(RIGHT_BRACK, None))
                        self.advance()
                    case _:
                        return IllegalCharError()
        return tokens
        



####################### RUNNER #######################

def run(text):
    lexer = Lexer(text)
    tokens = lexer.tokenize()
    return tokens