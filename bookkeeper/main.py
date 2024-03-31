import sqlite3
from datetime import datetime
from inspect import get_annotations
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.expense import Expense

SQLRepo = SQLiteRepository('db_file.db', Expense)

con = sqlite3.connect('db_file.db')
cursor = con.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS expense(ID INTEGER, added_date TEXT, expense_date TEXT, category TEXT, amount REAL, comment TEXT)')

expence1 = Expense
setattr(expence1, 'added_date', str(datetime.now())[:-6])
setattr(expence1, 'expense_date', str(datetime.now())[:-6])
setattr(expence1, 'category', 'Пиво')
setattr(expence1, 'amount', 69.69)
setattr(expence1, 'comment', 'Пиво для Илюши')
print(expence1.pk)

print(SQLRepo.add(expence1))

con.commit()
con.close()
