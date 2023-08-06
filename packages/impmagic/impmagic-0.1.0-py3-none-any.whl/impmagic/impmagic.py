import __main__
import inspect
import sys

__main__.__dict__['imp_cache'] = {}
CACHE = __main__.__dict__['imp_cache']

#Importation de module à partir d'un tuple ou d'une liste
def load(data, func=None, globals=None):
    #if 'imp_cache' not in __main__.__dict__:
    #    __main__.__dict__['imp_cache'] = {}    

    if not func:
        if globals:
            func = globals
        else:
            current_frame = inspect.currentframe()
            calling_frame = current_frame.f_back
            calling_globals = calling_frame.f_globals
            func = calling_globals
    else:
        func = func.__globals__

    if isinstance(data, tuple) or isinstance(data, list):
        for mod in data:
            if isinstance(mod, dict):
                if 'submodule' in mod and mod['submodule']!=None:
                    #print(mod)
                    for sub in mod['submodule']:
                        try:
                            if 'as' in mod:
                                name = mod['module']+"."+sub+mod['as']
                                if name in CACHE:
                                    func[mod['as']] = CACHE[name]
                                else:
                                    funct_in = getattr(__import__(mod['module'], fromlist=['object']), sub)
                                    CACHE[name] = funct_in
                                    func[mod['as']] = funct_in
                            else:
                                name = mod['module']+"."+sub
                                if name in CACHE:
                                    func[sub] = CACHE[name]
                                else:
                                    funct_in = getattr(__import__(mod['module'], fromlist=['object']), sub)
                                    CACHE[name] = funct_in
                                    func[sub] = funct_in
                        except:
                            if 'as' in mod:
                                name = mod['module']+"."+sub+mod['as']
                                if name in CACHE:
                                    func[mod['as']] = CACHE[name]
                                else:
                                    funct = __import__(mod['module']+"."+sub, fromlist=['object'])
                                    CACHE[name] = funct
                                    func[mod['as']] = funct
                            else:
                                name = mod['module']+"."+sub
                                if name in CACHE:
                                    func[sub] = CACHE[name]
                                else:
                                    funct = __import__(mod['module']+"."+sub, fromlist=['object'])
                                    CACHE[name] = funct
                                    func[sub] = funct
                else:
                    if 'as' in mod:
                        name = mod['module']+"."+mod['as']
                        if name in CACHE:
                            func[mod['as']] = CACHE[name]
                        else:
                            funct = __import__(mod['module'], fromlist=['object'])
                            CACHE[name] = funct
                            func[mod['as']] = funct
                    else:
                        name = mod['module']
                        if name in CACHE:
                            func[mod['module']] = CACHE[name]
                        else:
                            funct = __import__(mod['module'], fromlist=['object'])
                            CACHE[name] = funct
                            func[mod['module']] = funct
            else:
                funct = __import__(mod, fromlist=['object'])
                CACHE[mod] = funct
                func[mod] = funct
                
    elif isinstance(data, str):
        funct = __import__(data, fromlist=['object'])
        CACHE[data] = funct
        func[data] = funct

#Décharger un module
def unload(modulename, uncache=False):
    if uncache:
        if 'imp_cache' in __main__.__dict__:
            if modulename in __main__.__dict__['imp_cache']:
                del __main__.__dict__['imp_cache'][modulename]
                #print("remove from cache")

    current_frame = inspect.currentframe()
    calling_frame = current_frame.f_back
    calling_globals = calling_frame.f_globals
    if modulename in calling_globals:
        del calling_globals[modulename]
    del sys.modules[modulename]

#Rechargement d'un module
def reload(modulename):
    unload(modulename, uncache=True)
    current_frame = inspect.currentframe()
    calling_frame = current_frame.f_back
    load(modulename, globals = calling_frame.f_globals)

#Chargement d'un module à partir du cache
def from_cache(modulename):
    if 'imp_cache' in __main__.__dict__:
        CACHE = __main__.__dict__['imp_cache']
        if modulename in CACHE:
            return CACHE[modulename]

    if modulename in sys.modules:
        return sys.modules[modulename]

    return None


#Décorateur pour l'importation de module
def loader(*data):
    def inner(func):
        def wrapper(*args, **kwargs):
            load(data, func)
            return func(*args, **kwargs)
        return wrapper
    return inner 


"""
@loader()
def payload():
    pass

payload()
"""