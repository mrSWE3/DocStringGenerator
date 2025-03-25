from typing import TypeVar, Generator, Callable, Iterable, Union, Optional, Any
from collections.abc import Mapping

class CustomDict[K,V](Mapping):
    """
    ## Summary
        
    ## Type Params
        K: 
        V: 
    """

    def __init__(self, data: dict[K, V]) -> None:
        """
        ## Summary
            
        ## Args
            data (dict[K, V]): 
        """
        self._data = data

    def __getitem__(self, key: K) -> V:
        """
        ## Summary
            
        ## Args
            key (K): 
        ## Return
            V
        """
        try:
            return self._data[key]
        except KeyError:
            raise KeyError(f"Key {key} not found")

    def __iter__(self) -> Iterable[K]:
        """
        ## Summary
            
        ## Return
            Iterable[K]
        """
        yield from self._data

    def __len__(self) -> int:
        """
        ## Summary
            
        ## Return
            int
        """
        return len(self._data)

def process_data[T,R:T](data: Iterable[T], processor: Callable[[T], R]) -> Generator[R, None, None]:
    """
    ## Summary
        
    ## Type params
        T: 
        R (T): 
    ## Args
        data (Iterable[T]): 
        processor (Callable[[T], R]): 
    ## Yields
        R
    ## Return
        Generator[R, None, None]
    """
    for item in data:
        try:
            yield processor(item)
        except Exception as e:
            print(f"Error processing item {item}: {e}")
            yield None

def get_value[K,V](mapping: Mapping[K, V], key: K) -> V | None | KeyError:
    """
    ## Summary
        
    ## Type params
        K: 
        V: 
    ## Args
        mapping (Mapping[K, V]): 
        key (K): 
    ## Return
        V | None | KeyError
    """
    if key in mapping:
        return mapping[key]
    else:
        raise KeyError(f"Key '{key}' not found in mapping.")

def complex_function[T](x: T, y: int | float) -> Generator[Optional[str], None, None]:
    """
    ## Summary
        
    ## Type params
        T: 
    ## Args
        x (T): 
        y (int | float): 
    ## Yields
        Optional[str]
    ## Return
        Generator[Optional[str], None, None]
    """
    try:
        if isinstance(x, int):
            yield str(x * y)
        elif isinstance(x, str):
            yield f"{x} with {y}"
        else:
            yield None
    except TypeError as e:
        print(f"Error: {e}")
        yield None

class DataProcessor[T,R]:
    """
    ## Summary
        
    ## Type Params
        T: 
        R: 
    """

    def __init__(self, data: Iterable[T]) -> None:
        """
        ## Summary
            
        ## Args
            data (Iterable[T]): 
        """
        self.data = data

    def __iter__(self) -> Generator[T, None, None]:
        """
        ## Summary
            
        ## Yields
            T
        ## Return
            Generator[T, None, None]
        """
        yield from self.data

    def filter_data(self, condition: Callable[[T], bool]) -> Generator[T, None, None]:
        """
        ## Summary
            
        ## Args
            condition (Callable[[T], bool]): 
        ## Yields
            T
        ## Return
            Generator[T, None, None]
        """
        for item in self.data:
            if condition(item):
                yield item

    def map_data(self, function: Callable[[T], R]) -> Generator[R, None, None]:
        """
        ## Summary
            
        ## Args
            function (Callable[[T], R]): 
        ## Yields
            R
        ## Return
            Generator[R, None, None]
        """
        for item in self.data:
            yield function(item)

def example_generator() -> Generator[int, None, None]:
    """
    ## Summary
        
    ## Yields
        int
    ## Return
        Generator[int, None, None]
    """
    try:
        for i in range(5):
            if i == 3:
                raise ValueError("Forced error on 3")
            yield i
    except ValueError as e:
        print(f"Exception caught: {e}")
        yield -1

def another_example_function[X,Y](x: X, y: Y) -> Generator[str, None, None]:
    """
    ## Summary
        
    ## Type params
        X: 
        Y: 
    ## Args
        x (X): 
        y (Y): 
    ## Yields
        str
    ## Return
        Generator[str, None, None]
    """
    if x < y:
        yield f"{x} is smaller than {y}"
    elif x > y:
        yield f"{x} is greater than {y}"
    else:
        yield f"{x} equals {y}"

def process_collection[T](data: Iterable[CustomDict]) -> Generator[str, None, None]:
    """
    ## Summary
        
    ## Type params
        T: 
    ## Args
        data (Iterable[CustomDict]): 
    ## Yields
        str
    ## Return
        Generator[str, None, None]
    """
    try:
        for item in data:
            if isinstance(item, int) and item < 0:
                raise ValueError("Negative integer detected")
            yield f"Processed item: {item}"
    except ValueError as e:
        print(f"Caught exception: {e}")
        yield f"Error processing item: {e}"

def multi_type_function[X,Y](x: X, y: Y) -> int | float | str | None:
    """
    ## Summary
        
    ## Type params
        X: 
        Y: 
    ## Args
        x (X): 
        y (Y): 
    ## Return
        int | float | str | None
    """
    try:
        if isinstance(x, int) and isinstance(y, int):
            return x + y
        elif isinstance(x, float) and isinstance(y, float):
            return x * y
        elif isinstance(x, str) and isinstance(y, str):
            return x + y
        return None
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None
