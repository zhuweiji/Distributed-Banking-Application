from dataclasses import dataclass
import uuid as _uuid

NOT_FOUND = "service not found"
MALFORMED = "malformed request"
INTERNAL_ERR = "internal server error"
OK = 'ok'


@dataclass
class RPCRequest:
    obj: any = None
    method: str = ''
    
    uuid: str = str(_uuid.uuid4())

@dataclass
class RPCResponse:
    status: str
    obj: any = None

    method: str = ''
    uuid: str = str(_uuid.uuid4())