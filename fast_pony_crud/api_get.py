from pony.orm import db_session
from uuid import UUID

@db_session
def api_get(table,kwargs:dict):
    """rest api get method
    Args:
        kwargs (dict): dictionary with {pkey:value} pairs
    Returns:
        list,int : list of entries matching query, status code
    """        
    sql = f"SELECT * FROM {table._table_}"
    first_condition = True
    k = {}
    for key,val in kwargs.items():
        if val is not None and key!="_api_key":
            if type(val)==str:
                query_val = val
            elif type(val) == UUID:
                query_val = val.bytes
            else:
                query_val = str(val)
            k[key]=query_val
            if first_condition == True:
                sql += f' WHERE {key}=${key}'
                first_condition = False
            else:
                sql += f' AND {key}=${key}'
    entries = table.select_by_sql(sql,k)
    return_entries = [entry.to_dict() for entry in entries]
    return return_entries