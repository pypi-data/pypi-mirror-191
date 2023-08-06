from .f5py import *

__doc__ = f5py.__doc__
if hasattr(f5py, "__all__"):
    __all__ = f5py.__all__