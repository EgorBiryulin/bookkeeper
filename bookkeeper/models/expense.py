"""
Описан класс, представляющий расходную операцию
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Expense():
    """
    Расходная операция.
    pk - id записи в базе данных
    added_date - дата добавления в бд
    expense_date - дата расхода
    category - id категории расходов
    amount - сумма
    comment - комментарий
    """
    pk: int
    added_date: str
    expense_date: str
    category: str
    amount: float
    comment: str = ''

    def __init__(self, expense_date: str, category: str, amount: float, comment: str):
        self.pk: int = 0
        self.added_date = str(datetime.now())[:-7]
        self.expense_date = expense_date
        self.category = category
        self.amount = amount
        self.comment = comment
