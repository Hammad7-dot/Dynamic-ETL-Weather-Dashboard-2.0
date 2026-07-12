from sqlalchemy import inspect

from database.database import engine

inspector = inspect(engine)
print(inspector.get_table_names())
