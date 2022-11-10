from math import fabs
from typing import List

from regs import FLR, TLB, S, set_S, set_Z, set_C, set_O


class Assembly:

    @staticmethod
    def check_S(result: int) -> None:
        set_S() if result < 0 else None

    @staticmethod
    def check_Z(result: int) -> None:
        set_Z() if result == 0 else None

    @staticmethod
    def check_C(result: int, arg1: int, arg2: int) -> None:
        result = abs(result)
        arg1 = abs(arg1)
        arg2 = abs(arg2)
        while arg1 != 0 and arg2 != 0:
            arg1 >>= 1
            arg2 >>= 1
            result >>= 1
        set_C() if result == 0 else None

    @staticmethod
    def check_O(result: int) -> None:
        if result >= (2 << 32) or result < -(2 << 32):
            set_O()

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
    def RB(RG: List[int], R0: int, R1: int, C: int = 0) -> None:
        RG[R0] = RG[R1] + C

    @staticmethod
    def RW(RG: List[int], R0: int, R1: int, C: int = 0) -> None:
        return Assembly.RB(RG, R0, R1, C)

    @staticmethod
    def RD(RG: List[int], R0: int, R1: int, C: int = 0) -> None:
        return Assembly.RB(RG, R0, R1, C)

    @staticmethod
    def WB(RG: List[int], MEM: List[int], R0: int, R1: int, C: int = 0) -> None:
        MEM[RG[R1] + C] = RG[R0]

    @staticmethod
    def WW(RG: List[int], MEM: List[int], R0: int, R1: int, C: int = 0) -> None:
        MEM[RG[R1] + C: RG[R1] + C + 1] = [MEM[RG[R0] + i] for i in range(2)]

    @staticmethod
    def WD(RG: List[int], MEM: List[int], R0: int, R1: int, C: int = 0) -> None:
        MEM[RG[R1] + C: RG[R1] + C + 3] = [MEM[RG[R0] + i] for i in range(4)]

    @staticmethod
    def RI(RG: List[int], R0: int, C: int) -> None:
        RG[R0] = C

    @staticmethod
    def MOV(RG: List[int], R0: int, R1: int) -> None:
        RG[R0] = RG[R1]

    @staticmethod
    def ADD(RG: List[int], R0: int, R1: int, R2: int) -> None:
        RG[R0] = RG[R1] + RG[R2]
        Assembly.check_S(RG[R0])
        Assembly.check_Z(RG[R0])
        Assembly.check_C(RG[R0], RG[R1], RG[R2])
        Assembly.check_O(RG[R0])

    @staticmethod
    def ADI(RG: List[int], R0: int, R1: int, C: int) -> None:
        RG[R0] = RG[R1] + C
        Assembly.check_S(RG[R0])
        Assembly.check_Z(RG[R0])
        Assembly.check_C(RG[R0], RG[R1], C)
        Assembly.check_O(RG[R0])

    @staticmethod
    def SUB(RG: List[int], R0: int, R1: int, R2: int) -> None:
        RG[R0] = RG[R1] - RG[R2]
        Assembly.check_S(RG[R0])
        Assembly.check_Z(RG[R0])
        Assembly.check_C(RG[R0], RG[R1], RG[R2])
        Assembly.check_O(RG[R0])

    @staticmethod
    def SUBI(RG: List[int], R0: int, R1: int, C: int) -> None:
        RG[R0] = RG[R1] - C
        Assembly.check_S(RG[R0])
        Assembly.check_Z(RG[R0])
        Assembly.check_C(RG[R0], RG[R1], C)
        Assembly.check_O(RG[R0])

    @staticmethod
    def MUL(RG: List[int], R5: int, R4: int, R0: int, R1: int) -> None:
        RG[R5] = (RG[R0] * RG[R1]) & int('0' * 32 + '1' * 32, 2)
        RG[R4] = ((RG[R0] * RG[R1]) >> 32) & int('0' * 32 + '1' * 32, 2)
        Assembly.check_S(RG[R5])
        Assembly.check_Z(RG[R5])
        Assembly.check_C(RG[R5], RG[R0], RG[R1])
        Assembly.check_O(RG[R5])
        Assembly.check_S(RG[R4])
        Assembly.check_Z(RG[R4])
        Assembly.check_C(RG[R4], RG[R0], RG[R1])
        Assembly.check_O(RG[R4])

    @staticmethod
    def MULI(RG: List[int], R5: int, R4: int, R0: int, C: int) -> None:
        RG[R5] = (RG[R0] * C) & int('0' * 32 + '1' * 32, 2)
        RG[R4] = ((RG[R0] * C) >> 32) & int('0' * 32 + '1' * 32, 2)
        Assembly.check_S(RG[R5])
        Assembly.check_Z(RG[R5])
        Assembly.check_C(RG[R5], RG[R0], C)
        Assembly.check_O(RG[R5])
        Assembly.check_S(RG[R4])
        Assembly.check_Z(RG[R4])
        Assembly.check_C(RG[R4], RG[R0], C)
        Assembly.check_O(RG[R4])

    @staticmethod
    def DIV(RG: List[int], R5: int, R4: int, R0: int, R1: int) -> None:
        RG[R5] = (RG[R0] // RG[R1]) & int('0' * 16 + '1' * 16, 2)
        RG[R4] = ((RG[R0] % RG[R1]) >> 16) & int('0' * 16 + '1' * 16, 2)
        Assembly.check_S(RG[R5])
        Assembly.check_Z(RG[R5])
        Assembly.check_C(RG[R5], RG[R0], RG[R1])
        Assembly.check_O(RG[R5])
        Assembly.check_S(RG[R4])
        Assembly.check_Z(RG[R4])
        Assembly.check_C(RG[R4], RG[R0], RG[R1])
        Assembly.check_O(RG[R4])

    @staticmethod
    def DIVI(RG: List[int], R5: int, R4: int, R0: int, C: int) -> None:
        RG[R5] = (RG[R0] // C) & int('0' * 16 + '1' * 16, 2)
        RG[R4] = ((RG[R0] % C) >> 16) & int('0' * 16 + '1' * 16, 2)
        Assembly.check_S(RG[R5])
        Assembly.check_Z(RG[R5])
        Assembly.check_C(RG[R5], RG[R0], C)
        Assembly.check_O(RG[R5])
        Assembly.check_S(RG[R4])
        Assembly.check_Z(RG[R4])
        Assembly.check_C(RG[R4], RG[R0], C)
        Assembly.check_O(RG[R4])

    @staticmethod
    def MULS(RG: List[int], R5: int, R4: int, R0: int, R1: int) -> None:
        return Assembly.MUL(RG, R5, R4, R0, R1)

    @staticmethod
    def MULSI(RG: List[int], R5: int, R4: int, R0: int, C: int) -> None:
        return Assembly.MULI(RG, R5, R4, R0, C)

    @staticmethod
    def DIVS(RG: List[int], R5: int, R4: int, R0: int, R1: int) -> None:
        return Assembly.DIV(RG, R5, R4, R0, R1)

    @staticmethod
    def DIVSI(RG: List[int], R5: int, R4: int, R0: int, C: int) -> None:
        return Assembly.DIVSI(RG, R5, R4, R0, C)

    @staticmethod
    def NOT(RG: List[int], R0: int) -> None:
        RG[R0] = ~RG[R0]

    @staticmethod
    def AND(RG: List[int], R0: int, R1: int) -> None:
        RG[R0] = RG[R0] & RG[R1]

    @staticmethod
    def ANDI(RG: List[int], R0: int, C: int) -> None:
        RG[R0] = RG[R0] & C

    @staticmethod
    def OR(RG: List[int], R0: int, R1: int) -> None:
        RG[R0] = RG[R0] | RG[R1]

    @staticmethod
    def ORI(RG: List[int], R0: int, C: int) -> None:
        RG[R0] = RG[R0] | C

    @staticmethod
    def XOR(RG: List[int], R0: int, R1: int) -> None:
        RG[R0] = RG[R0] ^ RG[R1]

    @staticmethod
    def XORI(RG: List[int], R0: int, C: int) -> None:
        RG[R0] = RG[R0] ^ C

    @staticmethod
    def SHL(RG: List[int], R0: int, C: int) -> None:
        RG[R0] = RG[R0] << C

    @staticmethod
    def SHR(RG: List[int], R0: int, C: int) -> None:
        RG[R0] = RG[R0] >> C

    @staticmethod
    def CALL() -> None:
        # TODO
        pass

    @staticmethod
    def RET() -> None:
        # TODO
        pass

    @staticmethod
    def JMP() -> None:
        # TODO
        pass

    @staticmethod
    def RJMP() -> None:
        # TODO
        pass

    @staticmethod
    def JZ() -> None:
        # TODO
        pass

    @staticmethod
    def JNZ() -> None:
        # TODO
        pass

    @staticmethod
    def JO() -> None:
        # TODO
        pass

    @staticmethod
    def JNO() -> None:
        # TODO
        pass

    @staticmethod
    def JC() -> None:
        # TODO
        pass

    @staticmethod
    def JNC() -> None:
        # TODO
        pass

    @staticmethod
    def JPS() -> None:
        # TODO
        pass

    @staticmethod
    def JMS() -> None:
        # TODO
        pass

    @staticmethod
    def NOP() -> None:
        # TODO
        pass

    @staticmethod
    def INT() -> None:
        # TODO
        pass

    @staticmethod
    def IRET() -> None:
        # TODO
        pass

    @staticmethod
    def RFL(RG: List[int], R0: int, F: int) -> None:
        RG[R0] = F

    @staticmethod
    def SFL(F: int) -> None:
        global FLR
        FLR |= (1 << F)

    @staticmethod
    def CFL(F: int) -> None:
        global FLR
        FLR &= (0 << F)

    @staticmethod
    def RTLB(RG: List[int], R0: int) -> None:
        RG[R0] = TLB

    @staticmethod
    def WTLB(RG: List[int], R0: int) -> None:
        global TLB
        TLB = RG[R0]

    @staticmethod
    def RFE() -> None:
        # TODO
        pass

    @staticmethod
    def SCALL() -> None:
        # TODO
        pass

    @staticmethod
    def HALT() -> None:
        # TODO
        pass

    @staticmethod
    def IFC(RG: List[int], R0: int, R1: int) -> None:
        RG[R0] = RG[R1]

    @staticmethod
    def FIC(RG: List[int], R0: int, R1: int) -> None:
        RG[R1] = RG[R0]

    @staticmethod
    def FADD(RG: List[int], R0: int, R1: int, R2: int) -> None:
        RG[R0] = RG[R1] + RG[R2]

    @staticmethod
    def FSUB(RG: List[int], R0: int, R1: int, R2: int) -> None:
        RG[R0] = RG[R1] - RG[R2]

    @staticmethod
    def FMUL(RG: List[int], R5: int, R4: int, R0: int, R1: int) -> None:
        return Assembly.MUL(RG, R5, R4, R0, R1)

    @staticmethod
    def FDIV(RG: List[int], R5: int, R4: int, R0: int, R1: int) -> None:
        return Assembly.DIV(RG, R5, R4, R0, R1)

    @staticmethod
    def FMOV(RG: List[int], R0: int, R1: int) -> None:
        RG[R0] = RG[R1]

    @staticmethod
    def FRI(RG: List[int], R0: int, C: int) -> None:
        RG[R0] = C

    @staticmethod
    def FRD(RG: List[int], R0: int, R1: int, C: int) -> None:
        # TODO
        pass

    @staticmethod
    def FWD(RG: List[int], R0: int, R1: int, C: int) -> None:
        # TODO
        pass
