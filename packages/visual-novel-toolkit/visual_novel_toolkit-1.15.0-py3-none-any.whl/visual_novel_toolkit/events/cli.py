# mypy: disable-error-code = misc
from typer import echo
from typer import Exit
from typer import Typer

from .exceptions import EventError
from .plot import plot_events


events = Typer()


@events.command()
def plot(check: bool = False) -> None:
    try:
        if plot_events(check):
            raise Exit(code=1)
    except EventError as error:
        echo(error)
        raise Exit(code=1)
