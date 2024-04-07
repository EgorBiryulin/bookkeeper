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
        # Добавить расход
        delete_expense_label = QtWidgets.QLabel("Добавить расход:")
        self.grid_layout.addWidget(delete_expense_label, 1, 0, 1, 3)

        # Подпись строки вводимой денежной суммы
        sum_widget_label = QtWidgets.QLabel("Сумма")
        self.grid_layout.addWidget(sum_widget_label, 2, 0)

        # Подпись списка категорий
        expenses_comment_widget_label = QtWidgets.QLabel("Комментарий")
        self.grid_layout.addWidget(expenses_comment_widget_label, 3, 0)

        # Подпись списка категорий
        category_widget_label = QtWidgets.QLabel("Категория")
        self.grid_layout.addWidget(category_widget_label, 4, 0)

        # Редактировать список категорий и расходов
        redactor_label = QtWidgets.QLabel("Редактировать список категорий и расходов:")
        self.grid_layout.addWidget(redactor_label, 5, 0, 1, 3)

        # Подпись комментария
        delete_expense_label = QtWidgets.QLabel("Удалить расход по номеру")
        self.grid_layout.addWidget(delete_expense_label, 6, 0)

        # Подпись комментария
        category_new_widget_label = QtWidgets.QLabel("Новая категория")
        self.grid_layout.addWidget(category_new_widget_label, 7, 0)

        # Строки для ввода номеров и т.д.
        # Cтрока нового бюджетного ограничения
        self.new_budget_line = QtWidgets.QLineEdit('0')
        self.grid_layout.addWidget(self.new_budget_line, 0, 1)

        # Cтрока вводимой денежной суммы
        self.expense_money_line = QtWidgets.QLineEdit('0')
        self.grid_layout.addWidget(self.expense_money_line, 2, 1)

        # Cтрока ввода комментария
        self.comment_line = QtWidgets.QLineEdit('Комментарий')
        self.grid_layout.addWidget(self.comment_line, 3, 1)

        # Cтрока ввода удаляемого расхода
        self.delete_expense_number = QtWidgets.QLineEdit('Число от 1')
        self.grid_layout.addWidget(self.delete_expense_number, 6, 1)

        # Строка для ввода новой категории
        self.new_category_line = QtWidgets.QLineEdit(
            'Новая категория (родительской будет считаться категория, выбранная в списке)')
        self.grid_layout.addWidget(self.new_category_line, 7, 1)

        # Элементы с взаимодействием
        # Список бюджетов (выпадающий список)
        self.budget_combobox = QtWidgets.QComboBox()
        self.budget_combobox.addItem("День")
        self.budget_combobox.addItem("Неделя")
        self.budget_combobox.addItem("Месяц")
        self.grid_layout.addWidget(self.budget_combobox, 0, 0)

        # Список категорий (выпадающий список)
        self.category_combobox = QtWidgets.QComboBox()
        self.grid_layout.addWidget(self.category_combobox, 4, 1)

        # Кнопки
        # Кнопка обновления бюджета
        self.update_budget_button = QPushButton("Обновить бюджетное ограничение")
        self.grid_layout.addWidget(self.update_budget_button, 0, 2)

        # Кнопка добавления расхода
        self.add_expense_button = QPushButton("Добавить расход")
        self.grid_layout.addWidget(self.add_expense_button, 2, 2, 2, 1)

        # Кнопка удаления категории
        self.delete_category_button = QtWidgets.QPushButton("Удалить категорию")
        self.grid_layout.addWidget(self.delete_category_button, 4, 2)

        # Кнопка удаления расхода
        self.delete_expense_button = QtWidgets.QPushButton("Удалить расход")
        self.grid_layout.addWidget(self.delete_expense_button, 6, 2)

        # Кнопка добавления категории
        self.add_category_button = QtWidgets.QPushButton("Новая категория")
        self.grid_layout.addWidget(self.add_category_button, 7, 2)

        self.vertical_layout.addLayout(self.grid_layout, -1)

    def register_budget_updater(self, handler):
        self.update_budget_button.clicked.connect(handle_error(handler))

    def register_expenses_adder(self, handler):
        self.add_expense_button.clicked.connect(handle_error(handler))

    def register_category_deleter(self, handler):
        self.delete_category_button.clicked.connect(handle_error(handler))

    def register_expenses_deleter(self, handler):
        self.delete_expense_button.clicked.connect(handle_error(handler))

    def register_category_adder(self, handler):
        self.add_category_button.clicked.connect(handle_error(handler))

    def update_category_combobox(self, category_names_list: [str]) -> None:
        self.category_combobox.clear()
        self.category_combobox.addItem("")
        for item in category_names_list:
            self.category_combobox.addItem(item)

    def get_selected_budget(self) -> int:
        return self.budget_combobox.currentIndex()

    def get_new_budget_plan(self) -> int:
        return int(self.new_budget_line.text())

    def get_selected_category(self) -> int:
        return self.category_combobox.currentIndex()

    def get_new_category_name(self):
        return self.new_category_line.text()
