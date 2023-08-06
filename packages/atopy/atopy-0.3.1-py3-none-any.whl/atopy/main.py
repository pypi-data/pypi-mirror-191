import typer
from loguru import logger

app = typer.Typer()


@app.command()
def debug(msg: str) -> None:
    logger.debug(f"{msg}")


@app.command()
def info(msg: str) -> None:
    logger.info(f"{msg}")


@app.command()
def error(msg: str) -> None:
    logger.error(f"{msg}")


if __name__ == "__main__":
    app()
