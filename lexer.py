####################### TOKENS #######################

DIGITS              = '0123456789'
ALPHAS              = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
INT_LIT               = 'INT_LIT'
INT_LIT_1             = 'INT_LIT_1'
INT_LIT_2             = 'INT_LIT_2'
INT_LIT_4             = 'INT_LIT_4'
INT_LIT_8             = 'INT_LIT_8'

# FLOAT_LIT           = 'FLOAT_LIT'
IDENT               = 'IDENT'

ASSIGN_OP           = '='
ADD_OP              = '*'
SUB_OP              = '-'
MULT_OP             = '+'
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

NEW_LINE            = "NEW_LINE"

YOINKY              = 'YOINKY' # start of program
SPLOINKY            = 'SPLOINKY' #end of program

NOCAP               = 'NOCAP' # true boolean keyword
CAP                 = 'CAP' # false keyword
CHECK               = 'CHECK' # if keyword
CASH                = 'CASH'  # else keyword
START               = 'START' # while keyword
GIVEN               = 'GIVEN' # for keyword



class Token:
    def __init__(self, type_, value = None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: 
            return f'{self.type}: {self.value}'
        return f'{self.type}'


####################### ERRORS #######################


class Error:
    def __init__(self, err_start, err_end, error_name, details):
        self.err_start = err_start
        self.err_end = err_end
        self.error_name = error_name
        self.details = details

    def to_string(self):
        result = f'{self.error_name}: {self.details} in {self.err_start.filename}, line {self.err_start.length +1}'
        return result

class IllegalCharError(Error):
    def __init__(self, err_start, err_end, details):
        super().__init__(err_start, err_end, 'Illegal Character', details)

class IllegalVarLenError(Error):
    def __init__(self, err_start, err_end, details):
        super().__init__(err_start, err_end, 'Illegal Variable Length', details)

class SyntaxError(Error):
    def __init__(self, details):
        super().__init__('Illegal Syntax', details)


####################### POSITION #######################

class Position:
    def __init__(self, index, length, column, filename, text):
        self.index = index
        self.length = length
        self.column = column
        self.filename = filename
        self.text = text
    
    def advance(self, curr_char):
        self.index += 1
        self.column += 1

        if curr_char == '\n':
            self.length += 1
            self.column += 0

        return self

    def copy(self):
        return Position(self.index, self.length, self.column, self.filename, self.text)



####################### LEXER #######################

class Lexer:
    def __init__(self, filename, text):
        self.filename = filename
        self.text = text
        self.position = Position(-1, 0, -1, filename, text)
        self.curr_char = None
        self.advance()
    
    def advance(self):
        self.position.advance(self.curr_char)
        self.curr_char = self.text[self.position.index] if self.position.index < len(self.text) else None

    def tokenize(self):
        tokens = []

        while self.curr_char != None:
            # integer literal conditions
            if self.curr_char.isnumeric(): 
                num_str = ""
                while self.curr_char != None and self.curr_char in DIGITS:
                    num_str += self.curr_char
                    self.advance()
                if self.curr_char == '_':
                    self.advance()
                    if self.curr_char == '1': tokens.append(Token(INT_LIT_1, int(num_str)))
                    elif self.curr_char == '2': tokens.append(Token(INT_LIT_2, int(num_str)))
                    elif self.curr_char == '4': tokens.append(Token(INT_LIT_4, int(num_str)))
                    elif self.curr_char == '8': tokens.append(Token(INT_LIT_8, int(num_str)))
                else: tokens.append(Token(INT_LIT, int(num_str)))

            # identifier and keyword conditions
            elif self.curr_char.isalpha():
                str_str = ""
                while self.curr_char != None and (self.curr_char in ALPHAS or self.curr_char in DIGITS): 
                    str_str += self.curr_char 
                    self.advance()
                if len(str_str) > 8 or len(str_str) < 6:
                    self.err_start = self.position.copy()
                    char = self.curr_char
                    self.advance()
                    return [], IllegalVarLenError(self.err_start, self.position, '"str_str"')
                if str_str == "check": tokens.append(Token(CHECK, None))
                elif str_str == "cash": tokens.append(Token(CASH, None))
                elif str_str == "start": tokens.append(Token(START, None))
                elif str_str == "given": tokens.append(Token(GIVEN, None))
                elif str_str == "NOCAP": tokens.append(Token(NOCAP, None))
                elif str_str == "CAP": tokens.append(Token(CAP, None))
                elif str_str == "YOINKY": tokens.append(Token(YOINKY, None))
                elif str_str == "SPLOINKY": tokens.append(Token(SPLOINKY, None))
                else: tokens.append(Token(IDENT, None))

            # all other tokens conditions
            else:    
                match self.curr_char:
                    case ' ':   self.advance()
                    case '\t':  self.advance()
                    case '\n':  tokens.append(Token(NEW_LINE, None)), self.advance()
                    case '*':   tokens.append(Token(ADD_OP, None)), self.advance()
                    case '-':   tokens.append(Token(SUB_OP, None)), self.advance()
                    case '+':   tokens.append(Token(MULT_OP, None)), self.advance()
                    case '/':   tokens.append(Token(DIV_OP, None)), self.advance()
                    case '%':   tokens.append(Token(MOD_OP, None)), self.advance()
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
                        self.err_start = self.position.copy()
                        char = self.curr_char
                        self.advance()
                        return [], IllegalCharError(self.err_start, self.position, char)
        return tokens, None


####################### RUNNER #######################

def run(filename, text):
    lexer = Lexer(filename, text)
    tokens, error = lexer.tokenize()
    return tokens, error


    