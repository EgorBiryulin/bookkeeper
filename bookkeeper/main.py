# Класс отвечает за запуск приложения
# Здесь объявляются репозитории и запускается приложение

import sys
import sqlite3

from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.view.presenter import Bookkeeper

# Основная БД (SQL), где содержится список покупок
SQLRepoExpenses = SQLiteRepository('db_file_expenses.db', Expense)
con = sqlite3.connect(SQLRepoExpenses.db_file)
cursor = con.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS expense(expense_date TEXT, category TEXT, amount REAL, comment TEXT)')
con.commit()
con.close()

# БД (SQL), где содержится список категорий
SQLRepoCategories = SQLiteRepository('db_file_categories.db', Category)
con = sqlite3.connect(SQLRepoCategories.db_file)
cursor = con.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS category(name TEXT, parent TEXT)')
con.commit()
con.close()

bookkeeper = Bookkeeper(SQLRepoExpenses,SQLRepoCategories)
bookkeeper.view.window.show()
sys.exit(bookkeeper.view.app.exec())
