func:
RD r1, r2
WD r1, r2
RD r2, r3, 15

MOV r1, r2
RET

_start:
NOP
RI r1, 10

lbl: 
ADD r3, r2, r2
ADI r2, r2, r1
SUBI r1, r1, 1

JNZ lbl
CALL func