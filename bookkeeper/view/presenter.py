from collections.abc import Callable
from typing import Protocol

from setuptools.config._validate_pyproject import ValidationError
from bookkeeper.models.category import Category


class AbstractView(Protocol):

    @Protocol
    def set_category_list(list[Category]) -> None:
        pass

    @Protocol
    def register_cat_modifier(handler: Callable[[Category], None]):
        pass

    @Protocol
    def register_cat_adder(handler: Callable[[Category], None]):
        pass

    @Protocol
    def register_cat_deleter(handler: Callable[[Category], None]):
        pass


class Bookkeeper:

    def __init__(self, view: AbstractView, repository_factory):
        self.view = view
        self.category_repository = repository_factory.get(Category)
        self.cats = self.category_repository.get_all()
        self.view.set_category_list(self.cats)
        self.view.register_cat_modifier(self.modify_cat)


        def modify_cat(self, cat: Category) -> None:
            self.category_repository.update(cat)
            self.view.set_category_list(self.cats)

        def add_category(self, name, parent):
            if name in [c.name for c in self.cats]:
                raise ValidationError(
                    f'Категория {name} уже существует')

            cat = Category(name, parent)
            self.category_repository.add(cat)
            self.cats.append(cat)
            self.view.set_category_list(self.cats)


