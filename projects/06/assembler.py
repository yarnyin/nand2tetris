import sys
# print(sys.argv)

sym_table = {
    "R0":0,
    "R1":1,
    "R2":2,
    "R3":3,
    "R4":4,
    "R5":5,
    "R6":6,
    "R7":7,
    "R8":8,
    "R9":9,
    "R10":10,
    "R11":11,
    "R12":12,
    "R13":13,
    "R14":14,
    "R15":15,
    "SCREEN":16384,
    "KBD":24576,
    "SP":0,
    "LCL":1,
    "ARG":2,
    "THIS":3,
    "THAT":4
}

comp_table = {
    "0":    "0101010",
    "1":    "0111111",
    "-1":   "0111010",
    "D":    "0001100",
    "A":    "0110000",
    "M":    "1110000",
    "!D":   "0001101",
    "!A":   "0110001",
    "!M":   "1110001",
    "-D":   "0001111",
    "-A":   "0110011",
    "-M":   "1110011",
    "D+1":  "0011111",
    "A+1":  "0110111",
    "M+1":  "1110111",
    "D-1":  "0001110",
    "A-1":  "0110010",
    "M-1":  "1110010",
    "D+A":  "0000010",
    "D+M":  "1000010",
    "D-A":  "0010011",
    "D-M":  "1010011",
    "A-D":  "0000111",
    "M-D":  "1000111",
    "D&A":  "0000000",
    "D&M":  "1000000",
    "D|A":  "0010101",
    "D|M":  "1010101",
}

dst_table = {
    "null": "000",
    "M":    "001",
    "D":    "010",
    "MD":   "011",
    "A":    "100",
    "AM":   "101",
    "AD":   "110",
    "AMD":  "111",
}

jmp_table = {
    "null": "000",
    "JGT":  "001",
    "JEQ":  "010",
    "JGE":  "011",
    "JLT":  "100",
    "JNE":  "101",
    "JLE":  "110",
    "JMP":  "111",
}

prog = []

def handle_label(file_name):
    # print(file_name)
    # print("handle labels ...")
    line_num = 0
    with open(file_name, 'r') as f:
        line = f.readline()
        while line:
            line = line.split('//')[0].strip().replace(' ', '').replace('\t', '')
            if line:
                if line[0] == '(':
                    # print(line[1:-1])
                    sym_table.update({line[1:-1]:line_num})
                else:
                    line_num += 1
                    prog.append(line)
            line=f.readline()
    # print(prog)
    # print(sym_table)
    # print("handle_label done")

def is_int(num):
     # is a int num
    if num[0] == ('-', '+'):
        return num[1:].isdigit()
    else:
        return num.isdigit()

next_addr = [16]
def A_inst(address, outf):
    if is_int(address):
        addr_binary = (bin(((1 << 15) - 1) & int(address))[2:]).zfill(15)
        # outf.write('0' + addr_binary + '\n')
    else:
        if address in sym_table.keys():
            addr_binary = (bin(((1 << 15) - 1) & sym_table[address])[2:]).zfill(15)
        else:
            sym_table.update({address:next_addr[0]})
            addr_binary = (bin(((1 << 15) - 1) & next_addr[0])[2:]).zfill(15)
            next_addr[0] += 1
        # print('0' + addr_binary)
    outf.write('0' + addr_binary + '\n')

def C_inst(instruction, outf):
    parse = instruction.split('=')
    # dst = parse[0].strip()
    if len(parse) == 2:
        dst = parse[0]
        if ';' in parse[1]:
            comp = parse[1].split(';')[0]
            jmp = parse[1].split(';')[1]
        else:
            comp = parse[1]
            jmp = "null"
    else:
        if ";" in parse[0]:
            comp = parse[0].split(";")[0]
            jmp = parse[0].split(";")[1]
            dst = "null"
        else:
            comp = parse[0]
            dst = "null"
            jmp = "null"
    bin_inst = "111"
    bin_inst += comp_table[comp]
    bin_inst += dst_table[dst]
    bin_inst += jmp_table[jmp]

    # print(bin_inst)
    outf.write(bin_inst + '\n')

    

def translate(output_file):
    # print("translate")
    outf = open(output_file, 'w')
    for instruction in prog:
        if instruction[0] == '@': #A_inst
            A_inst(instruction[1:], outf)
        else: #C_inst
            C_inst(instruction, outf)
    outf.close()
    # print(sym_table)





if __name__ == '__main__':
    if len(sys.argv) != 2:
        # print(sys.argv)
        print("Usage:", sys.argv[0], "<asm_file>")
        exit(1)
    handle_label(sys.argv[1])
    # print(sys.argv[1].replace("asm", "hack"))
    translate(sys.argv[1].replace("asm", "hack"))