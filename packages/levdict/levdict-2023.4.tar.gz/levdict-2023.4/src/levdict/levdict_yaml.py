import yaml
from yaml.loader import SafeLoader
from .levdict_base import LevDict
from pathlib import Path


class LevDictYaml(LevDict):
    """Handles yaml files using LevDict functionality"""

    def __init__(self, yaml_file: str | Path = "") -> None:
        """Constructor: you supply a filename, a Path object or none"""

        super().__init__()
        if yaml_file:
            self.load(yaml_file)

    def load(self, yaml_file: str | Path, clear: bool = False) -> None:
        """Loads a yaml file into the class, allowing it to use dot notation"""

        if isinstance(yaml_file, str):
            yaml_file = Path(yaml_file)
        elif not isinstance(yaml_file, Path):
            raise TypeError("Bad argument yaml_file: expected str or Path")

        with yaml_file.open("r") as yh:
            data = yaml.load(yh, Loader=SafeLoader)

        self.from_dict(data, clear)

    def dump(self, yaml_file: str | Path, force: bool = False, **kwargs) -> None:
        """
        Saves the class dict content to a yaml file

        Arguments:
        file:   The filename string or a Path object where the dict will be saved.
        force:  If False (default value) an error will be given if the file exists.
        kwargs: Arguments to the yaml.dump() command (see yaml documentation for details)
        """

        if isinstance(yaml_file, str):
            yaml_file = Path(yaml_file)
        elif not isinstance(yaml_file, Path):
            raise TypeError("Bad argument toml_file: expected str or Path")

        if yaml_file.exists() and not force:
            raise ValueError("Attempt to overwrite file without 'force' flag")

        with yaml_file.open("w") as yh:
            yaml.dump(self.as_dict(), yh, **kwargs)
