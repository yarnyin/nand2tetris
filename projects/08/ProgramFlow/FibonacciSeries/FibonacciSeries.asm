//push argument 1
@ARG
D=M
@1
A=D+A
D=M
@SP
M=M+1
A=M-1
M=D
//pop pointer 1
@SP
M=M-1
A=M
D=M
@THAT
M=D
//push constant 0
@0
D=A
@SP
M=M+1
A=M-1
M=D
//pop that 0
@0
D=A
@THAT
M=M+D
@SP
M=M-1
A=M
D=M
@THAT
A=M
M=D
@0
D=A
@THAT
M=M-D
//push constant 1
@1
D=A
@SP
M=M+1
A=M-1
M=D
//pop that 1
@1
D=A
@THAT
M=M+D
@SP
M=M-1
A=M
D=M
@THAT
A=M
M=D
@1
D=A
@THAT
M=M-D
//push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
M=M+1
A=M-1
M=D
//push constant 2
@2
D=A
@SP
M=M+1
A=M-1
M=D
//sub
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M-D
//pop argument 0
@0
D=A
@ARG
M=M+D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@0
D=A
@ARG
M=M-D
//label MAIN_LOOP_START
(MAIN_LOOP_START)
//push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
M=M+1
A=M-1
M=D
//if-goto COMPUTE_ELEMENT
@SP
M=M-1
A=M
D=M
@COMPUTE_ELEMENT
D; JNE
//goto END_PROGRAM
@END_PROGRAM
0; JMP
//label COMPUTE_ELEMENT
(COMPUTE_ELEMENT)
//push that 0
@THAT
D=M
@0
A=D+A
D=M
@SP
M=M+1
A=M-1
M=D
//push that 1
@THAT
D=M
@1
A=D+A
D=M
@SP
M=M+1
A=M-1
M=D
//add
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M+D
//pop that 2
@2
D=A
@THAT
M=M+D
@SP
M=M-1
A=M
D=M
@THAT
A=M
M=D
@2
D=A
@THAT
M=M-D
//push pointer 1
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
//push constant 1
@1
D=A
@SP
M=M+1
A=M-1
M=D
//add
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M+D
//pop pointer 1
@SP
M=M-1
A=M
D=M
@THAT
M=D
//push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
M=M+1
A=M-1
M=D
//push constant 1
@1
D=A
@SP
M=M+1
A=M-1
M=D
//sub
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M-D
//pop argument 0
@0
D=A
@ARG
M=M+D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@0
D=A
@ARG
M=M-D
//goto MAIN_LOOP_START
@MAIN_LOOP_START
0; JMP
//label END_PROGRAM
(END_PROGRAM)
