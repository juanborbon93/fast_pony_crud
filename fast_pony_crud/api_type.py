from pony.orm.core import Set as PonySet
from pony.orm import *
from typing import Dict
def get_api_type(table,col,make_optional=False):
    """
    Args:
        t ([type]): Pony table attribute object
    Returns:
        [GenericMeta]: Pydantic.GenericMeta type used for route data marshalling
    """
    conversion_map = {
        ormtypes.Json:Dict
    }
    if type(col) is PonySet:
        return None
    t =  col.py_type
    if col.py_type in conversion_map:
        t =  conversion_map[col.py_type]
    if col.py_type in table._database_.entities.values():
        if len(col.py_type._pk_attrs_)==1:
            return get_api_type(col.py_type,col.py_type._pk_attrs_[0],make_optional=make_optional)
        else:
            t =  col.py_type.get_model("GET") 
    if col.is_required and make_optional==False:
        return (t,...)
    else:
        return (t,None)