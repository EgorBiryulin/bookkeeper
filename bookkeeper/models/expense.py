# Описан класс, представляющий расходную операцию


from dataclasses import dataclass


@dataclass(slots=True)
class Expense:
    # Модель расходной операции.

    # Параметры модели:
    # amount - сумма операции;
    # category - id категории расходов;
    # added_date - дата добавления в бд;
    # comment - комментарий;
    # pk - id записи в базе данных.

    expense_date: str = ''
    added_date: str = ''
    category: int = 0
    amount: float = 0
    comment: str = ''
    pk: int = None
