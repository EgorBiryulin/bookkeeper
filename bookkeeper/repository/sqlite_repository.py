"""
Модуль описывает репозиторий, работающий в SQLite
"""
from inspect import get_annotations
from typing import Any
from datetime import datetime
import sqlite3

from bookkeeper.repository.abstract_repository import AbstractRepository, T
from bookkeeper.models.budget import Budget


class SQLiteRepository(AbstractRepository[T]):
    """
    Репозиторий, работающий в работающий в SQLite
    """

    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        #self.fields.pop('pk')
        self.cls_type: T = cls

    def add(self, obj: T) -> int:
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object with filled `pk` attribute')
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
            cur.execute(f'UPDATE {self.table_name} SET pk = ? WHERE pk = ?',
                        [obj.pk, 0]
                        )
        con.commit()
        con.close()
        # return obj.pk

    def get(self, pk: int) -> T | None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(f'SELECT * FROM {self.table_name} WHERE rowid = ?', (pk,))
            result = cur.fetchone()
        con.commit()
        con.close()

        if result:
            result_obj: any = self.cls_type
            keys = list(self.fields.keys())
            for i in range(len(keys)):
                setattr(result_obj, keys[i], result[i])
            try:
                setattr(result_obj, 'pk', pk)
            except:
                pass
            return result_obj
        else:
            return None

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
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
                    result.append(self.get(i + 1))
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

    def countSpents(self, budget: Budget):
        con = sqlite3.connect(self.db_file)
        cursor = con.cursor()
        cursor.execute(
            f'SELECT SUM(amount) FROM {self.table_name} WHERE expense_date>{str(datetime.now() - budget.duration)[-8]}', )
        sum = cursor.fetchone()[0]
        con.commit()
        con.close()
        budget.moneyAmount = sum
