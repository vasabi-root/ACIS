# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QAbstractItemView
from PyQt5.QtWidgets import qApp, QTableWidget, QHeaderView
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import QFile
from PySide2.QtUiTools import QUiLoader

from parse_qt_palette import parse_xml
from form import Ui_Widget

class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__()
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        palette = qApp.palette()
        
        pathUI = os.fspath(Path(__file__).resolve().parent / "form.ui")
        pathPalette = os.fspath(Path(__file__).resolve().parent / "default_palette.xml")
        
        ui_file = QFile(pathUI)
        ui_file.open(QFile.ReadOnly)
        # loader.load(ui_file, self)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        
        tableInit(self.ui.tableRGP, 50)
        tableInit(self.ui.tableCPR, 50)
        tableInit(self.ui.tableMem, 30)
        
        palette = parse_xml(pathPalette)
        qApp.setPalette(palette)
        
        ui_file.close()

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

