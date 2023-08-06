from typing import Iterable, overload, Any, Callable, NoReturn, Optional, Tuple, Union, Type
_Key = str | int
_Value = Any

def get_value(iterable:Iterable, *key:_Key) -> _Value:
    for k in key:
        if (k < len(iterable) if isinstance(iterable,list) else k in iterable.keys()):
            iterable = iterable[k]
        else:
            raise IndexError()
    return iterable
def get_index(iterable:Iterable, value:_Value) -> _Key:
    if isinstance(iterable, dict):
        return list(iterable.keys())[list(iterable.values()).index(value)]
    else:
        return iterable.index(value)
def get_keys(iterable:Iterable, *key:_Key) -> list:
    iterable = get_value(iterable, *key)
    if isinstance(iterable, dict):
        return list(iterable.keys())
    else:
        return list(range(len(iterable)))
def get_values(iterable:Iterable, *key:_Key) -> list:
    iterable = get_value(iterable, *key)
    if isinstance(iterable, dict):
        return list(iterable.values())
    else:
        return iterable.copy()
def get_items(iterable:Iterable, *key:_Key) -> list:
    iterable = get_value(iterable, *key)
    if isinstance(iterable, dict):
        return list(iterable.items())
    else:
        return list(enumerate(iterable))

def where(iterable:Iterable, func:Callable[[_Key,_Value],bool]=lambda key, value: True, getkey:bool=False) -> Iterable:
    result = dict()
    iterable = todict(iterable)
    for key, value in iterable.items():
        if func(key, value):
            result[key] = value
    if not getkey:
        result = list(result.values())
    return result
def oftype(iterable:Iterable, types:Union[Tuple[Type],Type], getkey:bool=False) -> Iterable:
    return where(iterable, lambda key,value: isinstance(value,types), getkey)
def first(iterable:Iterable, func:Callable[[_Key,_Value],bool]=lambda key, value: True) -> Optional[Tuple[_Key,_Value]]:
    iterable = todict(iterable)
    for key, value in iterable.items():
        if func(key, value):
            return (key,value)
    return (None,None)
def last(iterable:Iterable, func:Callable[[_Key,_Value],bool]=lambda key, value: True) -> Optional[Tuple[_Key,_Value]]:
    result = where(iterable, func, getkey=True)
    if len(result) == 0:
        return (None,None)
    else:
        return list(result.items())[-1]
def single(iterable:Iterable, func:Callable[[_Key,_Value],bool]=lambda key, value: True) -> Optional[Tuple[_Key,_Value]]:
    result = where(iterable, func, getkey=True)
    if len(result) != 1:
        return (None,None)
    else:
        return list(result.items())[0]
def orderby(iterable:Iterable[str], func:Callable[[_Key,_Value],bool]=lambda key, value: value, desc:bool=False) -> Iterable:
    if isinstance(iterable, dict):
        return dict(sorted(iterable.items(), key=lambda x: func(x[0],x[1]), reverse=desc))
    else:
        return list(dict(sorted(enumerate(iterable), key=lambda x: func(x[0],x[1]), reverse=desc)).values())
def tolist(iterable:Iterable) -> list:
    return (iterable.copy() if isinstance(iterable, list) else list(iterable.values()))
def todict(iterable:Iterable) -> dict:
    return (iterable.copy() if isinstance(iterable, dict) else dict(enumerate(iterable)))

def any(iterable:Iterable, func:Callable[[_Key,_Value],bool]=lambda key, value: True) -> bool:
    result = False
    iterable = todict(iterable)
    for key, value in iterable.items():
        if func(key, value):
            result = True
            break
    return result
def all(iterable:Iterable, func:Callable[[_Key,_Value],bool]=lambda key, value: True) -> bool:
    result = True
    iterable = todict(iterable)
    for key, value in iterable.items():
        if not func(key, value):
            result = False
            break
    return result
def isempty(iterable:Iterable) -> bool:
    return iterable in [[],{},None]

def count(iterable:Iterable, value:_Value) -> int:
    if isinstance(iterable, dict):
        return list(iterable.values()).count(value)
    else:
        return iterable.count(value)      
def lenght(iterable:Iterable) -> int:
    return len(iterable) 
def sum(iterable:Iterable[int]) -> Optional[int]:
    if all(iterable,lambda k,v: isinstance(v,(int,float))):
        iterable = get_values(iterable)
        return sum(iterable)
    else:
        return None
def avg(iterable:Iterable[int]) -> Optional[int]:
    if all(iterable,lambda k,v: isinstance(v,(int,float))):
        return sum(iterable) / len(iterable)
    else:
        return None
def max(iterable:Iterable[int]) -> Optional[int]:
    if all(iterable,lambda k,v: isinstance(v,(int,float))):
        iterable = get_values(iterable)
        return max(iterable)
    else:
        return None
def min(iterable:Iterable[int]) -> Optional[int]:
    if all(iterable,lambda k,v: isinstance(v,(int,float))):
        iterable = get_values(iterable)
        return min(iterable)
    else:
        return None

@overload
def add(iterable:Iterable, value:_Value): ...
@overload
def add(iterable:Iterable, key:_Key, value:_Value): ...
def add(iterable:Iterable, v1, v2=...):
    if isinstance(iterable, dict):
        iterable[v1] = (None if v2 is ... else v2)
    else:
        if v2 is ...:
            iterable.append(v1)
        else:
            iterable.insert(v1, v2)
def update(iterable:Iterable, key:_Key, value:_Value):
    iterable[key] = value
def union(iterable:Iterable, *new_iterable:Iterable):
    for new_i in new_iterable:
        if isinstance(iterable, dict):
            iterable.update(new_i)
        else:
            iterable.extend(new_i)
def delete(iterable:Iterable, *key:_Key):
    for k in key:
        iterable.pop(k)
def remove(iterable:Iterable, *value:_Value, all:bool=False):
    for v in value:
        if isinstance(iterable, dict):
            iterable.pop(first(iterable, lambda k, va: va == v)[0])
        else:
            if all:
                while True:
                    if iterable.count(v) == 0:
                        break
                    iterable.remove(v)
            else:
                iterable.remove(v)
def clear(iterable:Iterable):
    iterable.clear()

@overload
def ingets(iterable:Iterable, func:Callable[[_Key,_Value],_Value]=lambda key, value: value) -> Iterable: ...
@overload
def ingets(iterable:Iterable, func:Callable[[_Key,_Value],_Value]=lambda key, value: value, key_func:Callable[[_Key,_Value],_Value]=lambda key, value: key) -> Iterable: ...
def ingets(iterable:Iterable, f1=lambda k,v: v, f2=...) -> Iterable:
    if isinstance(iterable, dict):
        return dict(zip((iterable.keys() if f2 is ... else map(f2,iterable.keys(),iterable.values())),map(f1,iterable.keys(),iterable.values())))
    else:
        return list(map(f1,range(len(iterable)),iterable))
@overload
def insets(iterable:Iterable, func:Callable[[_Key,_Value],_Value]=lambda key, value: value) -> Iterable: ...
@overload
def insets(iterable:Iterable, func:Callable[[_Key,_Value],_Value]=lambda key, value: value, key_func:Callable[[_Key,_Value],_Value]=lambda key, value: key) -> Iterable: ...
def insets(iterable:Iterable, f1=lambda k,v: v, f2=...):
    if isinstance(iterable, dict):
        new_iterable = dict(zip((iterable.keys() if f2 is ... else map(f2,iterable.keys(),iterable.values())),map(f1,iterable.keys(),iterable.values())))
        iterable.clear()
        iterable.update(new_iterable)
    else:
        new_iterable = list(map(f1,range(len(iterable)),iterable))
        iterable.clear()
        iterable.extend(new_iterable)

__all__ = [
    "_Key", "_Value",
    "get_value", "get_index", "get_values", "get_keys", "get_items",
    "where", "first", "last", "single", "oftype",
    "any", "all", "isempty",
    "tolist", "todict",
    "count", "lenght", "avg", "max", "min", "orderby",
    "add", "update", "union", "delete", "remove", "clear",
    "ingets", "insets"
]