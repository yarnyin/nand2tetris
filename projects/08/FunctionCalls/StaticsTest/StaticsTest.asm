@SYS_START
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(SYS_START)
//function Class1.set 0
(Class1.set)
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
//pop static 0
@SP
M=M-1
A=M
D=M
@Class1.0
M=D
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
//pop static 1
@SP
M=M-1
A=M
D=M
@Class1.1
M=D
//push constant 0
@0
D=A
@SP
M=M+1
A=M-1
M=D
//return
@LCL
D=M
@5
A=D-A
D=M
@5
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@LCL
M=M-1
A=M
D=M
@THAT
M=D
@LCL
M=M-1
A=M
D=M
@THIS
M=D
@LCL
M=M-1
A=M
D=M
@ARG
M=D
@LCL
M=M-1
A=M
D=M
@LCL
M=D
@5
A=M
0;JMP
//function Class1.get 0
(Class1.get)
//push static 0
@Class1.0
D=M
@SP
M=M+1
A=M-1
M=D
//push static 1
@Class1.1
D=M
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
//return
@LCL
D=M
@5
A=D-A
D=M
@5
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@LCL
M=M-1
A=M
D=M
@THAT
M=D
@LCL
M=M-1
A=M
D=M
@THIS
M=D
@LCL
M=M-1
A=M
D=M
@ARG
M=D
@LCL
M=M-1
A=M
D=M
@LCL
M=D
@5
A=M
0;JMP
//function Class2.set 0
(Class2.set)
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
//pop static 0
@SP
M=M-1
A=M
D=M
@Class2.0
M=D
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
//pop static 1
@SP
M=M-1
A=M
D=M
@Class2.1
M=D
//push constant 0
@0
D=A
@SP
M=M+1
A=M-1
M=D
//return
@LCL
D=M
@5
A=D-A
D=M
@5
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@LCL
M=M-1
A=M
D=M
@THAT
M=D
@LCL
M=M-1
A=M
D=M
@THIS
M=D
@LCL
M=M-1
A=M
D=M
@ARG
M=D
@LCL
M=M-1
A=M
D=M
@LCL
M=D
@5
A=M
0;JMP
//function Class2.get 0
(Class2.get)
//push static 0
@Class2.0
D=M
@SP
M=M+1
A=M-1
M=D
//push static 1
@Class2.1
D=M
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
//return
@LCL
D=M
@5
A=D-A
D=M
@5
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@LCL
M=M-1
A=M
D=M
@THAT
M=D
@LCL
M=M-1
A=M
D=M
@THIS
M=D
@LCL
M=M-1
A=M
D=M
@ARG
M=D
@LCL
M=M-1
A=M
D=M
@LCL
M=D
@5
A=M
0;JMP
//function Sys.init 0
(Sys.init)
//push constant 6
@6
D=A
@SP
M=M+1
A=M-1
M=D
//push constant 8
@8
D=A
@SP
M=M+1
A=M-1
M=D
//call Class1.set 2
@Sys.init.RET$0
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@5
D=D-A
@2
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.set
0;JMP
(Sys.init.RET$0)
//pop temp 0
@SP
M=M-1
A=M
D=M
@5
M=D
//push constant 23
@23
D=A
@SP
M=M+1
A=M-1
M=D
//push constant 15
@15
D=A
@SP
M=M+1
A=M-1
M=D
//call Class2.set 2
@Sys.init.RET$1
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@5
D=D-A
@2
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.set
0;JMP
(Sys.init.RET$1)
//pop temp 0
@SP
M=M-1
A=M
D=M
@5
M=D
//call Class1.get 0
@Sys.init.RET$2
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.get
0;JMP
(Sys.init.RET$2)
//call Class2.get 0
@Sys.init.RET$3
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.get
0;JMP
(Sys.init.RET$3)
//label WHILE
(WHILE)
//goto WHILE
@WHILE
0; JMP
