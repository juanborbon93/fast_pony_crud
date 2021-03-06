from .table_crud import create_table_crud
def create_crud_routes(db,app,prefix="/db",api_key:str=None):
    for table in db.entities.values():
        create_table_crud(table,app,prefix,api_key)