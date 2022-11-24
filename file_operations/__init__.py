from form import Ui_widget

from PyQt5.QtCore import QTextCodec
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QFileDialog, QMessageBox
)

from parse_qt_palette import parse_xml
from pathlib import Path
import os

class File_Opers:
    def __init__(self, ui: Ui_widget, widget: QWidget) -> None:
        self.ui = ui
        self.widget = widget
        self.file_name = None
        self.f = None
        self.if_changed = False
        
        pathPalette = os.fspath(Path(__file__).resolve().parent / "../default_palette.xml")
        self.palette = parse_xml(pathPalette)
        
        self.ui.pushButtonOpen.clicked.connect(self.open)
        self.ui.pushButtonSave.clicked.connect(self.save)
        self.ui.textEditCode.textChanged.connect(self.state_changed)
        self.ui.pushButtonSaveAs.clicked.connect(self.save_as)
        self.ui.pushButtonClose.clicked.connect(self.close)
        
    def open(self) -> None:
        if (self.if_changed):
            self.close()
        self.file_name = QFileDialog.getOpenFileName(
            self.widget,
            'Open file', 
            os.getcwd(), 
            'ASM file (*.asm);;'
        )[0]
        if (len(self.file_name) > 0):
            try:
                self.f = open(self.file_name, "r")
                self.ui.textEditCode.setText(self.f.read())
            except Exception:
                self.show_error_msg('Cannot read this file!')
                
            self.f = None
            self.if_changed = False
    
    def save(self) -> None:
        if (not self.f):
            self.save_as()
        elif (self.if_changed):
            self.f.close()
            
            self.f = open(self.file_name, "w")
            self.f.write(self.ui.textEditCode.toPlainText())
            
            self.f = open(self.file_name, "r")
            self.ui.textEditCode.setText(self.f.read())
            
        self.if_changed = False
            
    def state_changed(self) -> None:
        self.if_changed = True
        
    def save_as(self) -> None:
        if (self.f):
            self.f.close
        self.file_name = QFileDialog.getSaveFileName(
            self.widget,
            'Save file as', 
            os.getcwd(), 
            'ASM file (*.asm);;'
        )[0]
        if (len(self.file_name) > 0):
            self.f = open(self.file_name, "w")
            self.f.write(self.ui.textEditCode.toPlainText())
        
        self.if_changed = False
        
    def close(self) -> None:
        if (self.if_changed):
            return_val = self.show_save_msg()
            if (return_val == QMessageBox.Yes):
                if (self.f):
                    self.save()
                else:
                    self.save_as()
            elif (return_val == QMessageBox.No):
                self.ui.textEditCode.setText('')
        else:
            self.ui.textEditCode.setText('')
            
    def show_save_msg(self) -> int:
        self.save_msg = QMessageBox()
        self.save_msg.setStyleSheet('color: black;')
        self.save_msg.setIcon(QMessageBox.Information)
        self.save_msg.setText('Do you want to save changes?')
        self.save_msg.setWindowTitle('Save warning')
        self.save_msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        return self.save_msg.exec()

    def show_error_msg(self, msg: str) -> None:
        self.err_msg = QMessageBox()
        self.err_msg.setStyleSheet('color: black;')
        self.err_msg.setIcon(QMessageBox.Critical)
        self.err_msg.setWindowTitle('Open file error')
        self.err_msg.setText(msg)
        self.err_msg.exec()
                
            
        