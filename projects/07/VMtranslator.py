from ast import parse
from cmd import Cmd
from enum import Enum
from os import stat
import sys
from telnetlib import STATUS

from babel import parse_locale

prefix = sys.argv[1].split("\\")[-1].split(".")[0]

class CMD_TYPE(Enum):
    NON     = -1
    ARITH   = 1
    MEM     = 2

arith_cmd = {
    "add":  ["@SP\n", "M=M-1\n", "A=M\n", "D=M\n", "@SP\n", "A=M-1\n", "M=M+D\n"],
    "sub":  ["@SP\n", "M=M-1\n", "A=M\n", "D=M\n", "@SP\n", "A=M-1\n", "M=M-D\n"],
    "and":  ["@SP\n", "M=M-1\n", "A=M\n", "D=M\n", "@SP\n", "A=M-1\n", "M=M&D\n"],
    "or":   ["@SP\n", "M=M-1\n", "A=M\n", "D=M\n", "@SP\n", "A=M-1\n", "M=M|D\n"],
    "neg":  ["@SP\n", "A=M-1\n", "M=-M\n"],
    "not":  ["@SP\n", "A=M-1\n", "M=!M\n"],
    "eq":   ["@SP\n", "M=M-1\n", "A=M\n", "D=M\n", "@SP\n", "A=M-1\n", "D=M-D\n", "@next_line+14\n", "D;JEQ\n", "@SP\n", "A=M-1\n", "M=0\n", "@next_line+16\n", "0;JMP\n", "@SP\n", "A=M-1\n", "M=-1\n"], #need current line
    "gt":   ["@SP\n", "M=M-1\n", "A=M\n", "D=M\n", "@SP\n", "A=M-1\n", "D=M-D\n", "@next_line+14\n", "D;JGT\n", "@SP\n", "A=M-1\n", "M=0\n", "@next_line+16\n", "0;JMP\n", "@SP\n", "A=M-1\n", "M=-1\n"], #need current line
    "lt":   ["@SP\n", "M=M-1\n", "A=M\n", "D=M\n", "@SP\n", "A=M-1\n", "D=M-D\n", "@next_line+14\n", "D;JLT\n", "@SP\n", "A=M-1\n", "M=0\n", "@next_line+16\n", "0;JMP\n", "@SP\n", "A=M-1\n", "M=-1\n"], #need current line
}
#7 12
#push temp i = 5: @5+i D=M @SP M=M+1 A=M-1 M=D
#push static i:@xxx.i D=M @SP M=M+1 A=M-1 M=D
#push pointer 0/1: @THIS/THAT D=M @SP M=M+1 A=M-1 M=D

#pop temp i :@SP M=M-1 A=M D=M @5+i M=D
#pop static i: @SP M=M-1 A=M D=M @xxx.i M=D
#pop pointer 0/1: @SP M=M-1 A=M D=M @THIS/THAT M=D

push_cmd = {
    "constant": ["@i\n", "D=A\n", "@SP\n", "M=M+1\n", "A=M-1\n", "M=D\n"],
    "local":    ["@LCL\n", "D=M\n", "@i\n", "A=D+A\n", "D=M\n", "@SP\n", "M=M+1\n", "A=M-1\n", "M=D\n"],
    "argument": ["@ARG\n", "D=M\n", "@i\n", "A=D+A\n", "D=M\n", "@SP\n", "M=M+1\n", "A=M-1\n", "M=D\n"],
    "this":     ["@THIS\n", "D=M\n", "@i\n", "A=D+A\n", "D=M\n", "@SP\n", "M=M+1\n", "A=M-1\n", "M=D\n"],
    "that":     ["@THAT\n", "D=M\n", "@i\n", "A=D+A\n", "D=M\n", "@SP\n", "M=M+1\n", "A=M-1\n", "M=D\n"],
    "temp":     ["@5+i\n", "D=M\n", "@SP\n", "M=M+1\n", "A=M-1\n", "M=D\n"],
    "static":   ["@xxx.i\n", "D=M\n", "@SP\n", "M=M+1\n", "A=M-1\n", "M=D\n"],
    "pointer":  ["@THIS/THAT\n", "D=M\n", "@SP\n", "M=M+1\n", "A=M-1\n", "M=D\n"],
}

pop_cmd = {
    "local":    ["@i\n", "D=A\n", "@LCL\n", "M=M+D\n","@SP\n", "M=M-1\n", "A=M\n", "D=M\n", "@LCL\n", "A=M\n", "M=D\n", "@i\n", "D=A\n", "@LCL\n", "M=M-D\n"],# LCL += i, D=*(--sp), *LCL = D, LCL -= i
    "argument": ["@i\n", "D=A\n", "@ARG\n", "M=M+D\n","@SP\n", "M=M-1\n", "A=M\n", "D=M\n", "@ARG\n", "A=M\n", "M=D\n", "@i\n", "D=A\n", "@ARG\n", "M=M-D\n"],# LCL += i, D=*(--sp), *LCL = D, LCL -= i
    "this":     ["@i\n", "D=A\n", "@THIS\n", "M=M+D\n","@SP\n", "M=M-1\n", "A=M\n", "D=M\n", "@THIS\n", "A=M\n", "M=D\n", "@i\n", "D=A\n", "@THIS\n", "M=M-D\n"],# LCL += i, D=*(--sp), *LCL = D, LCL -= i
    "that":     ["@i\n", "D=A\n", "@THAT\n", "M=M+D\n","@SP\n", "M=M-1\n", "A=M\n", "D=M\n", "@THAT\n", "A=M\n", "M=D\n", "@i\n", "D=A\n", "@THAT\n", "M=M-D\n"],# LCL += i, D=*(--sp), *LCL = D, LCL -= i
    "temp":     ["@SP\n", "M=M-1\n", "A=M\n", "D=M\n", "@5+i\n", "M=D\n"],
    "pointer":  ["@SP\n", "M=M-1\n", "A=M\n", "D=M\n", "@THIS/THAT\n", "M=D\n"],
    "static":   ["@SP\n", "M=M-1\n", "A=M\n", "D=M\n", "@xxx.i\n", "M=D\n"],
}
#0 11


def parse_cmd(cmd):
    token = cmd.split()
    if token[0] in arith_cmd.keys():
        status = CMD_TYPE.ARITH
    elif token[0] in ("pop", "push"):
        status = CMD_TYPE.MEM
    else:
        status = CMD_TYPE.NON
    return token, status

next_line = [0]

def gen_arith_asm(parsed_lst):
    asm_lst = arith_cmd[parsed_lst[0]]
    if parsed_lst[0] in ("eq", "gt", "lt"):
        asm_lst[7] = "@" + str(next_line[0] + 14) + '\n'
        asm_lst[12] = "@" + str(next_line[0] + 17) + '\n'
    
    return asm_lst

def gen_push(parsed_lst):
    asm_lst = push_cmd[parsed_lst[1]]
    if parsed_lst[1] == "constant":
        asm_lst[0] = "@" + parsed_lst[2] + "\n"
    if parsed_lst[1] in ("local", "argument", "this", "that"):
        asm_lst[2] = "@" + parsed_lst[2] + "\n"
    if parsed_lst[1] == "temp":
        asm_lst[0] = "@" + str(5+int(parsed_lst[2])) + "\n"
    if parsed_lst[1] == "static":
        asm_lst[0] = "@" + prefix + "." + parsed_lst[2] + "\n"
    if parsed_lst[1] == "pointer":
        if parsed_lst[2] == "0":
            asm_lst[0] = "@THIS\n"
        else:
            asm_lst[0] = "@THAT\n"
    return asm_lst

def gen_pop(parsed_lst):
    asm_lst = pop_cmd[parsed_lst[1]]
    if parsed_lst[1] in ("local", "argument", "this", "that"):
        asm_lst[0] = "@" + parsed_lst[2] + "\n"
        asm_lst[11] = "@" + parsed_lst[2] + "\n"
    if parsed_lst[1] == "temp":
        asm_lst[4] = "@" + str(5+int(parsed_lst[2])) + "\n"
    if parsed_lst[1] == "static":
        asm_lst[4] = "@" + prefix + "." + parsed_lst[2] + "\n"
    if parsed_lst[1] == "pointer":
        if parsed_lst[2] == "0":
            asm_lst[4] = "@THIS\n"
        else:
            asm_lst[4] = "@THAT\n"   
    return asm_lst

def gen_mem_asm(parsed_lst):
    asm_lst = []
    if parsed_lst[0] == "push":
        asm_lst = gen_push(parsed_lst)
        
    elif parsed_lst[0] == "pop":
        asm_lst = gen_pop(parsed_lst)
        
    # asm_code = ""
    # if parsed_cmd[1] == "constant":
    #     # asm_code += 
    #     pass
    
    return asm_lst

def gen_asm(parsed_lst, status, out_f):
    out_f.write("//" + " ".join(parsed_lst) + '\n')
    asm_lst = []
    if status == CMD_TYPE.ARITH:
        asm_lst = gen_arith_asm(parsed_lst)
    elif status == CMD_TYPE.MEM:
        asm_lst = gen_mem_asm(parsed_lst)
        # pass
    if asm_lst:
        out_f.write("".join(asm_lst))
        next_line[0] += len(asm_lst)





if __name__ == '__main__':
    if len(sys.argv) != 2:
        # print(sys.argv)
        print("Usage:", sys.argv[0], "<vm_file>")
        exit(1)
    # print(sys.argv[1].split("\\")[-1].split(".")[0])
    out_file = open(sys.argv[1].replace("vm", "asm"), 'w')
    # out_file.writelines()
    with open(sys.argv[1], 'r') as f:
        line = f.readline()
        while line:
            de_comment = line.split('//')[0].strip()
            if de_comment:
                parsed, status = parse_cmd(de_comment)
                gen_asm(parsed, status, out_file)
            line = f.readline()