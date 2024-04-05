# Класс View отвечает за создание интерфейса и вывод информации на экран

import sys
from setuptools.config._validate_pyproject import ValidationError

from PySide6 import QtWidgets
from PySide6.QtWidgets import QMessageBox, QPushButton

from bookkeeper.view.abstract_view import AbstractView


def handle_error(handler):
    def inner(*args, **kwargs):
        try:
            handler(*args, **kwargs)
        except ValidationError as ex:
            QMessageBox.critical('Ошибка', str(ex))

    return inner


class View(AbstractView):
    cat_modifier: any = None
    cat_adder: any = None
    cat_deleter: any = None

    def __init__(self):
        # Создание и запуск окна
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = QtWidgets.QMainWindow()
        self.window.setWindowTitle('The Bookkeeper App')
        self.window.resize(800, 600)

        self.central_widget = QtWidgets.QWidget()
        self.window.setCentralWidget(self.central_widget)

        self.vertical_layout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(self.vertical_layout)

        # Список последних расходов
        # Заголовок списка расходов
        self.expenses_table_label = QtWidgets.QLabel("Последние расходы")  # Заголовок списка
        self.vertical_layout.addWidget(self.expenses_table_label)

        # Список расходов
        # Таблица последних расходов
        self.expenses_table = QtWidgets.QTableWidget(20, 4)
        self.expenses_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # Подписи столбцов таблицы
        self.expenses_table.setHorizontalHeaderLabels("Дата Сумма Категория Комментарий".split())
        self.expenses_table_header = self.expenses_table.horizontalHeader()

        # Настройки масштабирования столбцов
        self.expenses_table_header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.expenses_table_header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.expenses_table_header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.expenses_table_header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.vertical_layout.addWidget(self.expenses_table)

        # Список бюджетов и бюджетных ограничений
        # Заголовок списка бюджетов
        self.budget_table_label = QtWidgets.QLabel("Бюджет")
        self.vertical_layout.addWidget(self.budget_table_label)

        # Список бюджетов
        self.budget_table = QtWidgets.QTableWidget(3, 2)

        # Подписи столбцов таблицы
        self.budget_table.setHorizontalHeaderLabels("Сумма Бюджет".split())
        self.budget_table_header_horizont = self.budget_table.horizontalHeader()

        # Настройки масштабирования столбцов
        self.budget_table_header_horizont.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.budget_table_header_horizont.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        # Подписи столбцов таблицы (вертикальные)
        self.budget_table.setVerticalHeaderLabels("День Неделя Месяц".split())
        self.budget_table_header_vert = self.budget_table.verticalHeader()

        # Настройки масштабирования столбцов
        self.budget_table_header_vert.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.budget_table_header_vert.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.budget_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.vertical_layout.addWidget(self.budget_table)

        # Создание сетки для расположения элементов окна
        self.grid_layout = QtWidgets.QGridLayout()

        # Настройка виджетов, с которыми будет взаимодействовать пользователь
        # Подписи
        # Подпись строки вводимой денежной суммы
        self.sum_widget = QtWidgets.QLabel("Сумма")
        self.grid_layout.addWidget(self.sum_widget, 1, 0)

        # Подпись списка категорий
        self.category_widget = QtWidgets.QLabel("Категория")
        self.grid_layout.addWidget(self.category_widget, 2, 0)

        # Подпись списка категорий
        self.category_widget = QtWidgets.QLabel("Новая категория")
        self.grid_layout.addWidget(self.category_widget, 3, 0)

        # Cтрока вводимой денежной суммы
        self.expense_money_line = QtWidgets.QLineEdit('0')
        self.grid_layout.addWidget(self.expense_money_line, 1, 1)

        # Элементы с взаимодействием
        # Список категорий (выпадающий список)
        self.category_combobox = QtWidgets.QComboBox()
        self.grid_layout.addWidget(self.category_combobox, 2, 1)

        # Строка для ввода новой категории
        self.new_category_line = QtWidgets.QLineEdit(
            'Новая категория (родительской будет считаться категория, выбранная в списке)')
        self.grid_layout.addWidget(self.new_category_line, 3, 1)

        # Кнопки
        # Кнопка редактирования списка расходов и бюджета
        self.edit_expense_button = QPushButton("Редактировать")
        self.grid_layout.addWidget(self.edit_expense_button, 0, 0, 1, 4)

        # Кнопка добавления расхода
        self.add_expense_button = QPushButton("Добавить расход")
        self.grid_layout.addWidget(self.add_expense_button, 1, 2)

        # Кнопка удаления категории
        self.delete_category_button = QtWidgets.QPushButton("Удалить категорию")
        self.grid_layout.addWidget(self.delete_category_button, 2, 2)

        # Кнопка добавления категории
        self.add_category_button = QtWidgets.QPushButton("Новая категория")
        self.grid_layout.addWidget(self.add_category_button, 3, 2)

        self.vertical_layout.addLayout(self.grid_layout, -1)

    def register_expenses_budget_modifier(self, handler):
        self.edit_expense_button.clicked.connect(handle_error(handler))

    def register_expenses_adder(self, handler):
        self.add_expense_button.clicked.connect(handle_error(handler))

    def register_category_deleter(self, handler):
        self.delete_category_button.clicked.connect(handle_error(handler))

    def register_category_adder(self, handler):
        self.add_category_button.clicked.connect(handle_error(handler))

    def update_category_combobox(self, category_names_list: [str]) -> None:
        self.category_combobox.clear()
        self.category_combobox.addItem("")
        for item in category_names_list:
            self.category_combobox.addItem(item)

    def get_selected_category(self) -> int:
        return self.category_combobox.currentIndex()

    def get_new_category_name(self):
        return self.new_category_line.text()
