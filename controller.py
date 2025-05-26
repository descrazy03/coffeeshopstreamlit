import sqlite3
import pandas as pd
from uuid import uuid4
from database.models import RecipeBase, CoffeeBase, CafeBase
from datetime import datetime

import sqlite3
import pandas as pd
from uuid import uuid4
from database.models import RecipeBase, CoffeeBase, CafeBase
from datetime import datetime

'''
define basic CRUD methods for each database model
'''

DATABASE_PATH = "mnts/coffeeproto_v1.db"

class Controller:

    def __init__(self, table):
        self.table = table

    # database connection for methods that alter database
    def db_conn(self, stmt: str):
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute(stmt)
        conn.commit()
        conn.close()

    # POST new row to table
    def post(self, data: RecipeBase | CoffeeBase | CafeBase):
        to_post = data.model_dump()
        id = str(uuid4())
        to_post['id'] = id
        post_values = tuple(to_post.values())
        stmt = f"INSERT INTO {self.table} VALUES {post_values}"
        self.db_conn(stmt)

    # GET all rows from table
    def get_all(self):
        entries = pd.read_sql(f"SELECT * FROM {self.table}", f"sqlite:///{DATABASE_PATH}")
        return entries

    # GET one row from table
    def get_one(self, id):
        entry = pd.read_sql(f"SELECT * FROM {self.table} WHERE id = '{id}'", f"sqlite:///{DATABASE_PATH}")
        return entry

    # UPDATE one row from table
    def update(self, updates: RecipeBase | CoffeeBase | CafeBase, id):
        # determine which table to use and get original row
        if self.table == "coffees":
            og_data = CoffeeBase(**self.get_one(id).iloc[0])
        elif self.table == "recipes":
            og_data = RecipeBase(**self.get_one(id).iloc[0])
        elif self.table == "cafes":
            og_data = CafeBase(**self.get_one(id).iloc[0])
        
        # create row from updated row from input
        new_data = og_data.model_copy(update=updates.model_dump(exclude_unset=True))
        new_vals = tuple(new_data.model_dump().values())

        # create SQL statment 
        cols = self.get_all().columns.to_list()
        to_insert = map(lambda col: f"{col[1]} = '{new_vals[col[0]]}'" if type(new_vals[col[0]]) is str else f"{col[1]} = {new_vals[col[0]]}", enumerate(cols))
        stmt = f"UPDATE {self.table} SET " + ', '.join(to_insert) + f" WHERE id = '{id}'"
        self.db_conn(stmt)

    # DELETE one row from table
    def delete(self, id):
        stmt = f"DELETE FROM {self.table} WHERE id = '{id}'"
        self.db_conn(stmt)

if __name__ == '__main__':
    pass