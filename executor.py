from compiler import Compiler, Command
from regs import get_PC, set_PC, PC, FLR
from cmds import Assembly

START_LABEL = '_start'
COM_SIZE = 4

class Executioner:
    def __init__(self, comp: Compiler) -> None:
        self.comp = comp
        self.cur_cm_idx = 0
        self.start_point = None

    def put_to_mem(self):
        self.start_point = 1024
        if START_LABEL in self.comp.mem_labels.keys():
            self.cur_cm_idx = self.comp.mem_labels[START_LABEL]
            set_PC(self.start_point + COM_SIZE * self.cur_cm_idx)
        ...

    def reset(self):
        self.cur_cm_idx = 0
        self.start_point = None

    def run_all(self):
        self.reset()
        next_com = None

        while True:
            next_com = self.run_step()
            if next_com is None:
                break
            print(next_com.com_str)

    def run_step(self, cur_idx = None) -> Command:
        if self.start_point is None:
            self.put_to_mem()
            

        if cur_idx is not None:
            self.cur_cm_idx = cur_idx

        if self.cur_cm_idx >= len(self.comp.coms):
            return None

        try:
            cm = self.comp.coms[self.cur_cm_idx]
            if cm.is_jump:
                old_pc = get_PC()
                cm.func(self.comp.mem_labels[cm.jump_lbl] * COM_SIZE + self.start_point)
                if old_pc != get_PC():
                    self.cur_cm_idx = self.comp.mem_labels[cm.jump_lbl]
                    return self.comp.coms[self.cur_cm_idx]
            elif cm.func is Assembly.RJMP:
                if get_PC() + cm.const * COM_SIZE < 0 or (self.cur_cm_idx + cm.const > len(self.comp.coms) ): raise Exception()
                set_PC(get_PC() + cm.const * COM_SIZE) 
                self.cur_cm_idx += cm.const
                return self.comp.coms[self.cur_cm_idx]
            elif cm.func is Assembly.RET:
                old_pc = get_PC()
                cm.func()
                new_pc = get_PC()
                self.cur_cm_idx = self.cur_cm_idx + (new_pc - old_pc) // COM_SIZE
            else: 
                eval('Assembly.'+cm.com_str)
                
            set_PC(get_PC() + COM_SIZE)
            self.cur_cm_idx += 1
            if self.cur_cm_idx >= len(self.comp.coms):
                return None

            return self.comp.coms[self.cur_cm_idx]

        except IndexError as e:
            raise ExecError(f'No command with idx {self.cur_cm_idx}')
        except Exception as e:
            # print(e.args)
            n_e = ExecError(f'Error in command by line {cm.str_num} : \n{e.args}')
            
            raise n_e

class ExecError(Exception):
    ...

def main():
    with open('prog.txt', 'r') as f:
        content = f.read()
        # print(content)
        # print('----------')
        cmp = Compiler(content)

    ex = Executioner(cmp)
    ex.run_all()

if __name__ == '__main__':
    main()