import re
import inspect
from assembly.cmds import SimpleCommands, JumpCommands
from assembly.regs import *
from assembly.syntax import *


def parse_asm(text: str) -> int:
    funcs = dir(SimpleCommands)
    regs = dir()
    strings = re.split('[;\n]+', text)
    for str in strings:
        print(str)
        cmd = re.split(f'[ ,]+', str)
        print(cmd)
        if (cmd[0] in funcs):
            # for i in range(1, len(cmd)):
            #     if (cmd[i] in )
            # eval(cmd[0] + '(' + ')')
            pass
        else:
            return -1

class CompileError(Exception):
    def __init__(self, text, str_num) -> None:
        self.text = text + f'\nString #{str(str_num)}' 

class Compiler:
    def __init__(self):
        self.markers = {}
        self.evals = []
        
        self.cmd_text = ''
        self.str_text = ''
        
        self.cmd_num = 0
        self.str_num = 0
        
        self.cur_cmd = 0
        self.cur_str = 0
        
        self.if_parsed = False
        
        
    def set_text(self, text: str) -> None:
        self.cmd_text = re.split('[;\n]+', text)
        rm_emptyness(self.cmd_text)
        self.str_text = text.split('\n')
        
        self.cmd_num = len(self.cmd_text) if self.cmd_text != None else 0
        self.str_num = len(self.str_text)
        
        self.cur_cmd = 0
        self.cur_str = 0

        self.markers = {}
        self.evals = []
        
        self.if_parsed = False
        
        
    def parse(self) -> None:
        for self.cur_cmd, cmd_str in enumerate(self.cmd_text):
            cmd_list = re.split(f'[ ,]+', cmd_str)
            rm_emptyness(cmd_list)
            if (cmd_list[0].count(':') == 1):
                self.parse_marker(cmd_list)
            
        self.parse_start_point()
        
        for self.cur_cmd, cmd_str in enumerate(self.cmd_text):
            cmd_list = re.split(f'[ ,]+', cmd_str)
            rm_emptyness(cmd_list)
            self.cur_str = self.str_text.index(cmd_str)
            if (cmd_list[0] in SIMPLE_COMMANDS):
                self.parse_simple_cmd(cmd_list)
            elif (cmd_list[0] in JUMP_COMMANDS):
                self.parse_jump_cmd(cmd_list)
            elif (cmd_list[0].count(':') != 1):
                raise CompileError(f'There is no command \'{cmd_list[0]}\'!', self.cur_str) 
        
        self.cur_cmd = PC_to_index()
        self.if_parsed = True
        
        
    def play_step(self):
        
        # CompileError ловить в assembly.__init__ !!!
        if (not self.if_parsed):
            self.parse()
        
        self.cur_cmd = PC_to_index()
        if (self.cmd_num > 0 and self.cur_cmd < len(self.evals)):
            eval_expr = self.evals[self.cur_cmd]
            
            old_pc = get_PC()
            
            eval(eval_expr[1])
            
            inc_PC()
            # if (PC_to_index() >= len(self.evals)):
                
            
            self.cur_str = eval_expr[0]
            
            
    def parse_simple_cmd(self, cmd_list: []) -> None:
        eval_str = f'SimpleCommands.{cmd_list[0]}('
        # parameters = []
        # parameters = eval(f're.split(f\'[\(\),]+| -> None\', str(inspect.signature(SimpleCommands.{cmd_list[0]})))')
        # rm_emptyness(parameters)
        
        for i in range(1, len(cmd_list)):
            s = re.split('[R]+', str(cmd_list[i]))
            rm_emptyness(s)
            eval_str += s[0] + ', '
            
            # eval_str += str(cmd_list[i]) + ', '
        if (len(cmd_list) > 1):
            eval_str = eval_str[:-2]
        eval_str += ')'
        
        self.evals.append([self.cur_str, eval_str])
        
        
    def parse_jump_cmd(self, cmd_list: []) -> None:
        eval_str = f'JumpCommands.{cmd_list[0]}('
        if cmd_list[0] == 'RET': # обработка в parse
            cur_cmd = 0
        elif cmd_list[0] == 'RJMP':
            eval_str += cmd_list[1]
            cur_cmd = self.cur_cmd + int(cmd_list[1])
        else: # other jumps
            try:
                eval_str += str(self.markers[cmd_list[1]])
            except KeyError:
                raise CompileError(f'Marker \'{cmd_list[1]}\' does not exists!', self.str_num)
            cur_cmd = (self.markers[cmd_list[1]] - OFFSET) / COMMAND_SIZE
            
        eval_str += ')'
        self.evals.append([self.cur_str, eval_str, cur_cmd])
            
            
    def parse_marker(self, cmd_list: []) -> None:
        marker = re.split(f':', cmd_list[0])[0]
        try:
            self.markers[marker]
            raise CompileError(f'Marker \'{marker}\' already exists!', self.str_num)
        except KeyError:
            self.markers[marker] = OFFSET + (self.cur_cmd - len(self.markers) - 1)*4
            
    
    def parse_start_point(self) -> None:
        try:
            # self.start_cmd = self.markers[START_POINT]
            set_PC(self.markers[START_POINT] + COMMAND_SIZE)
        except KeyError:
            # self.start_cmd = 0
            set_PC(OFFSET)
            
            
def rm_emptyness(str_list: []) -> None:
    try:
        str_list.remove('')
    except ValueError:
        pass