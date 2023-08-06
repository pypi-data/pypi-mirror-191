from typing import Callable, Iterable, Optional, Tuple, Union, Type, overload
from linqex.builds import *

version = '1.2'

def enumerable_catch(linq:"Enumerable",iterable:Iterable, items:bool=False, onevalue:bool=False) -> Union["Enumerable",Iterable]:
    if items:
        new_enumerable = Enumerable(iterable[1] if isinstance(iterable[1], (dict,list)) and not onevalue else [iterable[1]])
        new_enumerable.keys_history = linq.keys_history.copy()
        new_enumerable.keys_history.append(iterable[0])
    else:
        new_enumerable = Enumerable(iterable)
        new_enumerable.keys_history = linq.keys_history.copy()
    new_enumerable._onevalue = onevalue
    new_enumerable._main = linq._main
    return new_enumerable
def enumerable_to_value(enumerable_or_value:Union["Enumerable",_Value]):
    if isinstance(enumerable_or_value, Enumerable):
        return enumerable_or_value.toValue
    else:
        return enumerable_or_value

class Enumerable:
    def __init__(self, iterable:Iterable):
        self.iterable = enumerable_to_value(iterable)
        self.keys_history = list()
        self._main:Enumerable = self
        self._onevalue = False
        if not isinstance(self.iterable,(list,dict)):
            if isinstance(self.iterable,(tuple,set)):
                self.iterable = list(self.iterable)
            else:
                raise TypeError("'{}' object is not iterable".format(str(type(self.iterable))))
    def __call__(self, iterable:Iterable):
        self.__init__(iterable)

    @property
    def type(self) -> bool:
        return type(self.iterable)

    def get(self, *key:_Key) -> Union["Enumerable",_Value]:
        result = get_value(self.iterable, *key)
        if isinstance(result,(list,dict)):
            return enumerable_catch(self,(key,result),items=True)
        else:
            return result
    def get_index(self, value:_Value) -> _Key:
        value = enumerable_to_value(value)
        return get_index(self.iterable, value)
    def get_keys(self, *key:_Key) -> list:
        return get_keys(self.iterable, *key)
    def get_values(self, *key:_Key) -> list:
        return get_values(self.iterable, *key)
    def get_items(self,*key:_Key) -> list:
        return get_items(self.iterable, *key)

    def where(self, func:Callable[[_Key,_Value],bool]=lambda key, value: True, getkey:bool=False) -> "Enumerable":
        return enumerable_catch(self,where(self.iterable,func, getkey))
    def oftype(self, *types:Type, getkey:bool=False) -> "Enumerable":
        return enumerable_catch(self,oftype(self.iterable,*types, getkey=getkey))
    def first(self, func:Callable[[_Key,_Value],bool]=lambda key, value: True) -> Optional[Union["Enumerable",_Value]]:
        return enumerable_catch(self,first(self.iterable,func),items=True,onevalue=True)
    def last(self, func:Callable[[_Key,_Value],bool]=lambda key, value: True) -> Optional[Union["Enumerable",_Value]]:
        return enumerable_catch(self,last(self.iterable,func),items=True,onevalue=True)
    def single(self, func:Callable[[_Key,_Value],bool]=lambda key, value: True) -> Optional[Union["Enumerable",_Value]]:
        return enumerable_catch(self,single(self.iterable,func),items=True,onevalue=True)    
    def orderby(self, func:Callable[[_Key,_Value],bool]=lambda key, value: value, desc:bool=False) -> "Enumerable":
        return enumerable_catch(self,orderby(self.iterable, func, desc=desc))

    def any(self, func:Callable[[_Key,_Value],bool]=lambda key, value: True) -> bool:
        return any(self.iterable,func)
    def all(self, func:Callable[[_Key,_Value],bool]=lambda key, value: True) -> bool:
        return all(self.iterable,func)

    def count(self, size:_Value) -> int:
        return count(self.iterable, size)
    def lenght(self) ->  int:
        return lenght(self.iterable)
    def sum(self) -> Optional[int]:
        return sum(self.iterable)
    def avg(self) -> Optional[int]:
        return avg(self.iterable)
    def max(self) -> Optional[int]:
        return max(self.iterable)
    def min(self) -> Optional[int]:
        return min(self.iterable)
    
    def set(self, value:_Value):
        value = enumerable_to_value(value)
        if len(self.keys_history) == 0:
            self.iterable = value
        else:
            self._main.get(*self.keys_history[:len(self.keys_history)-1]).update(self.toKey, value)
            self.iterable = value
    @overload
    def add(self, value:_Value): ...
    @overload
    def add(self, key:_Key, value:_Value): ...
    def add(self, v1, v2=...):
        v1, v2 = enumerable_to_value(v1), enumerable_to_value(v2)
        add(self.iterable, v1, v2)
    def update(self, key:_Key, value:_Value):
        value = enumerable_to_value(value)
        update(self.iterable, key, value)
    def union(self, *iterable:Iterable):
        union(self.iterable, *list(map(lambda v: enumerable_to_value(v), list(iterable))))
    def delete(self, *key:_Key):
        delete(self.iterable, *key)
    def remove(self, *value:_Value, all:bool=False):
        value = enumerable_to_value(value)
        remove(self.iterable, *value, all=all)
    def clear(self):
        clear(self.iterable)

    @overload
    def ingets(self, func:Callable[[_Key,_Value],_Value]=lambda key, value: value) -> "Enumerable": ...
    @overload
    def ingets(self, func:Callable[[_Key,_Value],_Value]=lambda key, value: value, key_func:Callable[[_Key,_Value],_Value]=lambda key, value: key) -> "Enumerable": ...
    def ingets(self, f1=lambda k,v: v, f2=...) -> "Enumerable":
        return Enumerable(ingets(self.iterable,f1,f2))
    @overload
    def insets(self, func:Callable[[_Key,_Value],_Value]=lambda key, value: value) -> "Enumerable": ...
    @overload
    def insets(self, func:Callable[[_Key,_Value],_Value]=lambda key, value: value, key_func:Callable[[_Key,_Value],_Value]=lambda key, value: key) -> "Enumerable": ...
    def insets(self, f1=lambda k,v: v, f2=...) -> "Enumerable":
        insets(self.iterable, f1, f2)

    def isType(self, type:Union[Tuple[Type],Type]) -> bool:
        return isinstance(self.iterable, type)
    def isKey(self, key:_Key) -> bool:
        if key == self.toKey:
            return True
        else:
            return False
    def isValue(self, value:_Value) -> bool:
        value = enumerable_to_value(value)
        if value == self.toValue:
            return True
        else:
            return False
    def inKey(self, *key:_Key) -> bool:
        iterable = self.get_keys()
        for k in key:
            if not k in iterable:
                return False
        return True
    def inValue(self, *value:_Value) -> bool:
        value = enumerable_to_value(value)
        iterable = self.get_values()
        for v in value:
            if not v in iterable:
                return False
        return True

    def convert_toList(self) -> Iterable:
        if isinstance(self.iterable, dict):
            self.set(self.toList)
        return self.toValue
    def convert_toDict(self) -> Iterable:
        if isinstance(self.iterable, list):
            self.set(self.toDict)
        return self.toValue
    def copy(self) -> "Enumerable":
        return Enumerable(self.iterable.copy())
    @property
    def toKey(self) -> _Key:
        if self.keys_history == []:
            return None
        else:
            return self.keys_history[-1]
    @property
    def toValue(self) -> _Value:
        if len(self.iterable) == 1 and self._onevalue:
            return self.get_values()[0]
        else:
            if isinstance(self.iterable, (list,dict)):
                return self.iterable.copy()
            else:
                return self.iterable
    @property
    def toList(self) -> Iterable:
        return tolist(self.iterable)
    @property
    def toDict(self) -> Iterable:
        return todict(self.iterable)
    @property
    def isEmpty(self) -> bool:
        return isempty(self.iterable)

    @classmethod
    def list(cls):
        return Enumerable(list())
    @classmethod
    def dict(cls):
        return Enumerable(dict())
    
    def __len__(self):
        return self.lenght()
    def __bool__(self):
        return not self.isEmpty
    def __getitem__(self,key):
        return self.get(key)
    def __setitem__(self,key,value):
        self.update(key,value)
    def __delitem__(self,key):
        self.delete(key)

__all__ = [
    "Enumerable", "version"
]