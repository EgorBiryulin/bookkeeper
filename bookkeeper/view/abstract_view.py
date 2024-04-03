from typing import Protocol, Callable

from bookkeeper.models.category import Category


class AbstractView(Protocol):

    def set_category_list(self, handler: [Category]) -> None:
        # Метод создает список категорий из БД и добавляет его в GUI
        pass

    def register_expenses_budget_modifier(self, handler: Callable) -> None:
        # Метод регистрирует обработчик команды кнопки на начало
        # модификации списка расходов и бюджетных ограничений
        pass

    def register_expenses_adder(self, handler: Callable) -> None:
        # Метод регистрирует обработчик команды кнопки, добавляющей расходную операцию
        pass

    def register_category_deleter(self, handler: Callable) -> None:
        # Метод регистрирует обработчик команды кнопки, удаляющей категорию
        pass

    def register_category_adder(self, handler: Callable) -> None:
        # Метод регистрирует обработчик команды кнопки, добавляющий категорию
        pass
