from PySide6 import QtWidgets
from setuptools.config._validate_pyproject import ValidationError
from datetime import timedelta, datetime

from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.view.view import View
from bookkeeper.view.model import Model


class Bookkeeper:

    editable: bool

    def __init__(self, SQLRepoExpenses, SQLRepoCategories):

        # Репозиторий, хранящийся в памяти. Содержит список покупок
        self.SQLRepoCategories = SQLRepoCategories
        self.expense_list = MemoryRepository()
        self.expense_list.create_db_from_list(SQLRepoExpenses.get_all())

        # Репозиторий, хранящийся в памяти. Содержит список категорий
        self.SQLRepoExpenses = SQLRepoExpenses
        self.categories_list_repo = MemoryRepository()
        category_list = SQLRepoCategories.get_all()
        self.categories_list_repo.create_db_from_list(SQLRepoCategories.get_all())

        self.budget_list = [Budget(plan=1000, duration=timedelta(days=1)),
                            Budget(plan=1000, duration=timedelta(days=7)),
                            Budget(plan=1000, duration=timedelta(days=30))]

        self.view = View()
        self.model = Model()

        self.view.edit_process = False

        # Регистрация обработчиков команд
        self.view.register_budget_updater(self.update_budget_plan)
        self.view.register_expenses_adder(self.add_expense)
        self.view.register_category_deleter(self.delete_category)
        self.view.register_expenses_budget_modifier(self.delete_expense)
        self.view.register_category_adder(self.add_category)

        # Обновление таблицы покупок
        self.update_expenses()

        # Обновление таблицы бюджетных ограничений
        self.update_budget()

        # Обновление списка категорий
        self.view.update_category_combobox(self.model.get_category_list_names(category_list))

    def update_budget_plan(self) -> None:
        num = self.view.get_selected_budget()
        new_plan = int(self.view.get_new_budget_plan())
        self.budget_list[num].plan = new_plan
        self.update_budget()

    def update_budget(self) -> None:
        for i in range(0, len(self.budget_list)):
            money_spent = self.model.count_spents(self.budget_list[i], self.SQLRepoExpenses)
            if money_spent is None:
                money_spent = 0
            self.view.budget_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(money_spent)))
            self.view.budget_table.setItem(i, 1, QtWidgets.QTableWidgetItem(
                str(self.budget_list[i].plan)))

    def update_expenses(self) -> None:
        expenses = self.expense_list._container.values()
        for i in range(0, len(expenses)):
            obj = self.expense_list.get(i+1)
            obj_category = self.categories_list_repo.get(int(obj.category))
            obj_category = obj_category.name
            print(obj)
            self.view.expenses_table.setItem(i, 0, QtWidgets.QTableWidgetItem(obj.expense_date))
            self.view.expenses_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(obj.amount)))
            self.view.expenses_table.setItem(i, 2, QtWidgets.QTableWidgetItem(obj_category))
            self.view.expenses_table.setItem(i, 3, QtWidgets.QTableWidgetItem(obj.comment))

    def add_expense(self) -> None:
        new_expense_amount = float(self.view.expense_money_line.text())
        new_expense_comment = self.view.comment_line.text()
        new_expense_category = self.view.get_selected_category()
        new_expense_date = str(datetime.now())[:-7]
        new_expense = Expense(expense_date=new_expense_date, added_date=new_expense_date,
                              category=new_expense_category, amount=new_expense_amount,
                              comment=new_expense_comment)
        self.expense_list.add(new_expense)
        setattr(new_expense, 'pk', None)
        self.SQLRepoExpenses.add(new_expense)

        self.update_expenses()
        self.update_budget()

    def delete_category(self) -> None:
        # получение данных из формочки
        delete_id = self.view.get_selected_category()

        # Запуск процесса удаления
        self.model.delete_category_with_id(delete_id, self.categories_list_repo, self.SQLRepoCategories)

        # Обновление формочки
        category_list = list(self.categories_list_repo._container.values())
        category_list_names = self.model.get_category_list_names(category_list)
        self.view.update_category_combobox(category_list_names)

        self.update_expenses()

    def delete_expense(self) -> None:
        print("Все, запомнил, отвали")
        # self.category_repository.update(cat)
        # self.view.set_category_list(self.cats)

    def add_category(self) -> None:
        # получение данных из формочки
        parent_id = None
        if self.view.get_selected_category() != 0:
            parent_id = self.view.get_selected_category()
        name = self.view.get_new_category_name()

        # Проверка существования категории
        category_list = list(self.categories_list_repo._container.values())
        existing_category_names = self.model.get_category_list_names(category_list)
        for existing_name in existing_category_names:
            if name == existing_name:
                raise ValidationError(f'Категория {name} уже существует')

        # Запуск процесса добавления
        self.model.add_category_with_name_id(name, parent_id, self.categories_list_repo, self.SQLRepoCategories)

        # Обновление формочки
        category_list = list(self.categories_list_repo._container.values())
        category_list_names = self.model.get_category_list_names(category_list)
        self.view.update_category_combobox(category_list_names)
