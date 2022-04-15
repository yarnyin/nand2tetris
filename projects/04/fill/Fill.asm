// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
@color
M=0
(loop)
@KBD
D=M;
@black
D;JNE

@color
M=0 //white
@draw
0;JMP

(black)
@color
M=-1
@draw
0;JMP

0;JMP
@loop
0;JMP






(draw)
@8192
D=A
@n_pixs
M=D
@SCREEN
D=A
@cur
M=D

(f_loop)
@n_pixs
D=M-1
M=D
@loop
D;JLT //if n_pixs < 0 ,jmp back
@color
D=M
@cur
A=M
M=D
@cur
M=M+1 //cur = cur+1
@f_loop
0;JMP


