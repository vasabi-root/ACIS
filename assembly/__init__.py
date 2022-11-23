from form import Ui_Widget

from PyQt5.QtCore import QTextCodec
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QFileDialog, QMessageBox,
    QTableWidgetItem, 
)

import os
from assembly.compiler import Compiler, CompileError
from assembly.regs import *

class Assembly_Opers:
    def __init__(self, ui: Ui_Widget, widget: QWidget) -> None:
        self.ui = ui
        self.widget = widget
        self.compiler = Compiler()
        self.reset()
        
        self.ui.textEditCode.textChanged.connect(self.text_update)
        self.ui.pushButtonPlay.clicked.connect(self.play)
        self.ui.pushButtonStep.clicked.connect(self.step)
        self.ui.pushButtonReset.clicked.connect(self.reset)
        
        
    def text_update(self) -> None:
        self.compiler.set_text(self.ui.textEditCode.toPlainText())
        
        scroll_pos = self.ui.textEditCode.verticalScrollBar().value()
        self.ui.textEditNums.setText(
            '\n'.join([ str(i) for i in range(1, self.compiler.str_num+1) ])
        )
        self.ui.textEditStep.setText('\n' * self.compiler.str_num)
        self.ui.textEditNums.verticalScrollBar().setValue(scroll_pos)
        
        
    def reset(self) -> None:
        reset_regs()
        self.text_update()
        self.update_ui()
        
        
    def play(self) -> None:
        # for _ in self.compiler.evals:
        while (not self.step()): ...
        
        
    def step(self) -> bool:
        try:
            self.compiler.play_step()
            self.update_ui()
            self.set_arrow()
        except CompileError as comp_err:
            self.set_arrow()
            self.show_error_msg(comp_err)
            return True
            
        if (self.compiler.cur_cmd == len(self.compiler.evals)):
            self.show_done_msg()
            return True

        return False
            
            
    def update_ui(self) -> None:
        self.update_RG()
    
    
    def update_RG(self) -> None:
        for row in range(self.ui.tableRGP.rowCount()):
            item = QTableWidgetItem(str(RG[row]))
            self.ui.tableRGP.setItem(row, 0, item)
            
            
    def update_CPR(self) -> None:
        for row in range(self.ui.tableCPR.rowCount()):
            item = QTableWidgetItem(str(RG[row]))
            self.ui.tableCPR.setItem(row, 0, item)
            
            
    def set_arrow(self) -> None:
        scroll_pos = self.ui.textEditCode.verticalScrollBar().value()
        self.ui.textEditStep.setText('\n'*self.compiler.cur_str + '->' + '\n'*(self.compiler.str_num-(self.compiler.cur_str+1)))
        self.ui.textEditStep.verticalScrollBar().setValue(scroll_pos)
        
        
    def show_error_msg(self, comp_err: CompileError) -> None:
        self.err_msg = QMessageBox()
        self.err_msg.setStyleSheet('color: black;')
        self.err_msg.setIcon(QMessageBox.Critical)
        self.err_msg.setWindowTitle('Compile Error')
        self.err_msg.setText(comp_err.text)
        self.err_msg.exec()
        
        
    def show_done_msg(self) -> None:
        self.done_msg = QMessageBox()
        self.done_msg.setStyleSheet('color: black;')
        self.done_msg.setIcon(QMessageBox.Information)
        self.done_msg.setWindowTitle('Compile message')
        self.done_msg.setText('All done!')
        self.done_msg.exec()