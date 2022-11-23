from typing import Callable, List, Union
from cmds import Assembly

class Command:

    def __init__(self, 
            func : Callable[[int], None] = None, 
            regs:List[int] = None, 
            const:int = None, 
            com_str : str = None, 
            str_num : int = None,
            is_jump : bool = False,
            jump_lbl: str = None
            ) -> None:
        self.func = func
        self.regs = regs
        self.const = const
        self.com_str = com_str
        self.str_num = str_num
        self.is_jump = is_jump
        self.jump_lbl = jump_lbl


class Compiler:
    def __init__(self, text : Union[List[str], str]) -> None:
        self.text = text
        self.coms : List[Command] = []
        self.mem_labels = {}

        self.parse()
        
    def parse(self, text: Union[List[str], str] = None):
        if text is not None: self.text = text
        self.coms = []
        self.mem_labels.clear()
        t = self.text.split('\n')

        meths = [func for func in dir(Assembly) if callable(getattr(Assembly, func)) and not func.startswith("__") and func.isupper()]

        # all jump commands without RJMP
        # they accept label, not a num
        jump_coms = [i for i in meths if i.startswith('J')]
        jump_coms.append('CALL')
        # jump_coms.append('RET')

        for str_num, r in enumerate(t):
            # ignore all after ;
            r = r.split(';')[0].strip().lstrip()
            
            # memory label
            if r.find(':') != -1:
                lbl,r = r.split(':', maxsplit=1)
                lbl = lbl.strip().lstrip()
                if lbl in self.mem_labels.keys():
                    raise CompilerError(str_num, f'Label "{lbl}" already exists')
                self.mem_labels[lbl] = len(self.coms)

            # if string is empty
            if r.isspace() or len(r) == 0: continue
            
            # split row on [func, args]
            com_name, *args = r.split(maxsplit=1)
            com_name.upper()

            # No command
            if com_name not in meths:
                raise CompilerError(str_num, f'Wrong command name {com_name}')

            # Default args
            is_jump = False
            jmp_lbl = None
            if com_name in jump_coms:
                is_jump = True

            com_args = []
            const = None

            # Getting rid of whitespaces and split args
            if len(args):
                args = [arg.strip().lstrip() for arg in args[0].split(',')]

            # Go through all arguments
            for arg_num, arg in enumerate(args):
                try:
                    
                    # if arg is register
                    if arg.find('r') != -1:
                        a = arg.replace('r','',1)
                        if not a.isdigit():
                            raise CompilerError(str_num, f'Wrong argument #{arg_num} {arg}')
                        com_args.append(int(a))
                    
                    # if arg is const or label
                    else:
                        if is_jump:
                            jmp_lbl = arg
                        else:
                            const = int(arg)
                except:
                    raise CompilerError(str_num, f'Error in parsing argument #{arg_num} {arg}')
            
            com = Command(
                func = getattr(Assembly, com_name),
                regs = com_args,
                const= const,
                com_str = f'{com_name}' \
                    f'({", ".join(map(str, com_args))}'\
                    f'{f", " if len(com_args) and const is not None else ""}'\
                    f'{const if const is not None else ""})',
                str_num=str_num,
                is_jump=is_jump,
                jump_lbl=jmp_lbl
            )
            self.coms.append(com)


class CompilerError(Exception):
    ...

def main():
    with open('prog.txt', 'r') as f:
        content = f.read()
        # print(content)
        # print('----------')
        cmp = Compiler(content)

        for i in cmp.coms:
            print(i.com_str)
    pass

if __name__ == '__main__':
    main()