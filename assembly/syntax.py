from assembly.cmds import SimpleCommands, JumpCommands


MARKER = ['marker:', 'MARKER:']
SIMPLE_COMMANDS = [method for method in dir(SimpleCommands) if method.startswith('__') is False]
JUMP_COMMANDS = [method for method in dir(JumpCommands) if method.startswith('__') is False]
REGS = ['RG', 'FP', 'FLR']
FLAGS = [None, 'M', 'T', 'I', 'O', 'C', 'Z', 'S']
START_POINT = '_START'