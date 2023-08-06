import pandas as _pandas

__all__ = []
for name in dir(_pandas):
    if name.startswith('_'):
        continue
    obj = getattr(_pandas, name)
    globals()[name] = obj
    __all__.append(name)

del _pandas

# suppress FutureWarning only when importing pandus
def pandus_import(name, globals=None, locals=None, fromlist=(), level=0):
    if name == 'pandus':
        with warnings.catch_warnings():
            warnings.simplefilter(action='ignore', category=FutureWarning)
            return __import__('pandus', globals, locals, fromlist, level)
    else:
        return __import__(name, globals, locals, fromlist, level)

import builtins
builtins.__import__ = pandus_import

