"""
Basic usage of LevDict.
We instantiate the class passing a dict.
It can be used as a normal dict, with a dot notation, or a combimation of both.
"""
from levdict import LevDict

d = {"user": {"name": "John Doe", "email": "john.d@somemail.com"}}


def main() -> None:
    mydict = LevDict(d)

    name = mydict.user.name  # dot notation
    email = mydict["user"].email  # mixed dict and dot notation

    print(f"Hi {name}, I will send you a document to {email}!")


if __name__ == "__main__":
    main()
