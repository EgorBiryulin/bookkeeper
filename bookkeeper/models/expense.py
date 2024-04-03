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

    amount: float = 0
    category: int = 0
    expense_date: datetime = field(default_factory=datetime.now)
    added_date: datetime = field(default_factory=datetime.now)
    comment: str = ''
    pk: int = None
