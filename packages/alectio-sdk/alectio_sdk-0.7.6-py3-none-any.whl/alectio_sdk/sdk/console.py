import typer


class MainConsole:
    def __init__(self) -> None:
        pass

    def error(self, msg: str):
        msg = "❌  " + msg + "\n"
        message = typer.style(msg, fg=typer.colors.RED)
        typer.echo(message)

    def success(self, msg: str):
        msg = "✅  " + msg + "\n"
        message = typer.style(msg, fg=typer.colors.GREEN)
        typer.echo(message)

    def info(self, msg: str):
        msg = "ℹ️  " + msg + "\n"
        message = typer.style(msg, fg=typer.colors.MAGENTA)
        typer.echo(message)

    def warning(self, msg: str):
        msg = "⚠️  " + msg + "\n"
        message = typer.style(msg, fg=typer.colors.YELLOW)
        typer.echo(message)

    def message(self, msg: str):
        message = typer.style(msg, fg=typer.colors.CYAN)
        typer.echo(message)
