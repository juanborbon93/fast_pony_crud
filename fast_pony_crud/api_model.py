from pony.orm.core import Set as PonySet
from pony.orm import *
from pydantic import create_model
from typing import List,Dict
from uuid import uuid4

def get_api_type(table,col,make_optional=False,prefix:str=""):
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
            return get_api_type(col.py_type,col.py_type._pk_attrs_[0],make_optional=not col.is_required)
        else:
            t =  get_api_model(col.py_type,"GET",name_prefix=f"{table.__name__}_") 
    if col.is_required and make_optional==False:
        return (t,...)
    else:
        return (t,None)

def get_api_model(table,model_type:str,name_prefix:str=""):
    """ 
    Returns:
        [dict]: model to be used in the restplus api for the crud routes
    """        
    pkey_attr_names = [pkey.name for pkey in table._pk_attrs_]
    non_auto_pkey_names = [pkey.name for pkey in table._pk_attrs_ if pkey.auto==False and pkey.default is None]
    non_pkey_col_names = [col for col in table._adict_ if col not in pkey_attr_names]
    post_model_keys = non_auto_pkey_names + non_pkey_col_names
    model = None
    if model_type == "GET" or model_type == "DELETE":
        model = create_model(
            str(uuid4().hex),
            **{pkey.name:get_api_type(table,pkey) for pkey in table._pk_attrs_ if get_api_type(table,pkey) is not None})
    elif model_type == "PUT":
        model = create_model(
            str(uuid4().hex),
            **{col_name:get_api_type(table,table._adict_.get(col_name),make_optional=True) for col_name in non_pkey_col_names if get_api_type(table,table._adict_.get(col_name)) is not None})
    elif model_type == "POST":
        model = create_model(
            str(uuid4().hex),
            **{col_name:get_api_type(table,table._adict_.get(col_name)) for col_name in post_model_keys if get_api_type(table,table._adict_.get(col_name)) is not None})
    elif model_type == "RESPONSE":
        model_entry = create_model(
            str(uuid4().hex),
            **{col_name:get_api_type(table,col) for col_name,col in table._adict_.items() if get_api_type(table,col) is not None})
        model = List[model_entry]
    return model
