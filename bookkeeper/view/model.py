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

    def countSpents(self, budget: Budget):
        con = sqlite3.connect(self.db_file)
        cursor = con.cursor()
        cursor.execute(f'SELECT SUM(amount) FROM {self.table_name} '
                       f'WHERE expense_date>{str(datetime.now() - budget.duration)[-8]}', )
        sum = cursor.fetchone()[0]
        con.commit()
        con.close()
        budget.moneyAmount = sum

    def add_category_with_name_id(self, name: str, parent_id: int, categories_list_repo: MemoryRepository,
                                  SQLRepoCategories: SQLiteRepository):
        try:
            categories_list_repo.add(Category(name, parent_id))  # зарегистрированный ранее обработчик
        except ValidationError as ex:
            QMessageBox.critical(self, 'Ошибка', str(ex))

        SQLRepoCategories.clear_update_from_list(categories_list_repo._container.values())

    def delete_category_with_id(self, delete_id: int, categories_list_repo: MemoryRepository,
                                SQLRepoCategories: SQLiteRepository):
        categories_list_repo.delete(delete_id)

        SQLRepoCategories.clear_update_from_list(categories_list_repo._container.values())
