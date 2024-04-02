from PySide6 import QtWidgets


def countSpents(self, budget: Budget):
    con = sqlite3.connect(self.db_file)
    cursor = con.cursor()
    cursor.execute(
        f'SELECT SUM(amount) FROM {self.table_name} WHERE expense_date>{str(datetime.now() - budget.duration)[-8]}', )
    sum = cursor.fetchone()[0]
    con.commit()
    con.close()
    budget.moneyAmount = sum


def set_table_data(self, data: []) -> None:
    for i, row in enumerate(data):
        for j, x in enumerate(row):
            self.setItem(
                i, j,
                QtWidgets.QTableWidgetItem(x.capitalize())
            )

