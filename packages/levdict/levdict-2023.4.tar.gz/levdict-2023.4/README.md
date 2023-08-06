# levdict

This module allows to handle dictionaries keys as attributes.
It has four classes:

- ***LevDict***: The base class, it acts as a dictionary but with the added feature of treating
consists of a main class LevDict, which allows to treat dictionaries as attributes.
- ***LevDictJson***: Derived from LevDict, reads and writes ***json*** files
- ***LevDictToml***: Derived from LevDict, reads and writes ***toml*** files (depends on toml)
- ***LevDictYaml***: Derived from LevDict, reads and writes ***yaml*** files (depends on pyyaml)

and three derived classes that allow using respectively toml, json and yaml for configuration purposes.

## Installation

The module is currently in production.

    python -m pip install levdict

## LevDict basic usage

    d = LevDict(name="John", surname="Doe")
    surname = d.surname
    surname = d["surname"]
    d.name = "Peter"
    d.update(name="Albert")
    d.surname="Hall"

More in the examples folder.

## Project Tree Structure

        .
    ├── LICENSE
    ├── Makefile
    ├── Pipfile
    ├── Pipfile.lock
    ├── README.md
    ├── examples
    │   ├── example1.py
    │   ├── example2.ini
    │   ├── example2.py
    │   ├── example3.py
    │   ├── example3.toml
    │   ├── example3_mod.toml
    │   ├── example4.json
    │   └── example4.py
    ├── pyproject.toml
    ├── scripts
    │   └── levmake.py
    ├── src
    │   └── levdict
    │       ├── __init__.py
    │       ├── levdict_base.py
    │       ├── levdict_json.py
    │       ├── levdict_toml.py
    │       └── levdict_yaml.py
    └── tests
        ├── __init__.py
        ├── examples
        │   ├── example.toml
        │   ├── example1.json
        │   ├── example1.toml
        │   ├── example1.yaml
        │   └── example1_mod.toml
        ├── test_basic.py
        └── test_levdict.py

    7 directories, 28 files
