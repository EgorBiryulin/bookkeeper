from bookkeeper.view.view import View


class Bookkeeper:

    def __init__(self):  # repository_factory):
        # self.category_repository = repository_factory.get(Category)
        # self.cats = self.category_repository.get_all()
        # self.view.set_category_list(self.cats)

        self.view = View()
        self.view.register_expenses_budget_modifier(self.modify_expenses_budget_list)
        self.view.register_expenses_adder(self.add_expense)
        self.view.register_category_deleter(self.delete_category)
        self.view.register_category_adder(self.add_category)

    def modify_expenses_budget_list(self) -> None:
        print("Ну давай, модифицируй покупки")
        # self.category_repository.update(cat)
        # self.view.set_category_list(self.cats)

    def add_expense(self) -> None:
        print("Я купил Пива")
        # if name in [c.name for c in self.cats]:
        #    raise ValidationError(f'Категория {name} уже существует')

        # cat = Category(name, parent)
        # self.category_repository.add(cat)
        # self.cats.append(cat)
        # self.view.set_category_list(self.cats)

    def delete_category(self) -> None:
        print("Я удалил категорию Пиво(")
        # if name in [c.name for c in self.cats]:
        #    raise ValidationError(f'Категория {name} уже существует')

        # cat = Category(name, parent)
        # self.category_repository.add(cat)
        # self.cats.append(cat)
        # self.view.set_category_list(self.cats)

    def add_category(self) -> None:
        print("Я добавил категорию Пиво")
        # if name in [c.name for c in self.cats]:
        #    raise ValidationError(f'Категория {name} уже существует')

        # cat = Category(name, parent)
        # self.category_repository.add(cat)
        # self.cats.append(cat)
        # self.view.set_category_list(self.cats)
