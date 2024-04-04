# Модуль описывает репозиторий, работающий в оперативной памяти

from itertools import count
from typing import Any

from bookkeeper.repository.abstract_repository import AbstractRepository, T


class MemoryRepository(AbstractRepository[T]):

    # Репозиторий, работающий в оперативной памяти. Хранит данные в виде словаря
    # Параметры функций описаны в abstract_repository.py

    def __init__(self) -> None:
        self._container: dict[int, T] = {}
        self._counter = count(1)

    def add(self, obj: T) -> int:
        # Метод добавляет элемент в конец БД
        # if getattr(obj, 'pk') != -1:
        if hasattr(obj, 'pk'):
            pass
        else:
            raise ValueError(f'trying to add object {obj} without `pk` attribute')
        if getattr(obj, 'pk') is not None:
            raise ValueError(f'trying to add object with filled `pk` attribute')
        pk = next(self._counter)
        self._container[pk] = obj
        if hasattr(obj, 'pk'):
            obj.pk = pk
        return pk

    def create_db_from_list(self, obj_list: [T]):
        # Метод метод создает БД из набора элементов
        for i in range(len(obj_list)):
            obj = obj_list[i]
            if hasattr(obj, 'pk'):
                setattr(obj, 'pk', None)
            self.add(obj)

    def get(self, pk: int) -> T | None:
        # Метод Возвращает элемент из БД с индексом pk
        return self._container.get(pk)

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        # Метод возвращает все элементы из БД
        if where is None:
            return list(self._container.values())
        return [obj for obj in self._container.values()
                if all(getattr(obj, attr) == value for attr, value in where.items())]

    def update(self, obj: T) -> None:
        # Метод обновляет выбранный элемент в БД (по индексу)
        if hasattr(obj, 'pk'):
            pass
        else:
            raise ValueError(f'trying to update object without `pk` attribute')
        if getattr(obj, 'pk') is None:
            raise ValueError('attempt to update object with unknown primary key')
        self._container[obj.pk] = obj

    def delete(self, pk: int) -> None:
        # Метод удаляет выбранный элемент в БД (по индексу)
        self._container.pop(pk)
