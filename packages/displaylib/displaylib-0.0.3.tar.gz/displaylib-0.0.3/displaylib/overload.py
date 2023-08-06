from typing import Any
from types import FunctionType


class OverloadUnmatched(Exception):
    """Exception raised when no suitable overload is found based on the callers signature
    """
    def __init__(self, function_name: str, signature: str) -> None:
        super().__init__(self)
        self.function_name = function_name
        self.signature = signature
    
    def __str__(self) -> str:
        return f"function '{self.function_name}' has no overload of signature {self.signature}"


class overload:
    """Overload decorator

    Raises:
        OverloadUnmatched: no suitable overloaded function found

    Returns:
        function: overloaded function (also overwritten)
    """
    _uniques = {}

    def __init__(self, function: FunctionType) -> None:
        self.function_name = function.__name__
        hints = tuple(function.__annotations__.get(arg, object) for arg in function.__code__.co_varnames)
        signature = tuple(object if hint == Any else hint for hint in hints) # Any --> object
        if not function.__name__ in self._uniques:
            self._uniques[function.__name__] = {signature: function}
        else:
            self._uniques[function.__name__][signature] = function

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        signature = (*map(type, args), *map(type, kwargs.values()))
        print(signature)
        if signature in self._uniques[self.function_name]:
            function = self._uniques[self.function_name][signature]
            return function(*args, **kwargs)
        if (function := self._get_best_match(signature)):
            return function(*args, **kwargs)
        raise OverloadUnmatched(self.function_name, signature)

    def _get_best_match(self, signature: tuple) -> FunctionType | None:
        best_match = None
        best_points = 0

        for signature_option in self._uniques[self.function_name]:
            if len(signature) != len(signature_option):
                continue
            points = 0
            # print("OPTION:")
            for this, other in zip(signature, signature_option):
                # print(f"  CALLER ({this}) | POSSIBILITY ({other})")
                if issubclass(this, object):
                    points += 1
                elif this == other:
                    points += 1
            if points == best_points and points != 0: # prefer precise type over <object>
                # print("CLASHING:", best_match, "|", signature, "?", signature_option)
                a_points = 0
                b_points = 0
                for this, other, perfect in zip(best_match, signature, signature_option):
                    if perfect == object:
                        continue
                    if this != object:
                        a_points += 1
                    elif other != object:
                        b_points += 1
                best_match = signature_option if (a_points > b_points) else best_match
                # print("BEST MATCH:", best_match)
            elif points > best_points:
                best_points = points
                best_match = signature_option
        # print("BEST MATCH FINAL:", best_match)
        # assure 'best_match' isn't conflicting
        if best_match not in self._uniques[self.function_name]:
            return None
        return self._uniques[self.function_name][best_match]


if __name__ == "__main__":
    # Vec2 = tuple

    # @overload
    # def f(vec2: Vec2, num: float) -> Vec2:
    #     return (vec2[0] * num, vec2[1] * num)
    
    # @overload
    # def f(vec2: Vec2, other: Vec2) -> Vec2:
    #     return (vec2[0] + other[1])

    # print("- - -")
    # a = (2, 3)
    # b = (5, 7)
    # c = 2.0
    # print("A:", a)
    # print("A:", b)
    # print(f(a, b))
    # print(f(a, c))

    # @overload
    # def f(a: int, b: Any):
    #     print("B")
    #     return a + b

    # @overload
    # def f(a: int, b: int):
    #     print("A")
    #     return a + b
    
    # print(f(2, 3))

    @overload
    def f(a: int, b: int) -> int:
        print("A")
        return a + b
    
    @overload
    def f(a: str, b: str) -> str:
        print("B")
        return a + b
    
    @overload
    def f(a: Any, b: int) -> str:
        print("C")
        return a * b

    print(overload._uniques)
    print("- - -")
    print(f(2, 5))
    print(f([2], 3))
    print(f("2", "3"))
