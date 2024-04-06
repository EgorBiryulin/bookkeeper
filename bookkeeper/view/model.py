import sqlite3
from datetime import datetime
from PySide6 import QtWidgets
from PySide6.QtWidgets import QMessageBox
from setuptools.config._validate_pyproject import ValidationError

from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository

class Model:

    def get_category_list_names(self, category_list: [Category]) -> []:
        names_list = []
        for i in range(len(category_list)):
            if hasattr(category_list[i], 'name'):
                names_list.append(getattr(category_list[i], 'name'))
            else:
                raise ValueError(f'trying to add object {category_list[i]} without `name` attribute')
        return names_list

    def set_table_data(self, data: []) -> None:
        for i, row in enumerate(data):
            for j, x in enumerate(row):
                self.setItem(
                    i, j,
                    QtWidgets.QTableWidgetItem(x.capitalize())
                )

    def add_category_with_name_id(self, name: str, parent_id: int, categories_list_repo: MemoryRepository,
                                  sql_repo: SQLiteRepository):
        # Добавление категории
        try:
            categories_list_repo.add(Category(name, parent_id))
        except ValidationError as ex:
            QMessageBox.critical(self, 'Ошибка', str(ex))

        # Обновление формочки
        sql_repo.clear_update_from_list(categories_list_repo._container.values())

    def delete_category_with_id(self, delete_id: int, categories_list_repo: MemoryRepository,
                                sql_repo: SQLiteRepository):
        # Удаляет категорию по ID. Присваивает детям удаляемой категории ее родителя
        delete_obj = categories_list_repo.get(delete_id)
        delete_obj_parent = delete_obj.parent
        delete_obj_pk = delete_obj.pk

        # Поиск и обновление родителей категорий
        update_cat = categories_list_repo.get_all({"parent": delete_obj_pk})
        for obj in update_cat:
            setattr(obj, 'parent', delete_obj_parent)
            categories_list_repo.update(obj)
            sql_repo.update(obj)

        # Удаление категории из репозиториев
        categories_list_repo.delete(delete_id)
        sql_repo.delete(delete_id)

    def countSpents(self, budget: Budget):
        con = sqlite3.connect(self.db_file)
        cursor = con.cursor()
        cursor.execute(f'SELECT SUM(amount) FROM {self.table_name} '
                       f'WHERE expense_date>{str(datetime.now() - budget.duration)[-8]}', )
        sum = cursor.fetchone()[0]
        con.commit()
        con.close()
        budget.moneyAmount = sum


