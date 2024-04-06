from setuptools.config._validate_pyproject import ValidationError

from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.view.view import View
from bookkeeper.view.model import Model


class Bookkeeper:

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

        self.view = View()
        self.model = Model()

        # Регистрация обработчиков команд
        self.view.register_expenses_budget_modifier(self.modify_expenses_budget_list)
        self.view.register_expenses_adder(self.add_expense)
        self.view.register_category_deleter(self.delete_category)
        self.view.register_category_adder(self.add_category)

        # Обновление таблицы покупок

        # Обновление таблицы бюджетных ограничений

        # Обновление списка категорий
        self.view.update_category_combobox(self.model.get_category_list_names(category_list))

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

    def delete_category(self) -> None:
        # получение данных из формочки
        delete_id = self.view.get_selected_category()

        # Запуск процесса удаления
        self.model.delete_category_with_id(delete_id, self.categories_list_repo, self.SQLRepoCategories)

        # Обновление формочки
        category_list = list(self.categories_list_repo._container.values())
        category_list_names = self.model.get_category_list_names(category_list)
        self.view.update_category_combobox(category_list_names)

    def modify_expenses_budget_list(self) -> None:
        print("Ну давай, модифицируй покупки")
        # self.category_repository.update(cat)
        # self.view.set_category_list(self.cats)

    def add_expense(self) -> None:
        print("Я купил Пива")
        #if name == "Пиво": # Пасхалка)
        #    print("Ура, я добавил Пиво в категории!!!")
        # if name in [c.name for c in self.cats]:
        #    raise ValidationError(f'Категория {name} уже существует')

        # cat = Category(name, parent)
        # self.category_repository.add(cat)
        # self.cats.append(cat)
        # self.view.set_category_list(self.cats)

