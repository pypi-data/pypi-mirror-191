import typer
from rich.console import Console
from pathlib import Path
import shutil
import os
from enum import Enum
import toml

app = typer.Typer(add_completion=False)


def _get_project_name() -> str:
    data = toml.load("pyproject.toml")
    return data["project"]["name"]


@app.command(name="build")
def cmd_build() -> None:
    cwd: Path = Path().cwd()
    shutil.rmtree(cwd / "dist")
    os.system("python -m build")


@app.command(name="test")
def cmd_test() -> None:
    os.system("python -m unittest tests")


@app.command(name="format")
def cmd_format() -> None:
    c = Console()
    for folder in ["examples", "src", "tests", "scripts"]:
        c.print(f"\nFormatting [yellow]{folder}[/yellow]")
        os.system(f"python -m black {folder}")


class EUploadChoice(str, Enum):
    prod = "prod"
    test = "test"


@app.command(name="upload")
def cmd_upload(
    choice: EUploadChoice = typer.Argument(..., help="Uploads to PyPi or to Test PyPi")
) -> None:
    repo = "dist/*"
    if choice.value == "test":
        repo = "--repository testpypi " + repo

    os.system(f"python -m twine upload {repo}")


class EInstallChoice(str, Enum):
    prod = "prod"
    test = "test"
    dev = "dev"


@app.command(name="install")
def cmd_install(
    choice: EInstallChoice = typer.Argument(..., help="Installs the module")
) -> None:
    module = _get_project_name().lower()
    if choice.value == "test":
        flag = "-i https://test.pypi.org/project/ "
    elif choice.value == "prod":
        flag = ""
    else:
        flag = "--editable"
        module = "."

    os.system(f"python -m pip install {flag} {module}")


if __name__ == "__main__":
    exit(app())
