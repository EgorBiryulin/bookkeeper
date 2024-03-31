import sqlite3
from datetime import datetime
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.expense import Expense

SQLRepo = SQLiteRepository('db_file.db', Expense)

con = sqlite3.connect('db_file.db')
cursor = con.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS expense(pk INTEGER, added_date TEXT, expense_date TEXT, category TEXT, amount REAL, comment TEXT)')

expence1 = Expense((str(datetime.now())[:-6]), 'Пиво', 69.69, 'Пиво для Илюши')
print(expence1.pk)

con.commit()
con.close()
