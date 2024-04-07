import sqlite3
from datetime import datetime
from PySide6.QtWidgets import QMessageBox
from setuptools.config._validate_pyproject import ValidationError

from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository


class Model:

    def get_category_list_names(self, category_list: [Category]) -> []:
        # Возвращает список имен категорий
        names_list = []
        for i in range(len(category_list)):
            if hasattr(category_list[i], 'name'):
                names_list.append(getattr(category_list[i], 'name'))
            else:
                raise ValueError(f'trying to add object {category_list[i]} without `name` attribute')
        return names_list

    def add_category_with_name_id(self, name: str, parent_id: int, categories_list_repo: MemoryRepository,
                                  sql_repo: SQLiteRepository):
        # Добавление категории
        try:
            categories_list_repo.add(Category(name, parent_id))
            sql_repo.add(Category(name, parent_id))
        except ValidationError as ex:
            QMessageBox.critical(QMessageBox(), 'Ошибка', str(ex))

        # Обновление формочки
        # sql_repo.clear_update_from_list(categories_list_repo._container.values())

    def delete_category_with_id(self, delete_id: int, categories_list_repo: MemoryRepository,
                                categories_sql_repo: SQLiteRepository, expenses_list_repo: MemoryRepository,
                                expenses_sql_repo: SQLiteRepository):
        # Удаляет категорию по ID. Присваивает детям удаляемой категории ее родителя
        delete_obj = categories_list_repo.get(delete_id)
        delete_obj_parent_pk = delete_obj.parent
        delete_obj_pk = delete_obj.pk

        # Удаление категории из репозиториев
        categories_list_repo.delete(delete_id)
        categories_sql_repo.delete(delete_id)

        category_objects = categories_list_repo.get_all()
        expense_objects = expenses_list_repo.get_all()

        # Обновление списка категорий
        for obj in category_objects:
            if obj.parent is not None:
                if int(obj.parent) == int(delete_obj_pk):
                    setattr(obj, 'parent', delete_obj_parent_pk)
                elif int(obj.parent) > int(delete_obj_pk):
                    setattr(obj, 'parent', int(obj.parent)-1)
                categories_list_repo.update(obj)
                categories_sql_repo.update(obj)

        # Обновление списка покупок
        for obj in expense_objects:
            if obj.category is not None:
                if int(obj.category) == int(delete_obj_pk):
                    setattr(obj, 'category', delete_obj_parent_pk)
                elif int(obj.category) > int(delete_obj_pk):
                    setattr(obj, 'category', int(obj.category)-1)
                expenses_list_repo.update(obj)
                expenses_sql_repo.update(obj)

        # Удаление из списка категорий при удалении Базовой категории
        for obj in expense_objects:
            if delete_obj_parent_pk is None:
                if obj.category is None:
                    expenses_list_repo.delete(obj.pk)
                    expenses_sql_repo.delete(obj.pk)

    def count_spents(self, budget: Budget, sql_db: SQLiteRepository) -> float:
        with sqlite3.connect(sql_db.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(f'SELECT SUM(amount) FROM {sql_db.table_name} '
                        f'WHERE expense_date>"{str(datetime.now() - budget.duration)[:-7]}"', )
            summ = cur.fetchone()[0]
            con.commit()
        con.close()
        return summ
