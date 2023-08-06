import toml
from .levdict_base import LevDict
from pathlib import Path


class LevDictToml(LevDict):
    """Handles toml files using LevDict functionality"""

    def __init__(self, toml_file: str | Path = "") -> None:
        """Constructor: you supply a filename, a Path object or none"""

        super().__init__()
        if toml_file:
            self.load(toml_file)

    def load(self, toml_file: str | Path, clear: bool = False) -> None:
        """Loads a toml file into the class, allowing it to use dot notation"""

        if isinstance(toml_file, str):
            toml_file = Path(toml_file)
        elif not isinstance(toml_file, Path):
            raise TypeError("Bad argument toml_file: expected str or Path")

        data = toml.load(toml_file)
        self.from_dict(data, clear)

    def dump(self, toml_file: str | Path, force: bool = False, **kwargs) -> None:
        """
        Saves the class dict content to a toml file

        Arguments:
        file:   The filename string or a Path object where the dict will be saved.
        force:  If False (default value) an error will be given if the file exists.
        kwargs: Arguments to the toml.dump() command (see toml documentation for details)
        """

        if isinstance(toml_file, str):
            toml_file = Path(toml_file)
        elif not isinstance(toml_file, Path):
            raise TypeError("Bad argument toml_file: expected str or Path")

        if toml_file.exists() and not force:
            raise ValueError("Attempt to overwrite file without 'force' flag")

        with toml_file.open("w") as tomh:
            toml.dump(self.as_dict(), tomh, **kwargs)
