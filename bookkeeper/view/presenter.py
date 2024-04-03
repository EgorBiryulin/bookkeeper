from typing import Callable

from bookkeeper.models.category import Category
from bookkeeper.view.view import View


class Bookkeeper():

    def __init__(self): #repository_factory):
        #self.category_repository = repository_factory.get(Category)
        #self.cats = self.category_repository.get_all()
        #self.view.set_category_list(self.cats)
        add_handler: Callable
        add_handler = self.add_category
        self.view = View(add_handler)

    def modify_cat(self, cat: Category) -> None:
        self.category_repository.update(cat)
        self.view.set_category_list(self.cats)

    def add_category(self):
        print("ПИВО ПИВО ПИВО ПИВО")
        #if name in [c.name for c in self.cats]:
        #    raise ValidationError(f'Категория {name} уже существует')

        #cat = Category(name, parent)
        #self.category_repository.add(cat)
        #self.cats.append(cat)
        #self.view.set_category_list(self.cats)


