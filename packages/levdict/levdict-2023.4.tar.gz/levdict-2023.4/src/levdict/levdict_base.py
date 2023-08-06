from typing import Any

# Forward declarations


class LevDict:
    pass


def _transform_list(data: list) -> list:
    pass


def _transform_tuple(data: tuple) -> tuple:
    pass


def _transform_list(data: list) -> list:
    """
    Returns the modified list with:
    - a LevDict in case of a dict element
    - a transformed tuple
    - a recursive call to itself in case of a list
    - the item if none of the above
    """
    result = []

    for item in data:
        if isinstance(item, dict):
            result.append(LevDict(item))
        elif isinstance(item, list):
            result.append(_transform_list(item))
        elif isinstance(item, tuple):
            result.append(_transform_tuple(item))
        else:
            result.append(item)
    return result


def _transform_tuple(data: tuple) -> tuple:
    """
    Returns the modified tuple with:
    - a LevDict in case of a dict element
    - a transformed list
    - a recursive call to itself in case of a tuple
    - the item if none of the above
    """
    result = ()

    for item in data:
        if isinstance(item, dict):
            result = (*result, LevDict(item))
        elif isinstance(item, list):
            result = (*result, _transform_list(item))
        elif isinstance(item, tuple):
            result = (*result, _transform_tuple(item))
        else:
            result = (*result, item)
    return result


def _transform_dict(data: dict) -> dict:
    """
    Returns the modified dict with:
    - a LevDict in case of a dict element
    - a transformed list
    - a transformed tuple
    - the item if none of the above
    """

    # If data is an instance of LevDict, it's also an instance of dict so trap it here!
    if isinstance(data, LevDict):
        return data

    result = {}
    for key, val in data.items():
        if isinstance(val, dict):
            result[key] = LevDict(val)
        elif isinstance(val, list):
            result[key] = _transform_list(val)
        elif isinstance(val, tuple):
            result[key] = _transform_tuple(val)
        else:
            result[key] = val
    return result


# --------------------------------------------------------------------------------------


def _normalize_list(data: list) -> list:
    pass


def _normalize_tuple(data: tuple) -> tuple:
    pass


def _normalize_list(data: list) -> list:
    """
    Returns the modified list with:
    - a dict in case of a LevDict element
    - a transformed tuple
    - a recursive call to itself in case of a list
    - the item if none of the above
    """
    result = []

    for item in data:
        if isinstance(item, LevDict):
            result.append(item.as_dict())
        elif isinstance(item, list):
            result.append(_normalize_list(item))
        elif isinstance(item, tuple):
            result.append(_normalize_tuple(item))
        else:
            result.append(item)
    return result


def _normalize_tuple(data: tuple) -> tuple:
    """
    Returns the modified tuple with:
    - a dict in case of a LevDict element
    - a transformed list
    - a recursive call to itself in case of a tuple
    - the item if none of the above
    """
    result = ()

    for item in data:
        if isinstance(item, LevDict):
            result = (*result, item.as_dict())
        elif isinstance(item, list):
            result = (*result, _normalize_list(item))
        elif isinstance(item, tuple):
            result = (*result, _normalize_tuple(item))
        else:
            result = (*result, item)
    return result


def _normalize_dict(data: dict) -> dict:
    """
    Returns the modified dict with:
    - a LevDict in case of a dict element
    - a transformed list
    - a transformed tuple
    - the item if none of the above
    """

    # If data is an instance of dict and NOT LevDict, trap it here!
    if isinstance(data, dict) and not isinstance(data, LevDict):
        return data

    result = {}
    for key, val in data.items():
        if isinstance(val, LevDict):
            result[key] = val.as_dict()
        elif isinstance(val, list):
            result[key] = _normalize_list(val)
        elif isinstance(val, tuple):
            result[key] = _normalize_tuple(val)
        else:
            result[key] = val
    return result


# ------------------------------------------------------------------------------


class LevDict(dict):
    """Class that implements an attribute oriented dictionary"""

    def __init__(self, the_dict: dict = {}, /, **kwargs) -> None:
        """Constructor: accepts a dict or no arguments"""
        super().__init__()
        if kwargs:
            the_dict.update(**kwargs)
        self.from_dict(data=the_dict)

    def from_dict(self, data: dict, clear: bool = False) -> None:
        """
        Loads itself from a dictionary

        Arguments:
        data:  The dictionary to load into the class
        clear: Whether to clear the data before assignment or not
        """
        if not isinstance(data, dict):
            raise ValueError("Bad parameter, not a dict!")

        if data:
            if clear:
                self.clear()

            data = _transform_dict(data)
            self.update(**data)

    def as_dict(self) -> None:
        """Returns the class data as a plain dict"""

        return _normalize_dict(self)

    def __getattr__(self, __attr: str) -> Any:
        """Implements the dot notation to retrieve an item"""
        if __attr in self:
            return self[__attr]
        else:
            raise AttributeError(f"No such attribute: {__attr}")

    def __setattr__(self, __attr: str, __value: Any) -> None:
        """Implements the dot notation to set an item"""
        if isinstance(__value, dict):
            __value = LevDict(__value)
        self[__attr] = __value

    def __delattr__(self, __attr: str) -> None:
        """Implements the dot notation to delete an item"""
        if __attr in self:
            del self[__attr]
        else:
            raise AttributeError(f"No such attribute: {__attr}")
