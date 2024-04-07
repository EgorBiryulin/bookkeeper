from typing import Protocol, Callable

from bookkeeper.models.category import Category


class AbstractView(Protocol):

    def register_budget_updater(self, handler):
        # Метод регистрирует обработчик команды кнопки, обновляющей бюджет
        pass

    def register_expenses_adder(self, handler):
        # Метод регистрирует обработчик команды кнопки, добавляющей расходную операцию
        pass

    def register_category_deleter(self, handler):
        # Метод регистрирует обработчик команды кнопки, удаляющей категорию
        pass

    def register_expenses_deleter(self, handler):
        # Метод регистрирует обработчик команды кнопки, удаляющей расходную операцию
        pass

    def register_category_adder(self, handler):
        # Метод регистрирует обработчик команды кнопки, добавляющий категорию
        pass
