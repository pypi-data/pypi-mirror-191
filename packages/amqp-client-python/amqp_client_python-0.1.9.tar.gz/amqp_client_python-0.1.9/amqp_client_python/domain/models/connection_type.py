from enum import Enum

class ConnectionType(Enum):
    pub = "_pub_connection"
    sub = "_sub_connection"
    rpc_client = "_rpc_client_connection"
    rpc_server = "_rpc_server_connection"