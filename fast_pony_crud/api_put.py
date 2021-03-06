from pony.orm import db_session

@db_session
def api_put(table,new_data:dict,entity_pkeys:dict):
    """rest api put method for updating an existing entry
    Args:
        kwargs (dict): dictionary containing pkey/column values
    Returns:
        int: status code 
    """        
    entity_pkey_names = [pkey.name for pkey in table._pk_attrs_]
    # entry_kwargs = {pkey:kwargs[pkey] for pkey in entity_pkey_names}
    db_entry  = table.get(**entity_pkeys)
    for col_name,col_val in new_data.items():
        if col_name not in entity_pkey_names and col_name in table._columns_:
            if col_val is not None:
                setattr(db_entry,col_name,col_val)
    table._database_.commit()
    return 200