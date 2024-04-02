import sqlite3

from PySide6 import QtWidgets

from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.expense import Expense
from bookkeeper.view.view import expenses_table


SQLRepoExpense = SQLiteRepository('db_file_expense.db', Expense)
con = sqlite3.connect('db_file_expense.db')
cursor = con.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS expense(expense_date TEXT, category TEXT, amount REAL, comment TEXT)') #expense_date TEXT
con.commit()
con.close()

expense_list = MemoryRepository()
expense_list.init_db_at_start(SQLRepoExpense.get_all())

SQLRepoBudget = SQLiteRepository('db_file_budget.db', Budget)

budget_list = MemoryRepository()
budget_list.init_db_at_start(SQLRepoBudget.get_all())

SQLRepoCategory = SQLiteRepository('db_file_category.db', Category)
categories_list = MemoryRepository()
categories_list.init_db_at_start(SQLRepoCategory.get_all())
