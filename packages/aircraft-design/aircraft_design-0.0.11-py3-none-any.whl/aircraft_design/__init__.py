#!/usr/bin/env python3
from .classes.runner import __config_path__, __list_bin_path__
from .classes import AircraftDesignError
from avlwrapper import Control, Parameter, Case

__AVL_LINK__ = 'https://github.com/NisusAerodesign/aircraft-design/releases/download/binaries/avl'

if not __config_path__ / 'avl' in __list_bin_path__:
    import requests
    import os, stat
    
    try:
        file = requests.get(__AVL_LINK__)
        avl_path = str(__config_path__ / 'avl')
        open(avl_path, 'wb').write(file.content)

        st = os.stat(avl_path)
        os.chmod(avl_path, st.st_mode | stat.S_IEXEC) 
    except:
        raise AircraftDesignError('Binary not found!')

from .classes import Aircraft, Wing, Session, MultiSession
