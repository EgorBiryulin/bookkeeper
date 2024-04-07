# Описан класс, представляющий расходную операцию


from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Expense:
    # Модель расходной операции.

    # Параметры модели:
    # amount - сумма операции;
    # category - id категории расходов;
    # added_date - дата добавления в бд;
    # comment - комментарий;
    # pk - id записи в базе данных.

    expense_date: datetime = field(default_factory=datetime.now)
    added_date: datetime = field(default_factory=datetime.now)
    category: int = 0
    amount: float = 0
    comment: str = ''
    pk: int = None
