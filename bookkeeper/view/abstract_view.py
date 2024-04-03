from typing import Protocol, Callable

from bookkeeper.models.category import Category

class AbstractView(Protocol):

    def set_category_list(self, handler: [Category]) -> None:
        pass

    def register_cat_modifier(self, widget, handler: Callable[[Category], None]):
        pass

    def register_cat_adder(self, widget, handler: Callable[[Category], None]):
        pass

    def register_cat_deleter(self, widget, handler: Callable[[Category], None]):
        pass
