OFFSET = 1243 # OS вернула 
COMMAND_SIZE = 4 # Bytes

RG = [0 for _ in range(32)]
FP = [0 for _ in range(32)]

PC = OFFSET

MEM = [0 for _ in range(5000)]

FLR = 0
TLB = 0

def reset_regs() -> None:
    global RG
    global FP
    global PC
    global MEM
    global FLR
    global TLB
    
    for i in range(32):
        RG[i] = 0
        FP[i] = 0

    PC = OFFSET

    for i in range(5000):
        MEM[i] = 0

    FLR = 0
    TLB = 0

def S() -> int:
    return (FLR >> 7) & 1


def set_S() -> None:
    global FLR
    FLR |= (1 << 7)


def drop_S() -> None:
    global FLR
    FLR &= ~(1 << 7)


def Z() -> int:
    return (FLR >> 6) & 1


def set_Z() -> None:
    global FLR
    FLR |= (1 << 6)


def drop_Z() -> None:
    global FLR
    FLR &= ~(1 << 6)


def C() -> int:
    return (FLR >> 5) & 1


def set_C() -> None:
    global FLR
    FLR |= (1 << 5)


def drop_C() -> None:
    global FLR
    FLR &= ~(1 << 5)


def O() -> int:
    return (FLR >> 4) & 1


def set_O() -> None:
    global FLR
    FLR |= (1 << 4)


def drop_O() -> None:
    global FLR
    FLR &= ~(1 << 4)


def I() -> int:
    return (FLR >> 3) & 1


def set_I() -> None:
    global FLR
    FLR |= (1 << 3)


def drop_I() -> None:
    global FLR
    FLR &= ~(1 << 3)


def T() -> int:
    return (FLR >> 2) & 1


def set_T() -> None:
    global FLR
    FLR |= (1 << 2)


def drop_T() -> None:
    global FLR
    FLR &= ~(1 << 2)


def M() -> int:
    return (FLR >> 1) & 1


def set_M() -> None:
    global FLR
    FLR |= (1 << 1)


def drop_M() -> None:
    global FLR
    FLR &= ~(1 << 1)


def set_PC(value: int) -> None:
    global PC
    PC = value
    
def inc_PC() -> None:
    global PC
    set_PC(get_PC() + COMMAND_SIZE)


def get_PC() -> int:
    return PC

def PC_to_index() -> int:
    return int((PC-OFFSET) / COMMAND_SIZE)


def get_FLR() -> int:
    return FLR


def set_FLR(value: int) -> None:
    global FLR
    FLR |= value


def drop_FLR(value: int) -> None:
    global FLR
    FLR &= value


def get_TLB() -> int:
    return TLB


def set_TLB(value: int) -> None:
    global TLB
    TLB = value
