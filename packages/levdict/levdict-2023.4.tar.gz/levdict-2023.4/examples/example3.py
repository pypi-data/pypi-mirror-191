"""
More advanced usage of LevDict by the derived class LevDictToml.
We instantiate the class and then use the 'load' method to load from a config file.
In this example we modify the dict and save it back to the toml file
"""
from levdict import LevDictToml


def main() -> None:
    ini = LevDictToml()
    ini.load("example3.toml")

    name: str = ini.user.name  # dot notation
    email: str = ini["user"].email  # mixed dict and dot notation

    newmail = email.replace("somemail", "gmail")

    ini.user.email = newmail

    ini.dump("example3_mod.toml", force=True)

    print(f"{email} has been replaced by {newmail}!")


if __name__ == "__main__":
    main()
