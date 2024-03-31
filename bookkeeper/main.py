import sqlite3
from datetime import datetime, timedelta

from bookkeeper.models.budget import Budget
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.expense import Expense

SQLRepo = SQLiteRepository('db_file.db', Expense)

con = sqlite3.connect('db_file.db')
cursor = con.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS expense(pk INTEGER, added_date TEXT, expense_date TEXT, category TEXT, amount REAL, comment TEXT)')
con.commit()
con.close()

expence1 = Expense((str(datetime.now())[:-7]), 'Пиво', 69.69, 'Пиво для Илюши')
expence2 = Expense((str(datetime.now())[:-7]), 'Пиво', 69.69, 'Пиво для Илюши')

SQLRepo.add(expence1)
SQLRepo.add(expence2)

dailyBudget = Budget(1000, timedelta(days = 1))
print(dailyBudget.moneyAmount)
