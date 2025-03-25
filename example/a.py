from typing import Generator, Callable, Iterable, Optional, List, Tuple
from collections.abc import Mapping

class CustomDict[K,V](
    Mapping[K,V]):





    """Bad
    docstring
    """
    
    def __init__(self, data: dict[K, V]) -> None:
        self._data = data

    def __getitem__(self, key: K) -> V:
        try:
            return self._data[key]
        except KeyError:
            raise KeyError(f"Key {key} not found")

    

    

    def __len__(self) -> int:
        return len(self._data)

def process_data[T,R:List[str]](data: Iterable[T], processor: Callable[[T], R]) -> Generator[R, None, None]:
    """Another docstring"""
    for item in data:
        try:
            yield processor(item)
        except Exception as e:
            print(f"Error processing item {item}: {e}")

def get_value[K,V](mapping: Mapping[K, V], key: K) -> V | None | KeyError:
    if key in mapping:
        return mapping[key]
    else:
        raise KeyError(f"Key '{key}' not found in mapping.")

def complex_function(x: float, y: float) -> Generator[Optional[str], None, Tuple[float, float]]:
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
    return x+y,x*y

class DataProcessor[T,R]:




    """Third docstring"""

    def __init__(self, data: Iterable[T]) -> None:
        """Last docstring"""
        self.data = data

    def __iter__(self) -> Generator[T, None, None]:
        yield from self.data

    def filter_data(self, condition: Callable[[T], bool]) -> Generator[T, None, None]:
        for item in self.data:
            if condition(item):
                yield item

    def map_data(self, function: Callable[[T], R]) -> Generator[R, None, None]:
        for item in self.data:
            yield function(item)

def example_generator() -> Generator[int, None, None]:
    try:
        for i in range(5):
            if i == 3:
                raise ValueError("Forced error on 3")
            yield i
    except ValueError as e:
        print(f"Exception caught: {e}")
        yield -1



def process_collection[K,V](data: Iterable[CustomDict[K,V]]) -> Generator[str, None, None]:
    try:
        for item in data:
            if isinstance(item, int) and item < 0:
                raise ValueError("Negative integer detected")
            yield f"Processed item: {item}"
    except ValueError as e:
        print(f"Caught exception: {e}")
        yield f"Error processing item: {e}"

def multi_type_function[X:int](x: X, y: int) -> int | float | str | X:
    try:
        if isinstance(x, float) and isinstance(y, float):
            return x * y
        elif isinstance(x, str) and isinstance(y, str):
            return x + y
        return x
    except Exception as e:
        raise e
