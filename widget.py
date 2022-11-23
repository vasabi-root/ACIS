# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QAbstractItemView
from PyQt5.QtWidgets import qApp, QTableWidget, QHeaderView
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import QFile, Qt
from PySide2.QtUiTools import QUiLoader

from parse_qt_palette import parse_xml
from form import Ui_Widget
from file_operations import File_Opers
from assembly import Assembly_Opers

class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__()
        self.load_ui()

    def load_ui(self):
        palette = qApp.palette()
        pathPalette = os.fspath(Path(__file__).resolve().parent / "default_palette.xml")
        
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        
        tableInit(self.ui.tableRGP, 50)
        tableInit(self.ui.tableCPR, 50)
        tableInit(self.ui.tableMem, 30)
        
        self.synchro_scroll()
        
        palette = parse_xml(pathPalette)
        qApp.setPalette(palette)
        
        self.file = File_Opers(self.ui, self)
        self.assembly = Assembly_Opers(self.ui, self)
        self.setWindowTitle('ACIS SQUAD RISC')
        
        
    def synchro_scroll(self) -> None:
        text_editors = [self.ui.textEditCode, self.ui.textEditNums, self.ui.textEditStep]
        for t1 in text_editors:
            for t2 in text_editors:
                if (t1 != t2):
                    t1.verticalScrollBar().valueChanged.connect(t2.verticalScrollBar().setValue)
        
        self.ui.textEditNums.setAlignment(Qt.AlignRight)
        self.ui.textEditStep.setAlignment(Qt.AlignRight)
        self.ui.textEditNums.verticalScrollBar().setVisible(False)
        self.ui.textEditStep.verticalScrollBar().setVisible(False)

def tableInit(table: QTableWidget, width: int) -> None:
    table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
    for i in range(table.columnCount()):
        table.setColumnWidth(i, width)
    # map(lambda i: table.setColumnWidth(i, 20), range(table.columnCount()))


if __name__ == "__main__":
    app = QApplication([])
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())

