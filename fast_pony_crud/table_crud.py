from .api_get import api_get
from .api_delete import api_delete
from .api_post import api_post
from .api_put import api_put
from .api_model import get_api_model
from .api_model import get_api_model
from fastapi import APIRouter,Depends
from pony.orm import *
from uuid import UUID
from datetime import datetime
from inspect import signature,Parameter
from .security import get_api_key,APIKey
import os

def create_table_crud(table,app,prefix:str="/db",api_key:str=None):
    if api_key:
        os.environ['API_CRUD_KEY']=api_key
    router = APIRouter()
    pkey_attr_names = [pkey.name for pkey in table._pk_attrs_]
    path_args = [f'{{{pk}}}' for pk in pkey_attr_names]
    get_query_params = []
    api_get_params = []
    security_parameter = Parameter('api_key',kind=Parameter.POSITIONAL_OR_KEYWORD,annotation=APIKey,default=Depends(get_api_key))
    for col in table._columns_:
        arg_type = table._adict_.get(col).py_type
        if arg_type not in  [dict,ormtypes.Json]:
            if arg_type not in [int,bool,float,UUID,datetime]:
                arg_type=str
            param = Parameter(col,kind=Parameter.POSITIONAL_OR_KEYWORD,annotation=arg_type,default=None)
            get_query_params.append(param)
            if col in pkey_attr_names:
                api_get_params.append(Parameter(col,kind=Parameter.POSITIONAL_OR_KEYWORD,annotation=arg_type))
    if api_key:
        get_query_params.append(security_parameter)
    def get_func(*args,**kwargs):
        return api_get(table,kwargs)
    sig = signature(get_func)
    sig = sig.replace(parameters=tuple(get_query_params))
    get_func.__signature__ = sig
    router.get(
        f"/{table.__name__}",
        summary=f'get items from {table.__name__} table',
        response_model= get_api_model(table,"RESPONSE"))(get_func)
    def del_func(*args,**kwargs):
        return api_delete(table,kwargs)
    del_fun_params = api_get_params
    if api_key:
        del_fun_params.append(security_parameter)
    sig = signature(del_func)
    sig = sig.replace(parameters=tuple(del_fun_params))
    del_func.__signature__ = sig
    router.delete(f"/{table.__name__}/{'/'.join(path_args)}",summary=f'delete items from {table.__name__} table')(del_func)
    if api_key:
        @router.post(f"/{table.__name__}",summary=f'post items to {table.__name__} table')
        def post_func(body:get_api_model(table,"POST"),api_key:APIKey=Depends(get_api_key)):
            return api_post(table,body)   
    else:
        @router.post(f"/{table.__name__}",summary=f'post items to {table.__name__} table')
        def post_func(body:get_api_model(table,"POST")):
            return api_post(table,body)
    
    def put_func(*args,**kwargs):
        pkeys = [i.name for i in table._pk_attrs_]
        entity_pkeys = {i:j for i,j in kwargs.items() if i in pkeys}
        return api_put(table,new_data = kwargs['body'].__dict__, entity_pkeys = entity_pkeys)
    pkey_fun_args = [Parameter(pkey.name,kind=Parameter.POSITIONAL_OR_KEYWORD) for pkey in table._pk_attrs_]
    body_arg = [Parameter("body",kind=Parameter.POSITIONAL_OR_KEYWORD,annotation=get_api_model(table,"PUT"))]
    put_args = pkey_fun_args+body_arg
    if api_key:
        put_args.append(security_parameter)
    sig = signature(put_func)
    sig = sig.replace(parameters=tuple(put_args))
    put_func.__signature__ = sig
    router.put(f"/{table.__name__}/{'/'.join(path_args)}",summary=f'update items in {table.__name__} table')(put_func)

    app.include_router(
        router,
        prefix=prefix,
        tags=['Database'])