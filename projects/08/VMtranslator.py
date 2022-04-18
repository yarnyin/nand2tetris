from ast import parse
from cmd import Cmd
from enum import Enum
import glob
from secrets import token_hex
import sys
from telnetlib import STATUS

from babel import parse_locale

# prefix = sys.argv[1].split("\\")[-1].split(".")[0]
cur_fun = ["NONENOENOENOENO", 0]

class CMD_TYPE(Enum):
    NON     = -1
    ARITH   = 1
    MEM     = 2
    BRCH    = 3
    FUNC    = 4

arith_cmd = {
    "add":  ["@SP\n", "M=M-1\n", "A=M\n", "D=M\n", "@SP\n", "A=M-1\n", "M=M+D\n"],
    "sub":  ["@SP\n", "M=M-1\n", "A=M\n", "D=M\n", "@SP\n", "A=M-1\n", "M=M-D\n"],
    "and":  ["@SP\n", "M=M-1\n", "A=M\n", "D=M\n", "@SP\n", "A=M-1\n", "M=M&D\n"],
    "or":   ["@SP\n", "M=M-1\n", "A=M\n", "D=M\n", "@SP\n", "A=M-1\n", "M=M|D\n"],
    "neg":  ["@SP\n", "A=M-1\n", "M=-M\n"],
    "not":  ["@SP\n", "A=M-1\n", "M=!M\n"],
    # "eq":   ["@SP\n", "M=M-1\n", "A=M\n", "D=M\n", "@SP\n", "A=M-1\n", "D=M-D\n", "@next_line+14\n", "D;JEQ\n", "@SP\n", "A=M-1\n", "M=0\n", "@next_line+16\n", "0;JMP\n", "@SP\n", "A=M-1\n", "M=-1\n"], #need current line
    # "gt":   ["@SP\n", "M=M-1\n", "A=M\n", "D=M\n", "@SP\n", "A=M-1\n", "D=M-D\n", "@next_line+14\n", "D;JGT\n", "@SP\n", "A=M-1\n", "M=0\n", "@next_line+16\n", "0;JMP\n", "@SP\n", "A=M-1\n", "M=-1\n"], #need current line
    # "lt":   ["@SP\n", "M=M-1\n", "A=M\n", "D=M\n", "@SP\n", "A=M-1\n", "D=M-D\n", "@next_line+14\n", "D;JLT\n", "@SP\n", "A=M-1\n", "M=0\n", "@next_line+16\n", "0;JMP\n", "@SP\n", "A=M-1\n", "M=-1\n"], #need current line
    "eq":   ["@SP\n", "M=M-1\n", "A=M\n", "D=M\n", "@SP\n", "A=M-1\n", "D=M-D\n", "M=0\n", "@END_EQ.i\n", "D;JNE\n", "@SP\n", "A=M-1\n", "M=-1\n", "(END_EQ.i)\n"],
    "gt":   ["@SP\n", "M=M-1\n", "A=M\n", "D=M\n", "@SP\n", "A=M-1\n", "D=M-D\n", "M=0\n", "@END_GT.i\n", "D;JLE\n", "@SP\n", "A=M-1\n", "M=-1\n", "(END_GT.i)\n"],
    "lt":   ["@SP\n", "M=M-1\n", "A=M\n", "D=M\n", "@SP\n", "A=M-1\n", "D=M-D\n", "M=0\n", "@END_LT.i\n", "D;JGE\n", "@SP\n", "A=M-1\n", "M=-1\n", "(END_LT.i)\n"],

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

branch_cmd = {
    "label":    ["(LBL)\n"],
    "goto":     ["@LBL\n", "0; JMP\n"],
    "if-goto":  ["@SP\n", "M=M-1\n", "A=M\n", "D=M\n", "@LBL\n", "D; JNE\n"]
}

func_cmd = {
    "function": ["(LBL)\n"], #lcl ntimes :(push constant 0) xn
    "call":     ["@returnAdd\n", "D=A\n@SP\nM=M+1\nA=M-1\nM=D\n", "@LCL\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n", "@ARG\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n"
                , "@THIS\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n", "@THAT\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n", "@SP\nD=M\n@5\nD=D-A\n", "@nArgs\n", "D=D-A\n@ARG\nM=D\n"
                , "@SP\nD=M\n@LCL\nM=D\n", "@funcName\n0;JMP\n", "(returnAdd)\n"], #push retvalue; push LCL; push ARG; push this; push that; arg = sp - 5- nargs; lcl 
    "return":   ["@LCL\nD=M\n@5\nA=D-A\nD=M\n@5\nM=D\n", "@SP\nA=M-1\nD=M\n@ARG\nA=M\nM=D\n", "@ARG\nD=M+1\n@SP\nM=D\n", "@LCL\nM=M-1\nA=M\nD=M\n@THAT\nM=D\n"
                , "@LCL\nM=M-1\nA=M\nD=M\n@THIS\nM=D\n", "@LCL\nM=M-1\nA=M\nD=M\n@ARG\nM=D\n", "@LCL\nM=M-1\nA=M\nD=M\n@LCL\nM=D\n", "@5\nA=M\n0;JMP\n"],

}


def parse_cmd(cmd):
    token = cmd.split()
    if token[0] in arith_cmd.keys():
        status = CMD_TYPE.ARITH
    elif token[0] in ("pop", "push"):
        status = CMD_TYPE.MEM
    elif token[0] in branch_cmd.keys():
        status = CMD_TYPE.BRCH
    elif token[0] in func_cmd.keys():
        status = CMD_TYPE.FUNC
    else:
        status = CMD_TYPE.NON
    return token, status

# next_line = [0]


def gen_func_asm(parsed_lst):
    head_tok = parsed_lst[0]
    asm_lst = func_cmd[head_tok]
    if head_tok == "function":
        asm_lst[0] = "(" + parsed_lst[1] + ")\n"
        # print("local = " + parsed_lst[2])
        for i in range(0, int(parsed_lst[2])):
            asm_lst += "@SP\nM=M+1\nA=M-1\nM=0\n"
        cur_fun[0] = parsed_lst[1]
        cur_fun[1] = 0
    elif head_tok == "call":
        asm_lst[0] = "@" + cur_fun[0] + ".RET$" + str(cur_fun[1]) + "\n"
        asm_lst[-1] = "(" + cur_fun[0] + ".RET$" + str(cur_fun[1]) + ")\n"
        asm_lst[-2] = "@" + parsed_lst[1] + "\n0;JMP\n"
        asm_lst[-5] = "@" + parsed_lst[-1] + "\n"
        cur_fun[1] += 1
    else:
        pass
    return asm_lst


def gen_brch_asm(parsed_lst):
    head_tok = parsed_lst[0]
    asm_lst = branch_cmd[head_tok]
    if head_tok == "label":
        asm_lst[0] = "(" + parsed_lst[1] + ")\n"
    elif head_tok == "goto":
        asm_lst[0] = "@" + parsed_lst[1] + "\n"
    else:
        asm_lst[4] = "@" + parsed_lst[1] + "\n"
    return asm_lst

def gen_arith_asm(parsed_lst):
    asm_lst = arith_cmd[parsed_lst[0]]
    if parsed_lst[0] in ("eq", "gt", "lt"):
        tok = parsed_lst[0]
        asm_lst[8] = "@END_" + tok.upper() + "." + prefix[0] + "." + str(logic_cnt[tok]) + "\n"
        asm_lst[13] = "(END_" + tok.upper() + "." + prefix[0] + "." + str(logic_cnt[tok]) + ")\n"
        logic_cnt[tok] += 1
    
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
        asm_lst[0] = "@" + prefix[0] + "." + parsed_lst[2] + "\n"
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
        asm_lst[4] = "@" + prefix[0] + "." + parsed_lst[2] + "\n"
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
    elif status == CMD_TYPE.BRCH:
        asm_lst = gen_brch_asm(parsed_lst)
    elif status == CMD_TYPE.FUNC:
        asm_lst = gen_func_asm(parsed_lst)
        # pass
    if asm_lst:
        out_f.write("".join(asm_lst))
        # next_line[0] += len(asm_lst)


def handle_file(in_file):
    with open(in_file, 'r') as f:
        line = f.readline()
        while line:
            de_comment = line.split('//')[0].strip()
            if de_comment:
                parsed, status = parse_cmd(de_comment)
                gen_asm(parsed, status, out_file)
            line = f.readline()


def get_files(file_or_dir):
    if file_or_dir.endswith(".vm"):
        return [file_or_dir], file_or_dir.replace(".vm", ".asm")
    else:
        return glob.glob(file_or_dir + "/*.vm"), file_or_dir + '\\' + file_or_dir.split('\\')[-1] + '.asm'
    
logic_cnt = {
    "eq":0,
    "gt":0,
    "lt":0,
}

prefix = [""]

def write_init():
    #init stack
    out_file.write("@256\nD=A\n@SP\nM=D\n")
    #call sys.init 0
    out_file.write(''.join(["@SYS_START\n", "D=A\n@SP\nM=M+1\nA=M-1\nM=D\n", "@LCL\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n", "@ARG\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n"
                , "@THIS\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n", "@THAT\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n", "@SP\nD=M\n@5\nD=D-A\n", "@ARG\nM=D\n"
                , "@SP\nD=M\n@LCL\nM=D\n", "@Sys.init\n0;JMP\n", "(SYS_START)\n"]))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        # print(sys.argv)
        print("Usage:", sys.argv[0], "<vm_file>")
        exit(1)
    # print(sys.argv[1].split("\\")[-1].split(".")[0])
    # out_file = open(sys.argv[1].replace("vm", "asm"), 'w')
    in_files, out_file = get_files(sys.argv[1].strip("\\"))
    out_file = open(out_file, "w")
    write_init()
    for in_file in in_files:
        prefix[0] = in_file.strip("\\").split("\\")[-1].split(".")[0]
        handle_file(in_file)
        # global prefix
        # print(prefix)
        logic_cnt = {
            "eq":0,
            "gt":0,
            "lt":0,
        }
    out_file.close()

    # out_file.writelines()
    # with open(sys.argv[1], 'r') as f:
    #     line = f.readline()
    #     while line:
    #         de_comment = line.split('//')[0].strip()
    #         if de_comment:
    #             parsed, status = parse_cmd(de_comment)
    #             gen_asm(parsed, status, out_file)
    #         line = f.readline()