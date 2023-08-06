"""
More advanced usage of LevDict by the derived class LevDictToml.
We instantiate the class and then use the 'load' method to load from a config file.
This class derives directly from LevDict.
It can be used as a normal dict, with a dot notation, or a combimation of both.
"""
from levdict import LevDictToml


def main() -> None:
    ini = LevDictToml()
    ini.load("example2.ini")

    name = ini.user.name  # dot notation
    email = ini["user"].email  # mixed dict and dot notation

    print(f"Hi {name}, I will send you a document to {email}!")


if __name__ == "__main__":
    main()
