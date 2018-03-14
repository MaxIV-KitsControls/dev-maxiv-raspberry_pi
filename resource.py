import socket
from functools import wraps
from PyTango import DevState

def catch_connection_error(func):
    """Decorator for connection errors."""
    
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except (BrokenPipeError, ConnectionRefusedError,
                socket.timeout) as connectionerror:
            self.set_state(DevState.FAULT)
            raise ValueError("Connection error")
    
    return wrapper
