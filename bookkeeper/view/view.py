import sys

from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui


# Создание и запуск окна
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
window.setWindowTitle('The Bookkeeper App')
window.resize(600, 600)

central_widget = QtWidgets.QWidget()
window.setCentralWidget(central_widget)

vertical_layout = QtWidgets.QVBoxLayout()
central_widget.setLayout(vertical_layout)
window.show()


# Список последних расходов
expenses_text = "Последние расходы"
expenses_widget = QtWidgets.QLabel(expenses_text)
vertical_layout.addWidget(expenses_widget)

expenses_table = QtWidgets.QTableWidget(4, 20)
expenses_table.setColumnCount(4)
expenses_table.setRowCount(20)
expenses_table.setHorizontalHeaderLabels("Дата Сумма Категория Комментарий".split())

header = expenses_table.horizontalHeader()
header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

expenses_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
expenses_table.verticalHeader().hide()
vertical_layout.addWidget(expenses_table)



budget_text = "Бюджет"
budget_widget = QtWidgets.QLabel(budget_text)
vertical_layout.addWidget(budget_widget)

budget_table = QtWidgets.QTableWidget(2, 3)
budget_table.setColumnCount(2)
budget_table.setRowCount(3)

budget_table.setHorizontalHeaderLabels(
    "Сумма Бюджет".split())
header = budget_table.horizontalHeader()
header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

budget_table.setVerticalHeaderLabels(
            "День Неделя Месяц".split())
header = budget_table.verticalHeader()
header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

budget_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
#expenses_table.verticalHeader().hide()


data = [row.split('|') for row in '''
    705.43|1000
    6719.43|7000
    10592.96|30000
    '''.strip().splitlines()]
#set_data(data)

vertical_layout.addWidget(budget_table)



grid_layout = QtWidgets.QGridLayout()

sum_text = "Сумма"
sum_widget = QtWidgets.QLabel(sum_text)
grid_layout.addWidget(sum_widget,0,0)

edit_line = QtWidgets.QLineEdit('0')
grid_layout.addWidget(edit_line,0,1)

category_text = "Категория"
category_widget = QtWidgets.QLabel(category_text)
grid_layout.addWidget(category_widget,1,0)

combobox_text = ["Продукты", "Книги", "Одежда"]
combobox_widget = QtWidgets.QComboBox()
for item in combobox_text:
    combobox_widget.addItem(item)
grid_layout.addWidget(combobox_widget,1,1)


edit_text = "Редактировать"
edit_button = QtWidgets.QPushButton(edit_text)
grid_layout.addWidget(edit_button,1,2)

add_button = QtWidgets.QPushButton()
add_text = "Добавить"
add_button.setText(add_text)
grid_layout.addWidget(add_button,2,1)

vertical_layout.addLayout(grid_layout,-1)

sys.exit(app.exec())


