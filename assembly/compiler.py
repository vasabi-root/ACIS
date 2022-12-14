import re
import inspect
from assembly.cmds import SimpleCommands, JumpCommands
from assembly.regs import *
from assembly.syntax import *

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
        text = text.upper()
        # self.cmd_text = re.split('[;\n]+', text)
        # rm_emptyness(self.cmd_text)
        self.str_text = text.split('\n')
        self.str_num = len(self.str_text) if len(self.str_text) > 1 or self.str_text[0] != '' else 0
        
        self.cur_cmd = 0
        self.cur_str = 0

        self.markers = {}
        self.evals = []
        
        self.if_parsed = False
        
        
    def parse(self) -> None:
        for self.cur_str, cmd_str in enumerate(self.str_text):
            if (len(cmd_str) == 0):
                continue
            cmd_list = re.split(f'[ ,]+', cmd_str)
            rm_emptyness(cmd_list)
            if (cmd_list[0].count(':') == 1):
                self.parse_marker(cmd_list)
            
        self.parse_start_point()
        
        for self.cur_str, cmd_str in enumerate(self.str_text):
            if (len(cmd_str) == 0):
                self.evals.append(0)
                continue
            cmd_list = re.split(f'[ ,]+', cmd_str)
            rm_emptyness(cmd_list)
            if (cmd_list[0] in SIMPLE_COMMANDS):
                self.parse_simple_cmd(cmd_list)
            elif (cmd_list[0] in JUMP_COMMANDS):
                self.parse_jump_cmd(cmd_list)
            elif (cmd_list[0].count(':') != 1):
                raise CompileError(f'There is no command \'{cmd_list[0]}\'!', self.cur_str+1) 
        
        self.cur_cmd = PC_to_index()
        self.cmd_num = len(self.evals)
        self.if_parsed = True
        
    def set_cur_str(self, cmd_str) -> None:
        try:
            self.cur_str = self.str_text.index(cmd_str)
        except ValueError:
            for i, s in enumerate(self.str_text):
                if (s.find(cmd_str) != -1):
                    self.cur_str = i
                    break
        
    def play_step(self):
        
        # CompileError ???????????? ?? assembly.__init__ !!!
        
        if (not self.if_parsed):
            self.parse()
            
        self.cur_cmd = PC_to_index()
        if (self.str_num > 0 and self.cur_cmd < self.cmd_num):
            if (self.evals[self.cur_cmd] == 0):
                inc_PC()
                self.play_step()
            else: # self.str_num > 0 and 
                eval_expr = self.evals[self.cur_cmd]
                
                old_pc = get_PC()
                self.cur_str = eval_expr[0]
                try:
                    eval(eval_expr[1])
                except NameError as name_er:
                    raise CompileError('There is no instance \'' + name_er.name + '\'' , self.cur_str+1)
                except Exception:
                    raise CompileError('Syntax error' , self.cur_str+1)
                
                inc_PC()
        else:
            inc_PC()
            self.cur_cmd = PC_to_index()
            
            
    def parse_simple_cmd(self, cmd_list: []) -> None:
        eval_str = f'SimpleCommands.{cmd_list[0]}('
        
        for i in range(1, len(cmd_list)):
            s = re.split('[R]+', str(cmd_list[i]))
            rm_emptyness(s)
            if (cmd_list[i] in FLAGS):
                eval_str += str(FLAGS.index(cmd_list[i])) + ', '
            else:
                eval_str += s[0] + ', '
            
        if (len(cmd_list) > 1):
            eval_str = eval_str[:-2]
        eval_str += ')'
        
        self.evals.append([self.cur_str, eval_str])
        
        
    def parse_jump_cmd(self, cmd_list: []) -> None:
        eval_str = f'JumpCommands.{cmd_list[0]}('
        if cmd_list[0] == 'RET': # ?????????????????? ?? parse
            cur_cmd = 0
        elif cmd_list[0] == 'RJMP':
            eval_str += cmd_list[1]
            cur_cmd = self.cur_cmd + int(cmd_list[1])
        else: # other jumps
            try:
                eval_str += str(self.markers[cmd_list[1]])
            except KeyError:
                raise CompileError(f'Marker \'{cmd_list[1]}\' does not exists!', self.cur_str+1)
            
        eval_str += ')'
        self.evals.append([self.cur_str, eval_str])
            
            
    def parse_marker(self, cmd_list: []) -> None:
        marker = re.split(f':', cmd_list[0])[0]
        try:
            self.markers[marker]
            raise CompileError(f'Marker \'{marker}\' already exists!', self.cur_str+1)
        except KeyError:
            self.markers[marker] = OFFSET + (self.cur_str - len(self.markers) - 1)*COMMAND_SIZE
            
    
    def parse_start_point(self) -> None:
        try:
            set_PC(self.markers[START_POINT] + COMMAND_SIZE)
        except KeyError:
            set_PC(OFFSET)
            
            
def rm_emptyness(str_list: []) -> None:
    try:
        str_list.remove('')
    except ValueError:
        pass
