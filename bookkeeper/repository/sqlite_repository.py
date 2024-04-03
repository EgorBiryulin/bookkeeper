# Модуль описывает репозиторий, работающий в sqlite

import sqlite3

from inspect import get_annotations
from typing import Any

from bookkeeper.repository.abstract_repository import AbstractRepository, T


class SQLiteRepository(AbstractRepository[T]):

    # Репозиторий, работающий в работающий с sqlite. Хранит данные в формате ".db"
    # Параметры функций описаны в abstract_repository.py

    def __init__(self, db_file: str, cls: type) -> None:
        # Инициализация БД
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        if self.fields.__contains__('pk'):
            self.fields.pop('pk')
        self.cls_type: T = cls

    def add(self, obj: T) -> int:
        # Метод добавляет элемент в конец БД
        if hasattr(obj, 'pk'):
            pass
        else:
            raise ValueError(f'trying to add object {obj} without `pk` attribute')
        if getattr(obj, 'pk') is not None:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')
        names = ', '.join(self.fields.keys())
        p = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'INSERT INTO {self.table_name} ({names}) VALUES ({p})',
                values
            )
            obj.pk = cur.lastrowid
        con.commit()
        con.close()
        return obj.pk

    def get(self, pk: int) -> T | None:
        # Метод Возвращает элемент из БД, находящийся в строке pk
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(f'SELECT * FROM {self.table_name} 'f'WHERE rowid = ?', (pk,))
            result = cur.fetchone()
        con.commit()
        con.close()

        if result:
            result_obj: any = self.cls_type()
            setattr(result_obj, 'pk', pk)
            keys = list(self.fields.keys())
            for i in range(len(keys)):
                setattr(result_obj, keys[i], result[i])
            return result_obj
        else:
            return None

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        # Метод возвращает все элементы из БД
        result = list()
        if where is None:
            with sqlite3.connect(self.db_file) as con:
                cur = con.cursor()
                cur.execute('PRAGMA foreign_keys = ON')
                cur.execute(f'SELECT COUNT(*) FROM {self.table_name}')
                size = cur.fetchone()[0]
            con.commit()
            con.close()
            if size > 0:
                for i in range(size):
                    result.append(self.get(i+1))
            return result

        for attr, value in where.items():
            with sqlite3.connect(self.db_file) as con:
                cur = con.cursor()
                cur.execute('PRAGMA foreign_keys = ON')
                cur.execute(f'SELECT ROWID FROM {self.table_name} WHERE {attr} = ?', (value,))
                rowids = cur.fetchall()
                print(rowids)
                for rowid in rowids:
                    result.append(self.get(rowid[0]))
            con.commit()
            con.close()
        return result

    def update(self, obj: T) -> None:
        # Метод обновляет выбранный элемент в БД
        if hasattr(obj, 'pk'):
            pass
        else:
            raise ValueError(f'trying to update object {obj} without `pk` attribute')
        if obj.pk == 0:
            raise ValueError('attempt to update object with unknown primary key')
        keys = list(self.fields.keys())
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            set_clause = ', '.join(f'{key} = ?' for key in keys)
            set_values = tuple(values + [obj.pk])  # Добавляем pk в конец кортежа
            cur.execute(f'UPDATE {self.table_name} SET {set_clause} WHERE rowid = ?', set_values)

        con.commit()
        con.close()

    def delete(self, pk: int) -> None:
        # Метод удаляет выбранный элемент в БД
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(f'SELECT COUNT(*) FROM {self.table_name} WHERE rowid = ?', (pk,))
            result = cur.fetchone()[0]
            if result > 0:
                cur.execute(f'DELETE FROM {self.table_name} '
                            f'WHERE rowid = ?', (pk,))
            else:
                raise KeyError(f'trying to delete object that does not exist')
        con.commit()
        con.close()
