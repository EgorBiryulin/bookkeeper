# Описан класс, представляющий категорию расходов

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterator

from ..repository.abstract_repository import AbstractRepository


@dataclass
class Category:

    # Модель категории расходов.

    # Параметры модели:
    # name - название категории расходов;
    # parent - ссылку на родителя (id родителя), у категорий верхнего уровня parent = None;
    # pk - идентификатор категории.

    name: str = ""
    parent: int = None
    pk: int = None

    def get_parent(self, repo: AbstractRepository['Category']) -> 'Category | None':
        # Метод находит и возвращает родительскую категорию в виде объекта Category.
        # Если метод вызван у категории верхнего уровня, возвращает None.

        # Параметры:
        # repo - репозиторий для получения объектов.

        # Возвращает объект класса Category или None.

        if self.parent is None:
            return None
        return repo.get(self.parent)

    def get_all_parents(self, repo: AbstractRepository['Category']) -> Iterator['Category']:
        # Метод получает и возвращает все категории верхнего уровня в иерархии.

        # Параметры:
        # repo - репозиторий для получения объектов.

        # Возвращает (Yields) объекты класса Category от родителя и выше до категории верхнего уровня.

        parent = self.get_parent(repo)
        if parent is None:
            return
        yield parent
        yield from parent.get_all_parents(repo)

    def get_subcategories(self, repo: AbstractRepository['Category']) -> Iterator['Category']:
        # Метод получает и возвращает все подкатегории из иерархии,
        # т.е. непосредственные подкатегории данной, все их подкатегории и т.д.

        # Параметры:
        # repo - репозиторий для получения объектов.

        # Возвращает объект класса Category, являющиеся подкатегориями разного уровня ниже данной.

        def get_children(graph: dict[int | None, list['Category']],
                         root: int) -> Iterator['Category']:
            """ dfs in graph from root """
            for x in graph[root]:
                yield x
                yield from get_children(graph, x.pk)

        subcats = defaultdict(list)
        for cat in repo.get_all():
            subcats[cat.parent].append(cat)
        return get_children(subcats, self.pk)

    @classmethod
    def create_from_tree(cls, tree: list[tuple[str, str | None]],
                         repo: AbstractRepository['Category']) -> list['Category']:
        # Создать дерево категорий из списка пар "потомок-родитель".
        # Список должен быть топологически отсортирован, т.е. потомки
        # не должны встречаться раньше своего родителя.
        # Проверка корректности исходных данных не производится.
        # При использовании СУБД с проверкой внешних ключей, будет получена
        # ошибка (для sqlite3 - IntegrityError). При отсутствии проверки
        # со стороны СУБД, результат, возможно, будет корректным, если исходные
        # данные корректны за исключением сортировки. Если нет, то нет.

        # Параметры:
        # tree - список пар "потомок-родитель"
        # repo - репозиторий для получения объектов.

        # Список созданных объектов Category

        created: dict[str, Category] = {}
        for child, parent in tree:
            cat = cls(child, created[parent].pk if parent is not None else None)
            repo.add(cat)
            created[child] = cat
        return list(created.values())
