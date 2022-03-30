import inspect
import json
import sys

from pkg.comm.RPCmessages import *
from pkg.comm.request_types import *
from pkg.comm.Currency import *

def marshal(RPCMsg: RPCRequest):
    if not (isinstance(RPCMsg, RPCRequest) or isinstance(RPCMsg, RPCResponse)):
        raise NotImplementedError(f'{RPCMsg} not accepted. Behavior only guaranteed for RPCRequest currently')
    
    return toJSON(RPCMsg).encode('utf-8')
    

def unmarshal(marshalled_RPCMessage: bytes):
    if not isinstance(marshalled_RPCMessage, bytes):
        raise ValueError('arg must be marshalled RPCMessage')

    value = marshalled_RPCMessage.decode('utf-8')
    value = json.loads(value)
    value = reinstantiate_classes(value)
    
    return value

def toJSON(value):
    def get_class_fields(item):
        if inspect.isclass(item):
            return str(item)

        item_dict = item.__dict__
        item_dict['__class_name__'] = type(item).__name__
        return item_dict
    
    return json.dumps(value, default=lambda o: get_class_fields(o), sort_keys=True)

def reinstantiate_classes(obj_dict: dict):
    class_name = obj_dict.get('__class_name__', None)
    args = []

    for k, v in obj_dict.items():
        if k == '__class_name__': continue
        if isinstance(v, dict):
            if '__class_name__' in v: 
                v = reinstantiate_classes(v)

        args.append((k,v))             

    clsname_boundname_map = dict(inspect.getmembers(sys.modules[__name__], inspect.isclass))

    class_obj = clsname_boundname_map[class_name]
    args = {arg[0]: arg[1] for arg in args}
    
    return class_obj(**args)

