# Модуль содержит описание абстрактного репозитория

# Репозиторий реализует хранение объектов, присваивая каждому объекту уникальный
# идентификатор в атрибуте pk (primary key). Объекты, которые могут быть сохранены
# в репозитории, должны поддерживать добавление атрибута pk и не должны
# использовать его для иных целей.

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Protocol, Any


class Model(Protocol):

    # Модель элемента БД должна содержать атрибут pk.

    pk: int


T = TypeVar('T', bound=Model)


class AbstractRepository(ABC, Generic[T]):

    # Абстрактный репозиторий содержит следующие абстрактные методы:
    # add, get, get_all, update, delete.

    @abstractmethod
    def add(self, obj: T) -> int:
        # Метод добавляет объект в репозиторий
        # и записывает id в атрибут pk.
        # Возвращает id объекта.
        pass

    @abstractmethod
    def get(self, pk: int) -> T | None:
        # Возвращает элемент БД по id.
        pass

    @abstractmethod
    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        # Получает и возвращает все записи в БД по некоторому условию:
        # where - условие в виде словаря {'название_поля': значение}.
        # Если условие не задано (по умолчанию), возвращает все записи.
        pass

    @abstractmethod
    def update(self, obj: T) -> None:
        # Обновить данные об объекте. Объект должен содержать поле pk.
        pass

    @abstractmethod
    def delete(self, pk: int) -> None:
        # Удаляет объект из БД по индексу pk.
        pass
