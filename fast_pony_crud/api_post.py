from pony.orm import db_session

@db_session
def api_post(table,kwargs:dict):
    """rest api post method
    Args:
        kwargs (dict): dictionary containing pkey/column values
    Returns:
        int: status code 
    """        
    kwargs = kwargs.dict()
    entity_pkey_names = [pkey.name for pkey in table._pk_attrs_]
    non_auto_pkeys = [pkey.name for pkey in table._pk_attrs_ if pkey.auto==False]
    entry_col_names = non_auto_pkeys + [col for col in table._columns_ if col not in entity_pkey_names]
    entry_kwargs = {col_name:kwargs.get(col_name) for col_name in entry_col_names if col_name in kwargs.keys() and kwargs.get(col_name) is not None}
    new_entry = table(**entry_kwargs)
    table._database_.commit()
    return new_entry.to_dict()