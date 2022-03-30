# from dataclasses import dataclass
# import pytest
# from client import RPCMessage, Marshal, ClassWithAttrs
# import json
    
# def test_marshalling():
    
#     @dataclass
#     class ClassWithAttrs:
#         int_val: int
#         str_val: str

#     obj = ClassWithAttrs(1, 'hello world')

#     message_method = 'method_name'
#     msg = RPCMessage(message_method, obj)

#     marshalled_msg = Marshal.marshal(msg)
#     resp = Marshal.unmarshal(marshalled_msg)
#     r = Marshal.reinstantiate_classes(resp)

#     assert r

# if __name__ == "__main__":
#     test_marshalling()


