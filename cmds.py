from typing import List

from regs import *


class Assembly:

    @staticmethod
    def check_S(result: int) -> None:
        set_S() if result < 0 else drop_S()

    @staticmethod
    def check_Z(result: int) -> None:
        set_Z() if result == 0 else drop_Z()

    @staticmethod
    def check_C(result: int, arg1: int, arg2: int) -> None:
        result = abs(result)
        arg1 = abs(arg1)
        arg2 = abs(arg2)
        while arg1 != 0 and arg2 != 0:
            arg1 >>= 1
            arg2 >>= 1
            result >>= 1
        set_C() if result == 0 else drop_C()

    @staticmethod
    def check_O(result: int) -> None:
        if result >= (2 << 32) or result < -(2 << 32):
            set_O()
        else:
            drop_O()

    @staticmethod
    def check_I() -> None:
        pass

    @staticmethod
    def check_T() -> None:
        pass

    @staticmethod
    def check_M() -> None:
        pass

    @staticmethod
    def bound_result(result: int) -> int:
        if result >= (2 << 32):
            return result % (2 << 32)
        if result < -(2 << 32):
            return result % -(2 << 32)

    @staticmethod
    def RB(R0: int, R1: int, C: int = 0) -> None:
        RG[R0] = MEM[RG[R1] + C]

    @staticmethod
    def RW(R0: int, R1: int, C: int = 0) -> None:
        RG[R0] =  MEM[RG[R1] + C]
        RG[R0] += MEM[RG[R1] + C + 1] << 8
        # return Assembly.RB(RG, MEM, R0, R1, C)

    @staticmethod
    def RD(R0: int, R1: int, C: int = 0) -> None:
        RG[R0] =  MEM[RG[R1] + C]
        RG[R0] += MEM[RG[R1] + C + 1] << 8
        RG[R0] += MEM[RG[R1] + C + 1] << 16
        RG[R0] += MEM[RG[R1] + C + 1] << 24
        # return Assembly.RB(RG, MEM, R0, R1, C)

    @staticmethod
    def WB(R0: int, R1: int, C: int = 0) -> None:
        MEM[RG[R1] + C] = RG[R0] & 0xff

    @staticmethod
    def WW(R0: int, R1: int, C: int = 0) -> None:
        MEM[RG[R1] + C] = RG[R0] & 0xff
        MEM[RG[R1] + C + 1] = RG[R0] & 0xff00

    @staticmethod
    def WD(R0: int, R1: int, C: int = 0) -> None:
        MEM[RG[R1] + C] = RG[R0] & 0xff
        MEM[RG[R1] + C + 1] = RG[R0] & 0xff00
        MEM[RG[R1] + C + 2] = RG[R0] & 0xff0000
        MEM[RG[R1] + C + 3] = RG[R0] & 0xff000000

    @staticmethod
    def RI(R0: int, C: int) -> None:
        RG[R0] = C

    @staticmethod
    def MOV(R0: int, R1: int) -> None:
        RG[R0] = RG[R1]

    @staticmethod
    def ADD(R0: int, R1: int, R2: int) -> None:
        RG[R0] = RG[R1] + RG[R2]
        Assembly.check_S(RG[R0])
        Assembly.check_Z(RG[R0])
        Assembly.check_C(RG[R0], RG[R1], RG[R2])
        Assembly.check_O(RG[R0])

    @staticmethod
    def ADI(R0: int, R1: int, C: int) -> None:
        RG[R0] = RG[R1] + C
        Assembly.check_S(RG[R0])
        Assembly.check_Z(RG[R0])
        Assembly.check_C(RG[R0], RG[R1], C)
        Assembly.check_O(RG[R0])

    @staticmethod
    def SUB(R0: int, R1: int, R2: int) -> None:
        RG[R0] = RG[R1] - RG[R2]
        Assembly.check_S(RG[R0])
        Assembly.check_Z(RG[R0])
        Assembly.check_C(RG[R0], RG[R1], RG[R2])
        Assembly.check_O(RG[R0])

    @staticmethod
    def SUBI(R0: int, R1: int, C: int) -> None:
        RG[R0] = RG[R1] - C
        Assembly.check_S(RG[R0])
        Assembly.check_Z(RG[R0])
        Assembly.check_C(RG[R0], RG[R1], C)
        Assembly.check_O(RG[R0])

    @staticmethod
    def MUL(R0: int, R1: int) -> None:
        res = RG[R0] * RG[R1]
        RG[5] = res & int('0' * 32 + '1' * 32, 2)
        RG[4] = (res >> 32) & int('0' * 32 + '1' * 32, 2)
        Assembly.check_S(res)
        Assembly.check_Z(res)
        Assembly.check_C(res, RG[R0], RG[R1])
        Assembly.check_O(res)

    @staticmethod
    def MULI(R0: int, C: int) -> None:
        res = RG[R0] * C
        RG[5] = res & int('0' * 32 + '1' * 32, 2)
        RG[4] = (res >> 32) & int('0' * 32 + '1' * 32, 2)
        Assembly.check_S(res)
        Assembly.check_Z(res)
        Assembly.check_C(res, RG[R0], C)
        Assembly.check_O(res)

    @staticmethod
    def DIV(R0: int, R1: int) -> None:
        RG[5] = (RG[R0] // RG[R1]) & int('0' * 16 + '1' * 16, 2)
        RG[4] = ((RG[R0] % RG[R1]) >> 16) & int('0' * 16 + '1' * 16, 2)
        Assembly.check_S(RG[5])
        Assembly.check_Z(RG[5])
        Assembly.check_C(RG[5], RG[R0], RG[R1])
        Assembly.check_O(RG[5])

    @staticmethod
    def DIVI(R0: int, C: int) -> None:
        RG[5] = (RG[R0] // C) & int('0' * 16 + '1' * 16, 2)
        RG[4] = ((RG[R0] % C) >> 16) & int('0' * 16 + '1' * 16, 2)
        Assembly.check_S(RG[5])
        Assembly.check_Z(RG[5])
        Assembly.check_C(RG[5], RG[R0], C)
        Assembly.check_O(RG[5])

    @staticmethod
    def NOT(R0: int) -> None:
        RG[R0] = ~RG[R0]
        Assembly.check_S(RG[R0])
        Assembly.check_Z(RG[R0])

    @staticmethod
    def AND(R0: int, R1: int) -> None:
        RG[R0] = RG[R0] & RG[R1]
        Assembly.check_S(RG[R0])
        Assembly.check_Z(RG[R0])

    @staticmethod
    def ANDI(R0: int, C: int) -> None:
        RG[R0] = RG[R0] & C
        Assembly.check_S(RG[R0])
        Assembly.check_Z(RG[R0])

    @staticmethod
    def OR(R0: int, R1: int) -> None:
        RG[R0] = RG[R0] | RG[R1]
        Assembly.check_S(RG[R0])
        Assembly.check_Z(RG[R0])

    @staticmethod
    def ORI(R0: int, C: int) -> None:
        RG[R0] = RG[R0] | C
        Assembly.check_S(RG[R0])
        Assembly.check_Z(RG[R0])

    @staticmethod
    def XOR(R0: int, R1: int) -> None:
        RG[R0] = RG[R0] ^ RG[R1]
        Assembly.check_S(RG[R0])
        Assembly.check_Z(RG[R0])

    @staticmethod
    def XORI(R0: int, C: int) -> None:
        RG[R0] = RG[R0] ^ C
        Assembly.check_S(RG[R0])
        Assembly.check_Z(RG[R0])

    @staticmethod
    def SHL(R0: int, C: int) -> None:
        t = RG[R0]
        RG[R0] = RG[R0] << C
        Assembly.check_S(RG[R0])
        Assembly.check_Z(RG[R0])
        # Assembly.check_C(RG[R0], t, C)
        set_C() if t & (1 << (32 - C)) else drop_C()
        Assembly.check_O(RG[R0])

    @staticmethod
    def SHR(R0: int, C: int) -> None:
        t = RG[R0]
        RG[R0] = RG[R0] >> C
        Assembly.check_S(RG[R0])
        Assembly.check_Z(RG[R0])
        # Assembly.check_C(RG[R0], t, C)
        set_C() if t & (1 << C - 1) else drop_C()
        Assembly.check_O(RG[R0])

    @staticmethod
    def CALL(C: int) -> None:
        RG[3] = get_PC()
        set_PC(C)

    @staticmethod
    def RET() -> None:
        set_PC(RG[3])

    @staticmethod
    def JMP(C: int) -> None:
        set_PC(C)

    @staticmethod
    def RJMP(C: int) -> None:
        set_PC(get_PC() + C)

    @staticmethod
    def JZ(C: int) -> None:
        if Z():
            Assembly.JMP(C)

    @staticmethod
    def JNZ(C: int) -> None:
        if not Z():
            Assembly.JMP(C)

    @staticmethod
    def JO(C: int) -> None:
        if O():
            Assembly.JMP(C)

    @staticmethod
    def JNO(C: int) -> None:
        if not O():
            Assembly.JMP(C)

    @staticmethod
    def JC(C: int) -> None:
        if C():
            Assembly.JMP(C)

    @staticmethod
    def JNC(C: int) -> None:
        if not C():
            Assembly.JMP(C)

    @staticmethod
    def JPS(C: int) -> None:
        if S():
            Assembly.JMP(C)

    @staticmethod
    def JMS(C: int) -> None:
        if not S():
            Assembly.JMP(C)

    @staticmethod
    def NOP() -> None:
        # set_PC(get_PC() + 1)
        ...

    @staticmethod
    def INT() -> None:
        raise NotImplemented

    @staticmethod
    def IRET() -> None:
        raise NotImplemented

    @staticmethod
    def RFL(R0: int) -> None:
        RG[R0] = get_FLR()

    @staticmethod
    def SFL(F: int) -> None:
        set_FLR(1 << F)

    @staticmethod
    def CFL(F: int) -> None:
        drop_FLR(0 << F)

    @staticmethod
    def RTLB(R0: int) -> None:
        RG[R0] = get_TLB()

    @staticmethod
    def WTLB(R0: int) -> None:
        set_TLB(RG[R0])

    @staticmethod
    def RFE() -> None:
        drop_M()

    @staticmethod
    def SCALL() -> None:
        set_M()

    @staticmethod
    def HALT() -> None:
        raise NotImplemented

    @staticmethod
    def IFC(R0: int, R1: int) -> None:
        FP[R0] = float(RG[R1])

    @staticmethod
    def FIC(R0: int, R1: int) -> None:
        RG[R1] = int(FP[R0])
        Assembly.check_S(RG[R1])
        Assembly.check_Z(RG[R1])
        # Assembly.check_C(RG[R1], FP[R0], 0)
        # Assembly.check_O(RG[R1])

    @staticmethod
    def FADD(R0: int, R1: int, R2: int) -> None:
        FP[R0] = FP[R1] + FP[R2]
        # return Assembly.ADD(FP, R0, R1, R2)

    @staticmethod
    def FSUB(R0: int, R1: int, R2: int) -> None:
        FP[R0] = FP[R1] - FP[R2]
        return Assembly.SUB(FP, R0, R1, R2)

    @staticmethod
    def FMUL(R0: int, R1: int, R2: int) -> None:
        FP[R0] = FP[R1] * FP[R2]

    @staticmethod
    def FDIV(R0: int, R1: int, R2: int) -> None:
        FP[R0] = FP[R1] / FP[R2]

    @staticmethod
    def FMOV(R0: int, R1: int) -> None:
        FP[R0] = FP[R1]

    @staticmethod
    def FRI(R0: int, C: int) -> None:
        FP[R0] = C

    @staticmethod
    def FRD(R0: int, R1: int, C: int) -> None:
        # return Assembly.RD(FP, MEM, R0, R1, C)
        FP[R0] =  MEM[FP[R1] + C]
        FP[R0] += MEM[FP[R1] + C + 1] << 8
        FP[R0] += MEM[FP[R1] + C + 1] << 16
        FP[R0] += MEM[FP[R1] + C + 1] << 24

    @staticmethod
    def FWD(R0: int, R1: int, C: int) -> None:
        # return Assembly.WD(FP, MEM, R0, R1, C)
        MEM[FP[R1] + C] =     FP[R0] & 0xff
        MEM[FP[R1] + C + 1] = FP[R0] & 0xff00
        MEM[FP[R1] + C + 2] = FP[R0] & 0xff0000
        MEM[FP[R1] + C + 3] = FP[R0] & 0xff000000
