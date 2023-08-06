import json
from .levdict_base import LevDict
from pathlib import Path


class LevDictJson(LevDict):
    """Handles json files using LevDict functionality"""

    def __init__(self, json_file: str | Path = "") -> None:
        """Constructor: you supply a filename, a Path object or none"""

        super().__init__()
        if json_file:
            self.load(json_file)

    def load(self, json_file: str | Path, clear: bool = False) -> None:
        """Loads a json file into the class, allowing it to use dot notation"""

        if isinstance(json_file, str):
            json_file = Path(json_file)
        elif not isinstance(json_file, Path):
            raise TypeError("Bad argument json_file: expected str or Path")

        with json_file.open("r") as jh:
            data: dict = json.load(jh)
            if not isinstance(data, dict):
                raise ValueError("*** Not a Dict !!! ***")

        self.from_dict(data, clear)

    def dump(self, json_file: str | Path, force: bool = False, **kwargs) -> None:
        """
        Saves the class dict content to a json file

        Arguments:
        file:   The filename string or a Path object where the dict will be saved.
        force:  If False (default value) an error will be given if the file exists.
        kwargs: Arguments to the json.dump() command (see json documentation for details)
        """

        if isinstance(json_file, str):
            json_file = Path(json_file)
        elif not isinstance(json_file, Path):
            raise TypeError("Bad argument json_file: expected str or Path")

        if json_file.exists() and not force:
            raise ValueError("Attempt to overwrite file without 'force' flag")

        with json_file.open("w") as jh:
            json.dump(self.as_dict(), jh, **kwargs)
