"""
convert: functions that convert types
Corey Rayburn Yung <coreyrayburnyung@gmail.com>
Copyright 2020-2023, Corey Rayburn Yung
License: Apache-2.0

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

All tools should follow one of two form. For conversion of a known type
to another type, the function name should be:
    f'{item type}_to_{output type}'
For a conversion from an unknown type to another type, the function name should
be:
    f'to_{output type}'
     
Contents:
    dictify: converts to or validates a dict.
    hashify: converts to or validates a hashable object.
    instancify: converts to or validates an instance. If it is already an
        instance, any passed kwargs are added as attributes to the instance.
    integerify: converts to or validates an int. 
    iterify: converts to or validates an iterable.
    kwargify: uses annotations to turn positional arguments into keyword 
        arguments.
    listify: converts to or validates a list.
    namify: returns hashable name for passed item.
    numify: converts to or validates a numerical type.
    pathlibify: converts to or validates a pathlib.Path.
    stringify: converts to or validates a str.
    tuplify: converts to or validates a tuple.
    typify: converts a str type to other common types, if possible.
    windowify: Returns a sliding window of length 'n' over 'item'.
    to_dict:
    to_index
    str_to_index
    to_int
    str_to_int
    float_to_int
    to_list
    str_to_list
    to_float
    int_to_float
    str_to_float
    to_path
    str_to_path
    to_str
    int_to_str
    float_to_str
    list_to_str
    none_to_str
    path_to_str
    datetime_to_str
    
ToDo:
    Add more flexible tools.
    
"""
from __future__ import annotations
import ast
import collections
from collections.abc import (
    Hashable, Iterable, MutableMapping, MutableSequence, Sequence)
import datetime
import functools
import inspect
import itertools
import pathlib
from typing import Any, Optional, Type

from . import modify


""" General Converters """

@functools.singledispatch  
def dictify(item: Any, /) -> MutableMapping[Hashable, Any]:
    """Converts 'item' to a MutableMapping.
    
    Args:
        item (Any): item to convert to a MutableMapping.

    Raises:
        TypeError: if 'item' is a type that is not registered.

    Returns:
        MutableMapping: derived from 'item'.

    """
    if isinstance(item, MutableMapping):
        return item
    else:
        raise TypeError(
        f'item cannot be converted because it is an unsupported type: '
        f'{type(item).__name__}')
 
@functools.singledispatch   
def hashify(item: Any, /) -> Hashable:
    """Converts 'item' to a Hashable.
    
    Args:
        item (Any): item to convert to a Hashable.

    Raises:
        TypeError: if 'item' is a type that is not registered.

    Returns:
        Hashable: derived from 'item'.

    """
    if isinstance(item, Hashable):
        return item
    else:
        try:
            return hash(item)
        except TypeError:
            try:
                return str(item)
            except TypeError:
                try:
                    return modify.snakify(item.__name__)
                except AttributeError:
                    return modify.snakify(item.__class__.__name__)
                except AttributeError:
                    raise TypeError(f'item cannot be converted because it is ' 
                                    f'an unsupported type: '
                                    f'{type(item).__name__}')

def instancify(item: Type[Any] | object, **kwargs: Any) -> Any:
    """Returns 'item' as an instance with 'kwargs' as parameters/attributes.
    
    If 'item' is already an instance, kwargs are added as attributes to the
    existing 'item'. This will overwrite any existing attributes of the same
    name.

    Args:
        item (Type[Any] | object)): class to make an instance out of by 
            passing kwargs or an instance to add kwargs to as attributes.

    Raises:
        TypeError: if 'item' is neither a class nor instance.
        
    Returns:
        object: a class instance with 'kwargs' as attributes or passed as 
            parameters (if 'item' is a class).
        
    """         
    if inspect.isclass(item):
        return item(**kwargs)
    elif isinstance(item, object):
        for key, value in kwargs.items():
            setattr(item, key, value)
        return item
    else:
        raise TypeError('item must be a class or class instance')

@functools.singledispatch  
def integerify(item: Any, /) -> int:
    """Converts 'item' to an int.
    
    Args:
        item (Any): item to convert.

    Raises:
        TypeError: if 'item' is a type that cannot be converted.

    Returns:
        int: derived from 'item'.

    """
    if isinstance(item, int):
        return item
    else:
        raise TypeError(
            f'item cannot be converted because it is an '
            f'unsupported type: {type(item).__name__}')

@functools.singledispatch                  
def iterify(item: Any, /) -> Iterable:
    """Returns 'item' as an iterable, but does not iterate str types.
    
    Args:
        item (Any): item to turn into an iterable

    Returns:
        Iterable: of 'item'. A str type will be stored as a single item in an
            Iterable wrapper.
        
    """     
    if item is None:
        return iter(())
    elif isinstance(item, (str, bytes)):
        return iter([item])
    else:
        try:
            return iter(item)
        except TypeError:
            return iter((item,))
        
def kwargify(item: Type[Any], /, args: tuple[Any]) -> dict[Hashable, Any]:
    """Converts args to kwargs.
    
    Args:
    item (Type): the item with annotations used to construct kwargs.
        args (tuple): arguments without keywords passed to 'item'.
        
    Raises:
        ValueError: if there are more args than annotations in 'item'.
        
    Returns
        dict[Hashable, Any]: kwargs based on 'args' and 'item'.
    
    """
    annotations = list(item.__annotations__.keys())
    if len(args) > len(annotations):
        raise ValueError('There are too many args for item')
    else:
        return dict(zip(annotations, args))

@functools.singledispatch   
def listify(item: Any, /, default: Optional[Any] = None) -> Any:
    """Returns passed item as a list (if not already a list).

    Args:
        item (Any): item to be transformed into a list to allow proper 
            iteration.
        default (Optional[Any]): the default value to return if 'item' is None.
            Unfortunately, to indicate you want None to be the default value,
            you need to put 'None' in quotes. If not passed, 'default' is set to 
            [].

    Returns:
        Any: a passed list, 'item' converted to a list, or the 'default' 
            argument.

    """
    if item is None:
        if default is None:
            return []
        elif default in ['None', 'none']:
            return None
        else:
            return default
    elif isinstance(item, MutableSequence) and not isinstance(item, str):
        return item
    else:
        return [item]

@functools.singledispatch                            
def numify(item: Any, raise_error: bool = False) -> int | float | Any:
    """Converts 'item' to a numeric type.
    
    If 'item' cannot be converted to a numeric type and 'raise_error' is False, 
        'item' is returned as is.

    Args:
        item (str): item to be converted.
        raise_error (bool): whether to raise a TypeError when conversion to a
            numeric type fails (True) or to simply return 'item' (False). 
            Defaults to False.

    Raises:
        TypeError: if 'item' cannot be converted to a numeric type and 
            'raise_error' is True.
            
    Returns
        int | float | Any: converted to numeric type, if possible.

    """
    try:
        return int(item)
    except ValueError:
        try:
            return float(item)
        except ValueError:
            if raise_error:
                raise TypeError(
                    f'{item} not able to be converted to a numeric type')
            else:
                return item
            
@functools.singledispatch
def pathlibify(item: str | pathlib.Path, /) -> pathlib.Path:
    """Converts string 'path' to pathlib.Path object.

    Args:
        item (str | pathlib.Path): either a string summary of a path or a 
            pathlib.Path object.

    Raises:
        TypeError if 'path' is neither a str or pathlib.Path type.

    Returns:
        pathlib.Path object.

    """
    if isinstance(item, str):
        return pathlib.Path(item)
    elif isinstance(item, pathlib.Path):
        return item
    else:
        raise TypeError('item must be str or pathlib.Path type')
    
@functools.singledispatch           
def stringify(item: Any, /, default: Optional[Any] = None) -> Any:
    """Converts 'item' to a str from a Sequence.
    
    Args:
        item (Any): item to convert to a str from a list if it is a list.
        default (Any): value to return if 'item' is equivalent to a null
            value when passed. Defaults to None.
    
    Raises:
        TypeError: if 'item' is not a str or list-like object.
        
    Returns:
        Any: str, if item was a list, None or the default value if a null value
            was passed, or the item as it was passed if there previous two 
            conditions don't appply.

    """
    if item is None:
        if default is None:
            return ''
        elif default in ['None', 'none']: 
            return None
        else:
            return default
    elif isinstance(item, str):
        return item
    elif isinstance(item, Sequence):
        return ', '.join(item)
    else:
        raise TypeError('item must be str or a sequence')

@functools.singledispatch    
def tuplify(item: Any, /, default: Optional[Any] = None) -> Any:
    """Returns passed item as a tuple (if not already a tuple).

    Args:
        item (Any): item to be transformed into a tuple.
        default (Any): the default value to return if 'item' is None.
            Unfortunately, to indicate you want None to be the default value,
            you need to put 'None' in quotes. If not passed, 'default'
            is set to ().

    Returns:
        tuple[Any]: a passed tuple, 'item' converted to a tuple, or 
            'default'.

    """
    if item is None:
        if default is None:
            return tuple()
        elif default in ['None', 'none']:
            return None
        else:
            return default
    elif isinstance(item, tuple):
        return item
    elif isinstance(item, Iterable):
        return tuple(item)
    else:
        return tuple([item])
        
def typify(item: str) -> Sequence[Any] | int | float | bool | str:
    """Converts stings to appropriate, supported datatypes.

    The method converts strings to list (if ', ' is present), int, float,
    or bool datatypes based upon the content of the string. If no
    alternative datatype is found, the item is returned in its original
    form.

    Args:
        item (str): string to be converted to appropriate datatype.

    Returns:
        Sequence[Any] | int | float | bool | str: converted item.

    """
    if not isinstance(item, str):
        return item
    else:
        try:
            return int(item)
        except ValueError:
            try:
                return float(item)
            except ValueError:
                if item.lower() in ['true', 'yes']:
                    return True
                elif item.lower() in ['false', 'no']:
                    return False
                elif ', ' in item:
                    item = item.split(', ')
                    return [typify(i) for i in item]
                else:
                    return item

def windowify(
    item: Sequence[Any], 
    length: int, 
    fill_value: Optional[Any] = None, 
    step: Optional[int] = 1) -> Sequence[Any]:
    """Returns a sliding window of length 'n' over 'item'.

    This code is adapted from more_itertools.windowed to remove a dependency.
   
    Args:
        item (Sequence[Any]): sequence from which to return windows.
        length (int): length of window.
        fill_value (Optional[Any]): value to use for items in a window that do 
            not exist when length > len(item). Defaults to None.
        step (Optional[Any]): number of items to advance between each window.
            Defaults to 1.
            
    Raises:
        ValueError: if 'length' is less than 0 or step is less than 1.
        
    Returns:
        Sequence[Any]: windowed sequence derived from arguments.      

    """
    if length < 0:
        raise ValueError('length must be >= 0')
    if length == 0:
        yield tuple()
        return
    if step < 1:
        raise ValueError('step must be >= 1')
    window = collections.deque(maxlen = length)
    i = length
    for _ in map(window.append, item):
        i -= 1
        if not i:
            i = step
            yield tuple(window)
    size = len(window)
    if size < length:
        yield tuple(itertools.chain(
            window, itertools.repeat(fill_value, length - size)))
    elif 0 < i < min(step, length):
        window += (fill_value,) * i
        yield tuple(window)
                                         
""" Specific Converters """

@integerify.register
def float_to_int(item: float, /) -> int:
    """Converts 'item' to an int.
    
    Args:
        item (float): item to convert.
        
    Returns:
        int: derived from 'item'.
        
    """ 
    return int(item)

@integerify.register
def str_to_int(item: str, /) -> int:
    """Converts 'item' to an int.
    
    Args:
        item (str): item to convert.
        
    Returns:
        int: derived from 'item'.
        
    """    
    return int(item)

# @camina.dynamic.dispatcher   
def to_list(item: Any, /) -> list[Any]:
    """Converts 'item' to a list.
    
    Args:
        item (Any): item to convert to a list.

    Raises:
        TypeError: if 'item' is a type that is not registered.

    Returns:
        list[Any]: derived from 'item'.

    """
    if isinstance(item, list[Any]):
        return item
    else:
        raise TypeError(
            f'item cannot be converted because it is an unsupported type: '
            f'{type(item).__name__}')

# @to_list.register
def str_to_list(item: str, /) -> list[Any]:
    """[summary]

    Args:
        item (str): [description]

    Returns:
        list[Any]: [description]
    """    
    """Converts a str to a list."""
    return ast.literal_eval(item)

# @camina.dynamic.dispatcher   
def to_float(item: Any, /) -> float:
    """Converts 'item' to a float.
    
    Args:
        item (Any): item to convert to a float.

    Raises:
        TypeError: if 'item' is a type that is not registered.

    Returns:
        float: derived from 'item'.

    """
    if isinstance(item, float):
        return item
    else:
        raise TypeError(
            f'item cannot be converted because it is an unsupported type: '
            f'{type(item).__name__}')

# @to_float.register
def int_to_float(item: int, /) -> float:
    """[summary]

    Args:
        item (int): [description]

    Returns:
        float: [description]
    """    
    """Converts an int to a float."""
    return float(item)

# @to_float.register
def str_to_float(item: str, /) -> float:
    """[summary]

    Args:
        item (str): [description]

    Returns:
        float: [description]
    """    
    """Converts a str to a float."""
    return float(item)

# @camina.dynamic.dispatcher   
def to_path(item: Any, /) -> pathlib.Path:
    """Converts 'item' to a pathlib.Path.
    
    Args:
        item (Any): item to convert to a pathlib.Path.

    Raises:
        TypeError: if 'item' is a type that is not registered.

    Returns:
        pathlib.Path: derived from 'item'.

    """
    if isinstance(item, pathlib.Path):
        return item
    else:
        raise TypeError(
            f'item cannot be converted because it is an unsupported type: '
            f'{type(item).__name__}')

@pathlibify.register  
def str_to_path(item: str, /) -> pathlib.Path:
    """[summary]

    Args:
        item (str): [description]

    Returns:
        pathlib.Path: [description]
    """    
    """Converts a str to a pathlib.Path."""
    return pathlib.pathlib.Path(item)

# @camina.dynamic.dispatcher   
def to_str(item: Any, /) -> str:
    """Converts 'item' to a str.
    
    Args:
        item (Any): item to convert to a str.

    Raises:
        TypeError: if 'item' is a type that is not registered.

    Returns:
        str: derived from 'item'.

    """
    if isinstance(item, str):
        return item
    else:
        raise TypeError(
            f'item cannot be converted because it is an unsupported type: '
            f'{type(item).__name__}')

# @to_str.register
def int_to_str(item: int, /) -> str:
    """[summary]

    Args:
        item (int): [description]

    Returns:
        str: [description]
    """    
    """Converts an int to a str."""
    return str(item)

# @to_str.register
def float_to_str(item: float, /) -> str:
    """[summary]

    Args:
        item (float): [description]

    Returns:
        str: [description]
    """    
    """Converts an float to a str."""
    return str(item)

# @to_str.register
def list_to_str(item: list[Any], /) -> str:
    """[summary]

    Args:
        item (list[Any]): [description]

    Returns:
        str: [description]
    """    
    """Converts a list to a str."""
    return ', '.join(item)
   
# @to_str.register 
def none_to_str(item: None, /) -> str:
    """[summary]

    Args:
        item (None): [description]

    Returns:
        str: [description]
    """    
    """Converts None to a str."""
    return 'None'

# @to_str.register
def path_to_str(item: pathlib.Path, /) -> str:
    """Converts a pathlib.Path to a str.

    Args:
        item (pathlib.Path): [description]

    Returns:
        str: [description]
        
    """    
    return str(item)

# @to_str.register
def datetime_to_string(
    item: datetime.datetime, /,
    time_format: Optional[str] = '%Y-%m-%d_%H-%M') -> str:
    """ Return datetime 'item' as a str based on 'time_format'.
    
    Args:
        item (datetime.datetime): datetime object to convert to a str.
        time_format (Optional[str]): format to create a str from datetime. The
            passed argument should follow the rules of datetime.strftime. 
            Defaults to '%Y-%m-%d_%H-%M'.
            
    Returns:
        str: converted datetime 'item'.
            
    """
    return item.strftime(time_format)
