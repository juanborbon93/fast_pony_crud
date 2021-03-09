from .api_type import get_api_type
from pydantic import create_model
from typing import List
def get_api_model(table,model_type:str):
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
            f'{table.__name__}_get',
            **{pkey.name:get_api_type(table,pkey) for pkey in table._pk_attrs_ if get_api_type(table,pkey) is not None})
    elif model_type == "PUT":
        model = create_model(
            f'{table.__name__}_put',
            **{col_name:get_api_type(table,table._adict_.get(col_name),make_optional=True) for col_name in non_pkey_col_names if get_api_type(table,table._adict_.get(col_name)) is not None})
    elif model_type == "POST":
        model = create_model(
            f'{table.__name__}_post',
            **{col_name:get_api_type(table,table._adict_.get(col_name)) for col_name in post_model_keys if get_api_type(table,table._adict_.get(col_name)) is not None})
    elif model_type == "RESPONSE":
        model_entry = create_model(
            f'{table.__name__}_response',
            **{col_name:get_api_type(table,col) for col_name,col in table._adict_.items() if get_api_type(table,col) is not None})
        model = List[model_entry]
    return model
