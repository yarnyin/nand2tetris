import enum
from glob import glob
from os import curdir
import sys
from tokenize import Token


from zmq import PROTOCOL_ERROR_ZMTP_CRYPTOGRAPHIC

# from pygments import lex
BUF_SZ = 8192
class LEX_ST(enum.Enum):
    NON     = -1
    PRECMT  = 0
    CMT1    = 1
    CMT2    = 2
    WORD    = 3
    CONSTR  = 4
    LCMT2   = 5

class TOKEN_TYPE(enum.Enum):
    NON          = 0
    KEYWORD      = 1
    IDENTIFIER   = 2
    INT_CONST    = 3
    SYMBOL       = 4
    STRING_CONST = 5

strTokenType = {
    TOKEN_TYPE.NON: "NON",
    TOKEN_TYPE.KEYWORD: "</keyword>",
    TOKEN_TYPE.IDENTIFIER: "</identifier>",
    TOKEN_TYPE.INT_CONST:   "</integerConstant>",
    TOKEN_TYPE.SYMBOL:  "</symbol>",
    TOKEN_TYPE.STRING_CONST: "</stringConstant>",
}
# a="<abc>"
# a.

syms = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']
keywords = {'class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int',
            'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if',
            'else', 'while', 'return'}

class tokenizer:
    def __init__(self, input_file) -> None:
        self.input_file = open(input_file, "r")
        self.current_token = ""
        self.token_type = TOKEN_TYPE.NON
        self.rd_buf = self.input_file.read(BUF_SZ)
        self.buf_sz = len(self.rd_buf)
        self.rd_idx = 0
        self.advance()
        # self.lex_st = LEX_ST.NON

    def has_more_tokens(self):
        pass


    def advance(self):
        self.current_token = ""
        lex_st = LEX_ST.NON
        self.token_type = TOKEN_TYPE.NON
        get_tok = False
        while self.rd_buf and not get_tok:
            while self.rd_idx < self.buf_sz and not get_tok:
                cur_chr = self.rd_buf[self.rd_idx]
                self.rd_idx += 1
                if lex_st == LEX_ST.NON:
                    if cur_chr == '/':
                        lex_st = LEX_ST.PRECMT
                    elif cur_chr in syms:
                        self.token_type = TOKEN_TYPE.SYMBOL
                        self.current_token += cur_chr
                        get_tok = True
                    elif cur_chr.isspace():
                        pass
                    elif cur_chr.isalnum() or cur_chr == '_':
                        self.current_token += cur_chr
                        lex_st = LEX_ST.WORD
                    elif cur_chr == '"':
                        self.token_type = TOKEN_TYPE.STRING_CONST
                        lex_st = LEX_ST.CONSTR
                    else:
                        print("Unexpected character")
                        exit(-1)
                
                elif lex_st == LEX_ST.WORD:
                    if cur_chr.isalnum() or cur_chr == '_':
                        self.current_token += cur_chr
                    elif (cur_chr.isspace()) or (cur_chr in syms):
                        get_tok = True
                        self.rd_idx -= 1
                    else:
                        print("Unexpected character")
                        exit(-1)
                
                elif lex_st == LEX_ST.CONSTR:
                    if cur_chr == '"':
                        get_tok = True
                    else:
                        self.current_token += cur_chr
                
                elif lex_st == LEX_ST.PRECMT:
                    if cur_chr == '/':
                        lex_st = LEX_ST.CMT1
                    elif cur_chr == '*':
                        lex_st = LEX_ST.CMT2
                    elif (cur_chr.isspace()) or (cur_chr in syms):
                        self.token_type = TOKEN_TYPE.SYMBOL
                        self.current_token += "/"
                        self.rd_idx -= 1
                        get_tok = True
                    else:
                        print("Unexpected character")
                        exit(-1)

                elif lex_st == LEX_ST.CMT1:
                    if cur_chr == '\n':
                        lex_st = LEX_ST.NON

                elif lex_st == LEX_ST.CMT2:
                    if cur_chr == '*':
                        lex_st = LEX_ST.LCMT2
                
                elif lex_st == LEX_ST.LCMT2:
                    if cur_chr == "/":
                        lex_st = LEX_ST.NON
                    else:
                        lex_st = LEX_ST.CMT2

            if self.rd_idx == self.buf_sz:
                self.rd_buf = self.input_file.read(BUF_SZ)
                self.buf_sz = len(self.rd_buf)
                self.rd_idx = 0
        if self.token_type == TOKEN_TYPE.NON and self.current_token:
            self.handle_tok()
        else:# sym or const_string
            self.current_token = self.current_token.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', "&quot;")



    def handle_tok(self):
        if self.current_token in keywords:
            self.token_type = TOKEN_TYPE.KEYWORD
        elif self.current_token.isdigit():
            self.token_type = TOKEN_TYPE.INT_CONST
        elif not self.current_token[0].isdigit():
            self.token_type = TOKEN_TYPE.IDENTIFIER
        else:
            print("ERROR")
            exit(-1)
    def token_type(self):
        pass
    def int_val(self):
        pass
    def string_val(self):
        pass
    pass

class compliation:
    def __init__(self, input_file) -> None:
        self.tknz = tokenizer(input_file)
        self.input_file = input_file
        self.output_file = open(input_file.replace(".jack", ".xml"), "w")
        self.level = 0
        self.compile_class()
        # compile_class()
    
    def output(self, line):
        self.output_file.write('  '*self.level + line + '\n')
    
    def eat(self, word):
        if self.tknz.current_token == word:
            self.output(strTokenType[self.tknz.token_type].replace('/', '') + ' ' + self.tknz.current_token + ' ' + strTokenType[self.tknz.token_type])
            self.tknz.advance()
        else:
            print("EAT ERROR")
            print("word = ", word)
            print("current_token = ", self.tknz.current_token)
            exit(-1)
        pass
    def compile_class(self):
        self.output("<class>")
        self.level += 1
        self.eat("class")
        # self.compile_term()
        if not self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
            print("CLASS ERROR")
            exit(-1)
        self.eat(self.tknz.current_token)
        self.eat("{")
        while self.tknz.current_token:
            if self.tknz.current_token in ('field', "static") and self.tknz.token_type == TOKEN_TYPE.KEYWORD:
                self.output("<classVarDec>")
                self.level += 1
                self.compile_class_var_dec()
                self.level -= 1
                self.output("</classVarDec>")

            elif self.tknz.current_token in ('method', 'function', 'constructor') and self.tknz.token_type == TOKEN_TYPE.KEYWORD:
                self.output("<subroutineDec>")
                self.level += 1
                self.compile_subroutine_dec()
                self.level -= 1
                self.output("</subroutineDec>")
            else:
                self.eat("}")
        self.level -= 1
        self.output("</class>")


    def compile_class_var_dec(self):
        self.eat(self.tknz.current_token)
        if self.tknz.current_token in ('int', 'char', 'boolean') or self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
            self.eat(self.tknz.current_token)
            if self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
                self.eat(self.tknz.current_token)
                while self.tknz.current_token:
                    if self.tknz.current_token == ',':
                        self.eat(',')
                        if self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
                            self.eat(self.tknz.current_token)
                        else:
                            print("class var error")
                            exit(-1)
                    elif self.tknz.current_token == ';':
                        self.eat(';')
                        break
                    else:
                        print("class var error")
                        exit(-1)
            else:
                print("class var error")
                exit(-1)

        else:
            print("class var error")
            exit(-1)

    def compile_subroutine_dec(self):
        self.eat(self.tknz.current_token)
        if self.tknz.current_token in ('int', 'char', 'boolean', 'void') or self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
            self.eat(self.tknz.current_token)
            if self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
                self.eat(self.tknz.current_token)
                # self.eat('(')
                self.compile_parameter_list()
                self.compile_subroutine_body()
            else:
                print('subroutine error')
                exit(-1)
        
        else:
            print("subroutine error")
            exit(-1)
        pass
    def compile_parameter_list(self):
        self.eat('(')
        self.output('<parameterList>')
        self.level += 1
        while self.tknz.token_type == TOKEN_TYPE.IDENTIFIER or self.tknz.current_token in ('int', 'char', 'boolean'):
            self.eat(self.tknz.current_token)
            if self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
                self.eat(self.tknz.current_token)
            else:
                print("parameter error")
                exit(-1)

            if self.tknz.token_type == TOKEN_TYPE.SYMBOL and self.tknz.current_token == ',':
                self.eat(',')
            else:
                break
        self.level -= 1
        self.output('</parameterList>')
        self.eat(')')
        pass
    def compile_subroutine_body(self):
        self.output('<subroutineBody>')
        self.level += 1
        self.eat('{')
        while self.tknz.current_token == "var" and self.tknz.token_type == TOKEN_TYPE.KEYWORD:
            self.compile_var_dec()
        self.compile_statements()
        self.eat('}')
        self.level -= 1
        self.output('</subroutineBody>')
        pass

    def compile_var_dec(self):
        self.output('<varDec>')
        self.level += 1
        self.eat('var')
        if self.tknz.current_token in ('int', 'char', 'boolean') or self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
            self.eat(self.tknz.current_token)
        else:
            print('var dec error')
            exit(-1)

        if self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
            while self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
                self.eat(self.tknz.current_token)
                if self.tknz.token_type == TOKEN_TYPE.SYMBOL and self.tknz.current_token == ',':
                    self.eat(',')
                else:
                    break
        else:
            print('var dec error')
            exit(-1)
        self.eat(';')
        self.level -= 1
        self.output('</varDec>')

    def compile_statements(self):
        self.output('<statements>')
        self.level += 1
        while self.tknz.current_token in ('let', 'if', 'while', 'do', 'return') and self.tknz.token_type == TOKEN_TYPE.KEYWORD:
            if self.tknz.current_token == "let":
                self.compile_let_statement()
            elif self.tknz.current_token == "if":
                self.compile_if_statement()
            elif self.tknz.current_token == "while":
                self.compile_while_statement()
            elif self.tknz.current_token == "do":
                self.compile_do_statement()
            elif self.tknz.current_token == "return":
                self.compile_return_expression()
        self.level -= 1
        self.output('</statements>')


    def compile_return_expression(self):
        self.output('<returnStatement>')
        self.level += 1
        self.eat('return')
        if self.tknz.token_type != TOKEN_TYPE.SYMBOL:
            self.compile_expression()
        self.eat(';')
        self.level -= 1
        self.output('</returnStatement>')


    def compile_do_statement(self):
        self.output('<doStatement>')
        self.level += 1
        self.eat('do')
        if self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
            self.eat(self.tknz.current_token)
            if self.tknz.token_type == TOKEN_TYPE.SYMBOL:
                if self.tknz.current_token == '(':
                    self.eat('(')
                    self.compile_expression_list()
                    self.eat(')')
                elif self.tknz.current_token == '.':
                    self.eat('.')
                    if self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
                        self.eat(self.tknz.current_token)
                        self.eat('(')
                        self.compile_expression_list()
                        self.eat(')')
                else:
                    print("do statement error")
                    exit(-1)
            else:
                print("do statement error")
                exit(-1)
        else:
            print('do statement error')
            exit(-1)
        self.eat(';')
        self.level -= 1
        self.output('</doStatement>')
    

    def compile_let_statement(self):
        self.output('<letStatement>')
        self.level += 1
        self.eat('let')
        if self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
            self.eat(self.tknz.current_token)
        else:
            print("let statement error")
            exit(-1)
        if self.tknz.token_type == TOKEN_TYPE.SYMBOL:
            if self.tknz.current_token == '[':
                self.eat('[')
                self.compile_expression()
                self.eat(']')
            # elif  self.tknz.current_token == '=':
            #     self.compile_expression()
        else:
            print("let statement error")
            exit(-1)
        if self.tknz.token_type == TOKEN_TYPE.SYMBOL:
            self.eat('=')
            self.compile_expression()
        else:
            print('let statement error')
            exit(-1)
        self.eat(';')
        self.level -= 1
        self.output('</letStatement>')



    def compile_if_statement(self):
        self.output('<ifStatement>')
        self.level += 1
        self.eat('if')
        self.eat('(')
        self.compile_expression()
        self.eat(')')
        self.eat('{')
        self.compile_statements()
        self.eat('}')
        if self.tknz.token_type == TOKEN_TYPE.KEYWORD and self.tknz.current_token == "else":
            self.eat('else')
            self.eat('{')
            self.compile_statements()
            self.eat('}')
        self.level -= 1
        self.output('</ifStatement>')


    def compile_while_statement(self):
        self.output('<whileStatement>')
        self.level += 1
        self.eat('while')
        self.eat('(')
        self.compile_expression()
        self.eat(')')
        self.eat('{')
        self.compile_statements()
        self.eat('}')
        self.level -= 1
        self.output('</whileStatement>')


    def compile_expression(self):
        self.output("<expression>")
        self.level += 1
        self.compile_term()
        # print("current_token = ", self.tknz.current_token)
        # print("token_type = ", self.tknz.token_type)
        while self.tknz.token_type == TOKEN_TYPE.SYMBOL and self.tknz.current_token in ('+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '='):
            self.eat(self.tknz.current_token)
            self.compile_term()
        self.level -= 1
        self.output("</expression>")

    def compile_term(self):
        self.output('<term>')
        self.level += 1
        # print("current_token = ", self.tknz.current_token)
        # print("token_type = ", self.tknz.token_type)
        if self.tknz.token_type in (TOKEN_TYPE.INT_CONST, TOKEN_TYPE.STRING_CONST):
            self.eat(self.tknz.current_token)
        elif self.tknz.token_type == TOKEN_TYPE.KEYWORD:
            if self.tknz.current_token in ("true", "false", "null", "this"):
                self.eat(self.tknz.current_token)
            else:
                print("term error")
                exit(-1)
        elif self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
            self.eat(self.tknz.current_token)
            if self.tknz.token_type == TOKEN_TYPE.SYMBOL:
                if self.tknz.current_token == '[':
                    self.eat('[')
                    self.compile_expression()
                    self.eat(']')
                elif self.tknz.current_token == '(': #subroutine call
                    self.eat('(')
                    self.compile_expression_list()
                    self.eat(')')
                elif self.tknz.current_token == '.':#sub routine call
                    self.eat('.')
                    if self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
                        self.eat(self.tknz.current_token)
                        self.eat('(')
                        self.compile_expression_list()
                        self.eat(')')
                    else:
                        print("term error")
                        exit(-1)
        elif self.tknz.token_type == TOKEN_TYPE.SYMBOL:
            if self.tknz.current_token == '(':
                self.eat('(')
                self.compile_expression()
                self.eat(')')
            elif self.tknz.current_token in ('-', '~'):
                self.eat(self.tknz.current_token)
                self.compile_term()
            else:
                print("term error")
                exit(-1)
        else:
            print("term error")
            exit(-1)
        self.level -= 1
        self.output('</term>')
        pass


    def compile_expression_list(self):
        self.output("<expressionList>")
        self.level += 1
        if not (self.tknz.token_type == TOKEN_TYPE.SYMBOL and self.tknz.current_token == ')'):
            self.compile_expression()
            while self.tknz.token_type == TOKEN_TYPE.SYMBOL and self.tknz.current_token == ',':
                self.eat(',')
                self.compile_expression()
        self.level -= 1
        self.output("</expressionList>")
        pass

def get_files(file_or_dir):
    if file_or_dir.endswith('.jack'):
        return [file_or_dir]
    else:
        return glob(file_or_dir + "/*.jack")

def main():
    in_files = get_files(sys.argv[1])
    for f in in_files:
        print(f)
        com = compliation(f)
        com.output_file.close()

def lex_test():
    # in_file = open(sys.argv[1], "r")
    # buf = in_file.read(1)
    tknd = tokenizer(sys.argv[1])
    while tknd.current_token:
        print(tknd.current_token, strTokenType[tknd.token_type])
        # print(tknd.rd_idx)
        tknd.advance()



if __name__ == "__main__":
    # lex_test()
    main()