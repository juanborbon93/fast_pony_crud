from pony.orm import db_session

@db_session
def api_delete(table,entry_kwargs:dict):
    """rest api delete method
    Args:
        kwargs (dict): dictionary containing pkey values
    Returns:
        int: status code 
    """    
    entry_kwargs = {key:val for key,val in entry_kwargs.items() if key!="_api_key"}
    db_entry  = table.get(**entry_kwargs)
    if db_entry is None:
        return 404
    db_entry.delete()
    table._database_.commit()
    return 200