"""
Описан класс, представляющий бюджет
"""
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(slots=True)
class Budget():
    """
    Расходная операция.
    pk - id записи в базе данных
    added_date - дата добавления в бд
    expense_date - дата расхода
    category - id категории расходов
    amount - сумма
    comment - комментарий
    """
    plan: float
    duration: timedelta
    moneyAmount: float

    def __init__(self, plan: float, duration: timedelta):
        self.plan = plan
        self.duration = duration
        self.moneyAmount = self.countMoney()

    def countMoney(self) -> float:
        con = sqlite3.connect('db_file.db')
        cursor = con.cursor()
        cursor.execute(f'SELECT SUM(amount) FROM expense WHERE expense_date>{str(datetime.now()-self.duration)[-8]}',)
        sum = cursor.fetchone()[0]
        con.commit()
        con.close()
        return sum
