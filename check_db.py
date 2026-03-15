from app import create_app
from app.extensions import db
from sqlalchemy import inspect

app = create_app()
with app.app_context():
    tables = inspect(db.engine).get_table_names()
    print(f"Tables: {tables}")
