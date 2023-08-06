from __future__ import annotations
from bidict import bidict, OnDup, OD
from abc import abstractmethod, ABC
from typing import Dict, List, Union


def create_types_class(types: Union[Dict[str, str], List[str]]) -> BaseTypes:
    if isinstance(types, dict):
        return DictTypes(types)

    return ListTypes(types)


class BaseTypes(ABC):
    def __init__(self, data: Union[Dict[str, str], List[str]]) -> None:
        self.data = data

    @abstractmethod
    def get(self, key: Union[str, int]) -> str:
        pass


class DictTypes(BaseTypes):
    """This class is used to convert between the integer values used by the API and the string values used by the user.
       It is implemented as a bidirectional dictionary, but with some custom logic to handle duplicate keys and values.
       The API will return duplicate keys, but the user should not be able to set duplicate values.
    """
    
    def __init__(self, data: Dict[str, str]) -> None:
        """This is an initializer for the class.
           Converts the dictionary to a bidict, and converts the keys to integers.
        """
        self.data = bidict()
        self.data.on_dup = OnDup(key=OD.RAISE, val=OD.DROP_NEW, kv=OD.DROP_NEW)
        self.data.putall([(int(k), v) for k, v in data.items()], on_dup=OnDup(key=OD.DROP_NEW, val=OD.DROP_NEW, kv=OD.DROP_NEW))

    def get(self, key: int) -> str:
        """
        This method returns the value associated with the given key.
        :param key: The key to look up.
        :return: The value associated with the given key.
        """
        return self.data.get(key)

    def get_inverse(self, key: str) -> str:
        """
        This method returns the key associated with the given value.
        :param key: The value to look up.
        :return: The key associated with the given value.
        """
        return self.data.inverse.get(key)

class ListTypes(BaseTypes):
    def get(self, key: int) -> str:
        return self.data[key]
