from asyncio import constants
import enum
from glob import glob
import sys

import outcome

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

# glb_counters = {
#     'WHILE_EXP':0,
#     'WHILE_END':0,
#     'IF_TRUE':0,
#     'IF_FALSE':0,
# }


class sym_entry:
    def __init__(self, typ, kind, idx):
        self.type = typ
        self.kind = kind
        self.idx = idx

class sym_table:
    def __init__(self):
        self.table = {}
        self.kind_num = {"this":0, "static":0, "argument":0, "local":0}
    
    def append(self, name, typ, kind):
        self.table.update({name:sym_entry(typ, kind, self.kind_num[kind])})
        self.kind_num[kind] += 1
    
    def clear(self):
        self.table.clear()
        self.kind_num = {"this":0, "static":0, "argument":0, "local":0}

    # def get_entry(self, name):
    #     if name in self.table

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

class code_writer:
    def __init__(self, f_name):
        self.output_file = open(f_name, 'w')
    
    def write(self, code):
        self.output_file.write(code + '\n')
    
    def write_push(self, segment, index):#push constant/arg/local/this/that 1
        # self.output_file.write("push ...")
        self.write("push " + segment +  ' ' + str(index))
        pass
    
    def write_pop(self, segment, index):#pop arg/local/this/that 1
        self.write("pop " + segment + ' ' + str(index))

    def write_arithmetic(self, command):#add/sub/neg/eq/gt/lt/and/or/not
        if command == '+':
            self.write("add")
        elif command == '-':
            self.write('sub')
        elif command == '*':
            self.write("call Math.multiply 2")
        elif command == '/':
            self.write("call Math.divide 2")
        elif command == '&amp;':
            self.write("and")
        elif command == '|':
            self.write("or")
        elif command == '&lt;':
            self.write('lt')
        elif command == '&gt;':
            self.write('gt')
        elif command == '=':
            self.write('eq')


    def write_label(self, label):
        self.write("label " + label)

    def write_goto(self, label):
        self.write('goto ' + label)

    def write_if(self, label): #if-goto
        self.write('if-goto ' + label)

    def write_unary(self, unary):
        if unary == '-':
            self.write('neg')
        else:
            self.write('not')

    def write_call(self, name, nargs):#call manipulate 3
        self.write('call ' + name + ' ' + str(nargs))

    def write_function(self, name, nlocals):#function manipulate 2
        self.write("function " + name + ' '+ str(nlocals))

    def write_return(self):
        self.write("return")

    def close(self):
        self.close()

class compliation:
    def __init__(self, input_file):
        self.tknz = tokenizer(input_file)
        self.class_name = ''.join(input_file.split("\\")[-1].split(".")[:-1])
        # self.output_file = open(input_file.replace(".jack", ".xml"), "w")
        self.output_file = 0
        self.code_writer = code_writer(input_file.replace(".jack", ".vm"))
        self.level = 0
        self.class_sym = sym_table()
        self.subroutine_sym = sym_table()
        self.func_lbl  = {
            'WHILE_EXP':0,
            'WHILE_END':0,
            'IF_TRUE':0,
            'IF_FALSE':0,
            'IF_END':0,
        }
        self.compile_class()
        # compile_class()

    def get_entry(self, name):
        if name in self.subroutine_sym.table.keys():
            return self.subroutine_sym.table[name]
        elif name in self.class_sym.table.keys():
            return self.class_sym.table[name]
        else:
            print("resolve sym error!")
            exit(-1)
    
    def output(self, line):
        # self.output_file.write('  '*self.level + line + '\n')
        pass
    
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
        kind = self.tknz.current_token
        if kind == 'field':
            kind = 'this'
        self.eat(self.tknz.current_token)
        if self.tknz.current_token in ('int', 'char', 'boolean') or self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
            typ = self.tknz.current_token
            self.eat(self.tknz.current_token)
            if self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
                name = self.tknz.current_token
                self.class_sym.append(name, typ, kind)
                self.eat(self.tknz.current_token)
                while self.tknz.current_token:
                    if self.tknz.current_token == ',':
                        self.eat(',')
                        if self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
                            name = self.tknz.current_token
                            self.class_sym.append(name, typ, kind)
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
        self.func_typ = self.tknz.current_token
        self.subroutine_sym.clear()
        self.func_lbl  = {
            'WHILE_EXP':0,
            'WHILE_END':0,
            'IF_TRUE':0,
            'IF_FALSE':0,
            'IF_END':0,
        }
        self.eat(self.tknz.current_token)
        if self.tknz.current_token in ('int', 'char', 'boolean', 'void') or self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
            self.eat(self.tknz.current_token)
            if self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
                func_name = self.class_name + '.' + self.tknz.current_token
                self.eat(self.tknz.current_token)
                # self.eat('(')
                self.compile_parameter_list()
                self.compile_subroutine_body(func_name)
                # self.code_writer.write_function(func_name, self.subroutine_sym.kind_num['local'])
            else:
                print('subroutine error')
                exit(-1)
        
        else:
            print("subroutine error")
            exit(-1)
        pass
    
    def compile_parameter_list(self):
        kind = "argument"
        #method
        if self.func_typ == "method":
            self.subroutine_sym.kind_num[kind] = 1
            # pass
        self.eat('(')
        self.output('<parameterList>')
        self.level += 1
        while self.tknz.token_type == TOKEN_TYPE.IDENTIFIER or self.tknz.current_token in ('int', 'char', 'boolean'):
            typ = self.tknz.current_token
            self.eat(self.tknz.current_token)
            if self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
                name = self.tknz.current_token
                self.subroutine_sym.append(name, typ, kind)
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

    def compile_subroutine_body(self, func_name):
        self.output('<subroutineBody>')
        self.level += 1
        self.eat('{')
        while self.tknz.current_token == "var" and self.tknz.token_type == TOKEN_TYPE.KEYWORD:
            self.compile_var_dec()
        self.code_writer.write_function(func_name, self.subroutine_sym.kind_num['local'])
        if self.func_typ == 'method':
            self.code_writer.write_push("argument", 0)
            self.code_writer.write_pop("pointer", 0) # set this pointer
        elif self.func_typ == 'constructor':
            self.code_writer.write_push("constant", self.class_sym.kind_num['this'])
            self.code_writer.write_call("Memory.alloc", 1)
            self.code_writer.write_pop("pointer", 0)
        self.compile_statements()
        self.eat('}')
        self.level -= 1
        self.output('</subroutineBody>')
        pass

    def compile_var_dec(self):
        kind = "local"
        self.output('<varDec>')
        self.level += 1
        self.eat('var')
        if self.tknz.current_token in ('int', 'char', 'boolean') or self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
            typ = self.tknz.current_token
            self.eat(self.tknz.current_token)
        else:
            print('var dec error')
            exit(-1)

        if self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
            while self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
                name = self.tknz.current_token
                self.subroutine_sym.append(name, typ, kind)
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
        if not (self.tknz.token_type == TOKEN_TYPE.SYMBOL and self.tknz.current_token == ';'):
            self.compile_expression()
        else:
            self.code_writer.write_push("constant", 0)
        self.eat(';')
        self.level -= 1
        self.output('</returnStatement>')
        self.code_writer.write_return()


    def compile_do_statement(self):
        n_args = 0
        self.output('<doStatement>')
        self.level += 1
        self.eat('do')
        if self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
            func_name = self.tknz.current_token
            # obj_name = self.tknz.current_token
            self.eat(self.tknz.current_token)
            if self.tknz.token_type == TOKEN_TYPE.SYMBOL:
                if self.tknz.current_token == '(':#this.method call
                    self.eat('(')
                    func_name = self.class_name + '.' + func_name
                    self.code_writer.write_push("pointer", 0) #push this
                    n_args += 1
                    n_args += self.compile_expression_list()
                    self.eat(')')
                elif self.tknz.current_token == '.': #method or class func
                    self.eat('.')
                    # if func_name in self.subroutine_sym.table.keys() or func_name in self.class_sym.table.keys():#method
                    #     entry = self.get_entry(func_name)
                    #     class_name = entry.type
                    #     #push 
                    #     self.code_writer.write_push(entry.kind, entry.idx)
                    #     func_name = 
                    # else:#class func
                    #     class_name = func_name
                    if self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
                        if func_name in self.subroutine_sym.table.keys() or func_name in self.class_sym.table.keys():#method
                            entry = self.get_entry(func_name)
                            func_name = entry.type + '.' + self.tknz.current_token
                            self.code_writer.write_push(entry.kind, entry.idx)
                            n_args += 1
                        else:#class func
                            func_name += '.' + self.tknz.current_token
                        self.eat(self.tknz.current_token)
                        self.eat('(')
                        n_args += self.compile_expression_list()
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
        self.code_writer.write_call(func_name, n_args)
        self.code_writer.write_pop("temp", 0)
    

    def compile_let_statement(self):
        self.output('<letStatement>')
        self.level += 1
        self.eat('let')
        if self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
            dst_name = self.tknz.current_token
            self.eat(self.tknz.current_token)
        else:
            print("let statement error")
            exit(-1)
        if self.tknz.token_type == TOKEN_TYPE.SYMBOL:
            entry = self.get_entry(dst_name)
            if self.tknz.current_token == '[': #array
                self.code_writer.write_push(entry.kind, entry.idx)
                self.eat('[')
                self.compile_expression()
                self.code_writer.write_arithmetic('+')
                self.eat(']')
                self.eat('=')
                self.compile_expression()
                self.code_writer.write_pop("temp", 0)
                self.code_writer.write_pop("pointer", 1) #set that
                self.code_writer.write_push("temp", 0)
                self.code_writer.write_pop("that", 0)
            # elif  self.tknz.current_token == '=':
            #     self.compile_expression()
            elif self.tknz.token_type == TOKEN_TYPE.SYMBOL:
                self.eat('=')
                self.compile_expression()
                #pop dst
                # entry = self.get_entry(dst_name)
                self.code_writer.write_pop(entry.kind, entry.idx)
            else:
                print('let statement error')
                exit(-1)
        else:
            print("let statement error")
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
        if_true = 'IF_TRUE' + str(self.func_lbl['IF_TRUE'])
        if_false = 'IF_FALSE' + str(self.func_lbl['IF_FALSE'])
        if_end = 'IF_END' + str(self.func_lbl['IF_END'])
        self.func_lbl['IF_TRUE'] += 1
        self.func_lbl['IF_FALSE'] += 1
        self.func_lbl['IF_END'] += 1
        self.code_writer.write_if(if_true)
        self.code_writer.write_goto(if_false)
        self.code_writer.write_label(if_true)
        self.eat('{')
        self.compile_statements()
        self.eat('}')
        # self.code_writer.write_goto(if_end)
        if self.tknz.token_type == TOKEN_TYPE.KEYWORD and self.tknz.current_token == "else":
            self.code_writer.write_goto(if_end)
            self.eat('else')
            self.eat('{')
            self.code_writer.write_label(if_false)
            self.compile_statements()
            self.code_writer.write_label(if_end)
            self.eat('}')
        else:
            self.code_writer.write_label(if_false)
        self.level -= 1
        self.output('</ifStatement>')


    def compile_while_statement(self):
        self.output('<whileStatement>')
        self.level += 1
        self.eat('while')
        while_exp = "WHILE_EXP" + str(self.func_lbl['WHILE_EXP'])
        self.func_lbl['WHILE_EXP'] += 1
        self.code_writer.write_label(while_exp)
        self.eat('(')
        self.compile_expression()
        self.eat(')')
        self.code_writer.write_unary('~')
        while_end = "WHILE_END" + str(self.func_lbl['WHILE_END'])
        self.func_lbl['WHILE_END'] += 1
        self.code_writer.write_if(while_end)
        self.eat('{')
        self.compile_statements()
        self.code_writer.write_goto(while_exp)
        self.eat('}')
        self.code_writer.write_label(while_end)
        self.level -= 1
        self.output('</whileStatement>')


    def compile_expression(self):
        self.output("<expression>")
        self.level += 1
        self.compile_term()
        # print("current_token = ", self.tknz.current_token)
        # print("token_type = ", self.tknz.token_type)
        while self.tknz.token_type == TOKEN_TYPE.SYMBOL and self.tknz.current_token in ('+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '='):
            op = self.tknz.current_token
            self.eat(self.tknz.current_token)
            self.compile_term()
            self.code_writer.write_arithmetic(op)
        self.level -= 1
        self.output("</expression>")

    def compile_term(self):
        self.output('<term>')
        self.level += 1
        # print("current_token = ", self.tknz.current_token)
        # print("token_type = ", self.tknz.token_type)
        if self.tknz.token_type == TOKEN_TYPE.INT_CONST: #TOKEN_TYPE.STRING_CONST
            number = self.tknz.current_token
            self.code_writer.write_push("constant", number)
            self.eat(self.tknz.current_token)
        elif self.tknz.token_type == TOKEN_TYPE.STRING_CONST:
            str_con = self.tknz.current_token
            self.code_writer.write_push("constant", len(str_con))
            self.code_writer.write_call("String.new", 1)
            for chr in str_con:
                self.code_writer.write_push("constant", ord(chr))
                self.code_writer.write_call("String.appendChar", 2)
            self.eat(str_con)
        elif self.tknz.token_type == TOKEN_TYPE.KEYWORD:
            if self.tknz.current_token in ("true", "false", "null", "this"):
                kwd = self.tknz.current_token
                if kwd == "true":
                    self.code_writer.write_push('constant', 0)
                    self.code_writer.write_unary('~')
                elif kwd == "false" or kwd == "null":
                    self.code_writer.write_push('constant', 0)
                elif kwd == "this":
                    self.code_writer.write_push('pointer', 0)
                self.eat(self.tknz.current_token)
            else:
                print("term error")
                exit(-1)
        elif self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
            # n_args = 0
            name = self.tknz.current_token
            self.eat(self.tknz.current_token)
            if self.tknz.token_type == TOKEN_TYPE.SYMBOL:
                if self.tknz.current_token == '[': #array
                    entry = self.get_entry(name)
                    self.code_writer.write_push(entry.kind, entry.idx)
                    self.eat('[')
                    self.compile_expression()
                    self.code_writer.write_arithmetic('+')
                    self.eat(']')
                    self.code_writer.write_pop('pointer', 1)#set that
                    self.code_writer.write_push('that', 0)
                elif self.tknz.current_token == '(': #this.method call
                    self.eat('(')
                    name = self.class_name + '.' + name
                    self.code_writer.write_push('pointer', 0) #push this
                    n_args = self.compile_expression_list() + 1
                    self.eat(')')
                    self.code_writer.write_call(name, n_args)
                elif self.tknz.current_token == '.':#method or class func
                    self.eat('.')
                    if self.tknz.token_type == TOKEN_TYPE.IDENTIFIER:
                        if name in self.subroutine_sym.table.keys() or name in self.class_sym.table.keys(): #method call
                            entry = self.get_entry(name)
                            name = entry.type + '.' + self.tknz.current_token
                            self.code_writer.write_push(entry.kind, entry.idx)
                            n_args = 1
                        else:#class func
                            n_args = 0
                            name += '.' + self.tknz.current_token
                        self.eat(self.tknz.current_token)
                        self.eat('(')
                        n_args += self.compile_expression_list()
                        self.eat(')')
                        self.code_writer.write_call(name, n_args)
                    else:
                        print("term error")
                        exit(-1)
                else:
                    entry = self.get_entry(name)
                    self.code_writer.write_push(entry.kind, entry.idx)
        elif self.tknz.token_type == TOKEN_TYPE.SYMBOL:
            if self.tknz.current_token == '(':
                self.eat('(')
                self.compile_expression()
                self.eat(')')
            elif self.tknz.current_token in ('-', '~'):
                unary = self.tknz.current_token
                self.eat(self.tknz.current_token)
                self.compile_term()
                self.code_writer.write_unary(unary)
            else:
                print("term error")
                exit(-1)
        else:
            print("term error")
            exit(-1)
        self.level -= 1
        self.output('</term>')


    def compile_expression_list(self):
        self.output("<expressionList>")
        n_args = 0
        self.level += 1
        if not (self.tknz.token_type == TOKEN_TYPE.SYMBOL and self.tknz.current_token == ')'):
            self.compile_expression()
            n_args += 1
            while self.tknz.token_type == TOKEN_TYPE.SYMBOL and self.tknz.current_token == ',':
                self.eat(',')
                self.compile_expression()
                n_args += 1
        self.level -= 1
        self.output("</expressionList>")
        return n_args



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
        # for name in com.class_sym.table.keys
        # test_tables(com) #sym_table tests
        # print(com.class_name)
        # com.output_file.close()

def test_tables(com):
    for name in com.class_sym.table.keys():
        entry = com.class_sym.table[name]
        print(name + entry.type + '|' + entry.kind + '|' + str(entry.idx))
    
    for name in com.subroutine_sym.table.keys():
        entry = com.subroutine_sym.table[name]
        print(name + entry.type + '|' + entry.kind + '|' + str(entry.idx))


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