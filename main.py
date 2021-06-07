import sys

from PyQt5 import QtWidgets, QtCore

from forms.ChoiseFrom import Ui_MatrixChoise
from core import (
    getWorshellMatrix,
    getBellmanMatrix
    )

from loguru import logger
import numpy as np

class Choise(QtWidgets.QMainWindow):
    def __init__(self):
        super(Choise, self).__init__()
        self.ui = Ui_MatrixChoise()
        self.ui.setupUi(self)

        self.ui.choise_btn.clicked.connect(self.getSize)
        self.ui.count_btn.clicked.connect(self.worshellMatrix)
        self.ui.row_choise_helper_lbl.clicked.connect(self.bellmanMatrix)
        self.ui.count_btn_2.clicked.connect(self.showBellman)
        self.ui.clear_btn.clicked.connect(self.clearMatrix)
        self.ui.return_btn.clicked.connect(self.returnToSize)
        self.status = ''

    def getSize(self):
        self.rows = self.ui.row_sb.value()
        self.cols = self.ui.col_sb.value()

        self.ui.col_sb.hide()
        self.ui.row_sb.hide()
        self.ui.col_lbl.hide()
        self.ui.row_lbl.hide()
        self.ui.choise_btn.hide()

        self.setWindowTitle('Заполните матрицу числами')

        self.ui.table.show()
        self.ui.table.setRowCount(self.rows)
        self.ui.table.setColumnCount(self.cols)
        self.ui.table.resize(900,600)
        self.ui.count_btn.show()
        self.ui.count_btn_2.show()
        self.ui.count_btn_3.show()
        self.ui.return_btn.show()
        self.ui.clear_btn.show()
        self.ui.help_lbl.show()

        self.setMinimumSize(QtCore.QSize(1200, 900))
        self.setMaximumSize(QtCore.QSize(1200, 900))
        self.move(self.pos().x() - 300, self.pos().y() - 200)

        if self.cols == 0 or self.rows == 0:
            self.ui.help_lbl.setText('Матрица задана неверно, попробуйте ещё раз')
            self.status = 'WRONG MATRIX SIZE'
        if self.cols > 1 and self.rows > 1:
            self.ui.help_lbl.setText('Матрица задана верно, можно заполнять числами')
            self.status = 'OK'
    
    def collectMatrix(self):
        self.matrix = []
        for row in range(self.rows):
            row_list = []
            for col in range(self.cols):
                str_element = self.ui.table.item(row,col)
                if str_element:
                    str_element = str_element.text()
                else:
                    str_element = '0'
                row_list.append(int(str_element))
            self.matrix.append(row_list)

    def worshellMatrix(self):

        if self.status == 'WRONG MATRIX SIZE':
            self.ui.help_lbl.setText('ОШИБКА!\nИзмените размерность матрицы')
        else:
            self.collectMatrix()
            logger.success(self.matrix)
            WorshellMatrix = getWorshellMatrix(self.matrix, self.rows, self.cols)
            
            self.setWindowTitle('Матрица под воздействием алгоритма Флойда-Уоршелла')

            for row in range(self.rows):
                for col in range(self.cols):
                    cellinfo = QtWidgets.QTableWidgetItem(str(WorshellMatrix[row][col]))
                    self.ui.table.setItem(row,col, cellinfo)
            self.ui.help_lbl.setText('Получили матрицу, под воздействием алгоритма Уоллшера-Флойда')

    def returnToSize(self):
        self.ui.col_sb.show()
        self.ui.row_sb.show()
        self.ui.col_lbl.show()
        self.ui.row_lbl.show()
        self.ui.choise_btn.show()

        self.setWindowTitle('Выберите размер матрицы')

        self.ui.table.hide()
        self.ui.count_btn.hide()
        self.ui.count_btn_2.hide()
        self.ui.count_btn_3.hide()
        self.ui.return_btn.hide()
        self.ui.clear_btn.hide()
        self.ui.help_lbl.hide()

        self.ui.row_choise_helper_lbl.hide()
        self.ui.row_choise_cb.hide()

        self.setMinimumSize(QtCore.QSize(600, 400))
        self.setMaximumSize(QtCore.QSize(600, 400))
        self.move(self.pos().x() + 300, self.pos().y() + 200)
        self.clearMatrix()

        if self.ui.row_choise_cb.count() > 0:
            for item in range(self.ui.row_choise_cb.count()):
                self.ui.row_choise_cb.removeItem(self.ui.row_choise_cb.currentIndex())
        
    def clearMatrix(self):
        self.ui.table.clear()

    def showBellman(self):
        self.ui.count_btn_2.hide()
        self.ui.row_choise_cb.show()
        self.ui.row_choise_helper_lbl.show()

        for row in range(self.rows):
            self.ui.row_choise_cb.addItem(f'{row + 1} точка', row)

    def bellmanMatrix(self):
        self.collectMatrix()
        logger.success(f'Выбранная позиция - {self.ui.row_choise_cb.currentData() + 1}')
        startpoint = self.ui.row_choise_cb.currentData() + 1
        ways = getBellmanMatrix(self.matrix, self.rows, self.cols, startpoint)
        logger.success(f'Кратчайшие пути: {ways}')
        self.ui.help_lbl.setText(f'Кратчайшие пути успешно вычислены!\nПолученные пути: {[way for way in ways]} для стартовой позиции {startpoint}')
        
app = QtWidgets.QApplication([])
application = Choise()
application.show()

sys.exit(app.exec())
