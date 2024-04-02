import sqlite3

from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.expense import Expense
from bookkeeper.view.view import View


def countSpents(self, budget: Budget):
    con = sqlite3.connect(self.db_file)
    cursor = con.cursor()
    cursor.execute(
        f'SELECT SUM(amount) FROM {self.table_name} WHERE expense_date>{str(datetime.now() - budget.duration)[-8]}', )
    sum = cursor.fetchone()[0]
    con.commit()
    con.close()
    budget.moneyAmount = sum


def update_view():
    expense_database = SQLRepoExpense.get_all()


SQLRepoExpense = SQLiteRepository('db_file_expense.db', Expense)
con = sqlite3.connect('db_file_expense.db')
cursor = con.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS expense(pk INTEGER, added_date TEXT, expense_date TEXT, category TEXT, amount REAL, comment TEXT)')
con.commit()
con.close()

SQLRepoBudget = SQLiteRepository('db_file_budget.db', Budget)
budget_list = SQLRepoBudget.get_all()

SQLRepoCategory = SQLiteRepository('db_file_category.db', Category)
categories_list = SQLRepoCategory.get_all()
