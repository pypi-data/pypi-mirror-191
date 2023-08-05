# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/005_FastKafkaServer.ipynb.

# %% auto 0
__all__ = ['logger', 'generate_app_in_tmp', 'ServerProcess', 'run_fastkafka_server_process', 'terminate_asyncio_process',
           'run_fastkafka_server', 'run_in_process']

# %% ../nbs/005_FastKafkaServer.ipynb 1
import importlib
import sys
import asyncio
from typing import *
from contextlib import contextmanager
from pathlib import Path
import threading
import signal
from contextlib import ExitStack, contextmanager
from tempfile import TemporaryDirectory


import multiprocessing
from fastcore.meta import delegates
from fastcore.basics import patch
import typer
import asyncer

from .application import FastKafka
from .testing import change_dir
from ._components.helpers import _import_from_string, generate_app_src
from ._components.logger import get_logger

# %% ../nbs/005_FastKafkaServer.ipynb 5
logger = get_logger(__name__)

# %% ../nbs/005_FastKafkaServer.ipynb 8
@contextmanager
def generate_app_in_tmp() -> Generator[str, None, None]:
    with TemporaryDirectory() as d:
        src_path = Path(d) / "main.py"
        generate_app_src(src_path)
        with change_dir(d):
            import_str = f"{src_path.stem}:kafka_app"
            yield import_str

# %% ../nbs/005_FastKafkaServer.ipynb 9
class ServerProcess:
    def __init__(self, app: str):
        self.app = app
        self.should_exit = False

    def run(self) -> None:
        return asyncio.run(self._serve())

    async def _serve(self) -> None:
        self._install_signal_handlers()

        self.application = _import_from_string(self.app)

        async with self.application:
            await self._main_loop()

    def _install_signal_handlers(self) -> None:
        if threading.current_thread() is not threading.main_thread():
            raise RuntimeError()

        loop = asyncio.get_event_loop()

        HANDLED_SIGNALS = (
            signal.SIGINT,  # Unix signal 2. Sent by Ctrl+C.
            signal.SIGTERM,  # Unix signal 15. Sent by `kill <pid>`.
        )

        def handle_exit(sig: int) -> None:
            self.should_exit = True

        for sig in HANDLED_SIGNALS:
            loop.add_signal_handler(sig, handle_exit, sig)

    async def _main_loop(self) -> None:
        while not self.should_exit:
            await asyncio.sleep(0.1)

# %% ../nbs/005_FastKafkaServer.ipynb 10
_app = typer.Typer()


@_app.command()
def run_fastkafka_server_process(
    app: str = typer.Argument(
        ...,
        help="input in the form of 'path:app', where **path** is the path to a python file and **app** is an object of type **FastKafka**.",
    )
) -> None:
    ServerProcess(app).run()

# %% ../nbs/005_FastKafkaServer.ipynb 12
async def terminate_asyncio_process(p: asyncio.subprocess.Process) -> None:
    logger.info(f"terminate_asyncio_process(): Terminating the process {p.pid}...")
    # Check if SIGINT already propagated to process
    try:
        await asyncio.wait_for(p.wait(), 1)
        logger.info(
            f"terminate_asyncio_process(): Process {p.pid} was already terminated."
        )
        return
    except asyncio.TimeoutError:
        pass

    for i in range(3):
        p.terminate()
        try:
            await asyncio.wait_for(p.wait(), 10)
            logger.info(f"terminate_asyncio_process(): Process {p.pid} terminated.")
            return
        except asyncio.TimeoutError:
            logger.warning(
                f"terminate_asyncio_process(): Process {p.pid} not terminated, retrying..."
            )

    logger.warning(f"Killing the process {p.pid}...")
    p.kill()
    await p.wait()
    logger.warning(f"terminate_asyncio_process(): Process {p.pid} killed!")

# %% ../nbs/005_FastKafkaServer.ipynb 14
async def run_fastkafka_server(num_workers: int, app: str) -> None:
    loop = asyncio.get_event_loop()

    HANDLED_SIGNALS = (
        signal.SIGINT,  # Unix signal 2. Sent by Ctrl+C.
        signal.SIGTERM,  # Unix signal 15. Sent by `kill <pid>`.
    )

    d = {"should_exit": False}

    def handle_exit(sig: int, d: Dict[str, bool] = d) -> None:
        d["should_exit"] = True

    for sig in HANDLED_SIGNALS:
        loop.add_signal_handler(sig, handle_exit, sig)

    async with asyncer.create_task_group() as tg:
        tasks = [
            tg.soonify(asyncio.create_subprocess_exec)(
                "run_fastkafka_server_process",
                app,
                stdout=asyncio.subprocess.PIPE,
                stdin=asyncio.subprocess.PIPE,
            )
            for i in range(num_workers)
        ]

    procs = [task.value for task in tasks]

    async def log_output(
        output: Optional[asyncio.StreamReader], pid: int, d: Dict[str, bool] = d
    ) -> None:
        if output is None:
            raise RuntimeError("Expected StreamReader, got None. Is stdout piped?")
        while not output.at_eof():
            outs = await output.readline()
            if outs != b"":
                typer.echo(f"[{pid:03d}]: " + outs.decode("utf-8"), nl=False)

    async with asyncer.create_task_group() as tg:
        for proc in procs:
            tg.soonify(log_output)(proc.stdout, proc.pid)

        while not d["should_exit"]:
            await asyncio.sleep(0.2)

        typer.echo("Starting process cleanup, this may take a few seconds...")
        for proc in procs:
            tg.soonify(terminate_asyncio_process)(proc)

    for proc in procs:
        output, _ = await proc.communicate()
        if output:
            typer.echo(f"[{proc.pid:03d}]: " + output.decode("utf-8"), nl=False)

    returncodes = [proc.returncode for proc in procs]
    if not returncodes == [0] * len(procs):
        typer.secho(
            f"Return codes are not all zero: {returncodes}",
            err=True,
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

# %% ../nbs/005_FastKafkaServer.ipynb 15
@contextmanager
def run_in_process(
    target: Callable[..., Any]
) -> Generator[multiprocessing.Process, None, None]:
    p = multiprocessing.Process(target=target)
    try:
        p.start()
        yield p
    except Exception as e:
        print(f"Exception raised {e=}")
    finally:
        p.terminate()
        p.join()
