import asyncio
import logging
import shlex
import html
from prompt_toolkit.formatted_text import HTML

from .StreamClient import StreamClient

_log = logging.getLogger("katcpcli.CommandDispatcher")


class CommandDispatcher:
    """
    Dispatch a command-line to the appropriate method.
    """

    def __init__(self, output_stream, log_stream):
        self.commands = {
            "connect": self.connect,
            "reconnect": self.reconnect,
            "log_inform": self.log_inform,
        }
        self.log_stream = log_stream
        self.output_stream = output_stream
        self.katcpclient = None
        self.completion_set = set(self.commands.keys())
        self.supressed_logs = 0
        self.running_tasks = set()

    async def __call__(self, line):
        """
        Act on a prompt line.
        """
        try:
            line = shlex.split(line)
        except ValueError as E:
            self.output_stream(
                HTML(
                    f' <style fg="ansired"> Error</style> processing line:<b> {html.escape(line)}</b> - {E}'
                )
            )
            return

        if not line:
            return
        cmd = line[0]
        args = line[1:]
        if cmd.startswith("?"):
            cmd = "katcpcmd"
            args.insert(0, line[0][1:])

        try:
            task = asyncio.create_task(self.commands[cmd](*args))
            self.running_tasks.add(task)
            task.add_done_callback(self.running_tasks.discard)
        except KeyError:
            self.output_stream(
                HTML(
                    f' <style fg="ansired"> Error</style> Unknown command:<b> {html.escape(cmd)}</b>'
                )
            )
        except TypeError as E:
            self.output_stream(E)

    async def update_command_completion(self):
        """
        Update command completion set
        """
        # remove requests from completion list
        to_remove = set()
        for s in self.completion_set:
            if s.startswith("?"):
                to_remove.add(s)
        self.completion_set -= to_remove

        requests = await self.katcpclient.get_requests()
        for s in requests:
            self.completion_set.add(f"?{s}")

    async def connect(self, host, port=None):
        """
        Connect to host:port
        """
        if port is None:
            try:
                host, port = host.split(":")
            except ValueError:
                self.output_stream(
                    HTML(
                        '<style fg="ansired"> Error</style> Expecting host:port or host port'
                    )
                )
                return

        if self.katcpclient:
            self.output_stream(
                f"Closing connection to {self.katcpclient.host}:{self.katcpclient.port}"
            )
            self.katcpclient.close()
            await self.katcpclient.wait_closed()
            self.katcpclient = None
        self.output_stream(f"Connecting to {host}:{port} ...")
        self.katcpclient = StreamClient(
            self.output_stream, self.log_stream, host, port
        )
        await self.katcpclient.wait_connected()
        await self.update_command_completion()
        self.output_stream(f"Connection to {host}:{port} established.")

        self.commands["katcpcmd"] = self.katcpclient.handle_request
        self.supressed_logs = 0

    async def reconnect(self):
        """
        Reconnect to the previous host
        """
        if self.katcpclient:
            self.output_stream("Reconnecting")
            await self.connect(self.katcpclient.host, self.katcpclient.port)
        else:
            self.output_stream("No connection to reconnect to!")

    async def log_inform(self, args):
        """
        Toggle log inform handling.
        """
        if args == "enabled":
            self.katcpclient.log_stream = self.log_stream
        elif args == "disabled":
            self.katcpclient.log_stream = self._log_counter
        else:
            self.output_stream("Requires one of [enabled/disabled] as arguement")
            return

        self.output_stream(f"Showing log informs is now {args}")

    def _log_counter(self, line):  # pylint: disable=unused-argument
        self.supressed_logs += 1
