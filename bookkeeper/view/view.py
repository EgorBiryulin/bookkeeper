import sys
from typing import Callable

from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6.QtWidgets import QMessageBox, QWidget, QPushButton
from setuptools.config._validate_pyproject import ValidationError

from bookkeeper.view.abstract_view import AbstractView

def handle_error(widget, handler):
    def inner(*args, **kwargs):
        try:
            handler(*args, **kwargs)
        except ValidationError as ex:
            QMessageBox.critical('Ошибка', str(ex))
    return inner


class View(QWidget):

    cat_modifier: any = None
    cat_adder: any = None
    cat_deleter: any = None

    def __init__(self, add_handler: Callable):
        # Создание и запуск окна
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = QtWidgets.QMainWindow()
        self.window.setWindowTitle('The Bookkeeper App')
        self.window.resize(600, 600)

        self.central_widget = QtWidgets.QWidget()
        self.window.setCentralWidget(self.central_widget)

        self.vertical_layout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(self.vertical_layout)

        # Список последних расходов
        self.expenses_text = "Последние расходы"
        self.expenses_widget = QtWidgets.QLabel(self.expenses_text)
        self.vertical_layout.addWidget(self.expenses_widget)

        self.expenses_table = QtWidgets.QTableWidget(4, 20)
        self.expenses_table.setColumnCount(4)
        self.expenses_table.setRowCount(20)
        self.expenses_table.setHorizontalHeaderLabels("Дата Сумма Категория Комментарий".split())

        self.header = self.expenses_table.horizontalHeader()
        self.header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        self.expenses_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.expenses_table.verticalHeader().hide()
        self.vertical_layout.addWidget(self.expenses_table)

        self.budget_text = "Бюджет"
        self.budget_widget = QtWidgets.QLabel(self.budget_text)
        self.vertical_layout.addWidget(self.budget_widget)

        self.budget_table = QtWidgets.QTableWidget(2, 3)
        self.budget_table.setColumnCount(2)
        self.budget_table.setRowCount(3)

        self.budget_table.setHorizontalHeaderLabels(
            "Сумма Бюджет".split())
        self.header = self.budget_table.horizontalHeader()
        self.header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        self.budget_table.setVerticalHeaderLabels(
            "День Неделя Месяц".split())
        self.header = self.budget_table.verticalHeader()
        self.header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

        self.budget_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)


        self.vertical_layout.addWidget(self.budget_table)

        self.grid_layout = QtWidgets.QGridLayout()

        self.sum_text = "Сумма"
        self.sum_widget = QtWidgets.QLabel(self.sum_text)
        self.grid_layout.addWidget(self.sum_widget, 0, 0)

        self.edit_line = QtWidgets.QLineEdit('0')
        self.grid_layout.addWidget(self.edit_line, 0, 1)

        edit_text = "Добавить категорию"
        self.edit_button = QtWidgets.QPushButton(edit_text)
        #edit_button.clicked.connect(bookkeeper.add_category())
        self.grid_layout.addWidget(self.edit_button, 1, 2)


        add_text = "Добавить"
        self.add_button = QPushButton(add_text)
        self.grid_layout.addWidget(self.add_button, 2, 1)
        self.add_button.clicked.connect(add_handler)

        self.vertical_layout.addLayout(self.grid_layout, -1)

        self.category_text = "Категория"
        self.category_widget = QtWidgets.QLabel(self.category_text)
        self.grid_layout.addWidget(self.category_widget, 1, 0)

        self.combobox_text = ["Продукты", "Книги", "Одежда"]
        self.combobox_widget = QtWidgets.QComboBox()
        for item in self.combobox_text:
            self.combobox_widget.addItem(item)
        self.grid_layout.addWidget(self.combobox_widget, 1, 1)



    def register_cat_modifier(self, handler):
        self.register_cat_modifier = handle_error(self, handler)

    def register_cat_adder(self, handler):
        self.cat_adder = handle_error(self.cat_adder, handler)

    def register_cat_deleter(self, widget, handler):
        self.cat_deleter = handle_error(widget, handler)
