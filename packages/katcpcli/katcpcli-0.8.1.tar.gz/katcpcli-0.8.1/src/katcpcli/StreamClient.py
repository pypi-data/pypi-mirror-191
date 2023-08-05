import logging
import time
import datetime
import html
import enum

import aiokatcp
from prompt_toolkit.formatted_text import HTML


_log = logging.getLogger("katcpcli.StreamClient")


def sensor_status_format(name):
    """
    Format sensor status value.
    """
    if isinstance(name, enum.Enum):
        name = name.name
    elif isinstance(name, int):
        name = aiokatcp.Sensor.Status(name).name


    colors = {
        "UNKNOWN": "ansiblue",
        "NOMINAL": "ansigreen",
        "WARN": "ansiyellow",
        "ERROR": "ansired",
        "FAILURE": "ansired",
        "UNREACHABLE": "anisred",
        "INACTIVE": "cyan",
    }

    col = colors.get(name)
    if col:
        res = f'<style fg="{col}">{name:10}</style>'
    else:
        res = name
    _log.debug("Formatted status name: %s", res)
    return res


class StreamClient(aiokatcp.client.Client):
    """
    KATCP client that creates output lines from the replies and writes them to
    different streams for log messages and default output.
    """

    def __init__(self, output_stream, log_stream, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output_stream = output_stream
        self.log_stream = log_stream

    def _decode(self, values):
        return [html.escape(v.decode("ascii")) for v in values]

    def unhandled_inform(self, msg: aiokatcp.core.Message) -> None:
        """Deal with unhandled informs"""
        args = " ".join(self._decode(msg.arguments))
        self.output_stream(HTML(f"unhandled-inform:\n#{msg.name} {args}"))

    def inform_client_connected(self, *args):
        """Deal with connect informs"""
        msg = " ".join(self._decode(args))
        self.log_stream(HTML(f"{time.ctime()} Client connected: {msg}"))

    def inform_client_disconnected(self, *args):
        """Deal with disconnect informs"""
        msg = " ".join(self._decode(args))
        self.log_stream(HTML(f"{time.ctime()} Client disconnected: {msg}"))

    def inform_log(self, *args):
        """Deal with connect informs"""
        msg = " ".join(self._decode(args))
        self.log_stream(HTML(f"{msg}"))

    def _format_sensor_list(self, *args):
        """Deal with sensor values"""
        arguments = self._decode(args)
        _log.debug("Arguments for format: %s", arguments)
        if len(arguments) >= 5:
            if arguments[4].startswith("iVBORw0KGgo"):
                data = "Some base64 encoded png image (hidden)"
            else:
                data = arguments[4]

            output = "{} {}  {:30}   {}".format(
                datetime.datetime.fromtimestamp(float(arguments[0])).isoformat(),
                sensor_status_format(arguments[3].upper()),
                arguments[2],
                data,
            )
        else:
            output = " ".join(arguments)
        return output.rstrip()
        self.output_stream(HTML(output))

    def inform_sensor_value(self, *args):
        """Deal with sensor values"""
        output = self._format_sensor_list(*args)
        self.output_stream(HTML(output))

    def inform_sensor_status(self, *args):
        """Deal with sensor values"""
        output = self._format_sensor_list(*args)
        self.log_stream(HTML(output))

    def inform_sensor_list(self, *args):
        """Deal with sensor list"""
        if len(args) > 1:
            R = "; ".join(self._decode(args[1:]))
        else:
            R = ""
        output = HTML(" - {}\n              {}".format(self._decode((args[0],))[0], R))
        self.output_stream(output)

    def inform_help(self, *args):
        """Pretty print help"""
        if len(args) > 1:
            R = "; ".join(self._decode(args[1:]))
        else:
            R = ""
        output = HTML(" - {}\n              {}".format(self._decode((args[0],))[0], R))
        self.output_stream(output)

    def print_command_reply(self, cmd, rv, res=""):
        """
        Print reply of a command.
        """
        if rv == "ok":
            col = "ansigreen"
        else:
            col = "ansired"
        self.output_stream(HTML(f'<b>!{cmd}</b> <style fg="{col}">{rv}</style> {res}'))

    async def handle_request(self, *args):
        """
        handle request reply
        """
        _log.debug("handle request called with args %s", args)
        if not args:
            return
        cmd = args[0]
        try:
            reply, informs = await self.request(cmd, *args[1:])
            for inform in informs:
                self.handle_inform(inform)
            rv = " ".join(self._decode(reply))
            self.print_command_reply(cmd, "ok", rv)
        except aiokatcp.connection.FailReply as E:
            self.print_command_reply(cmd, "fail", E)
        except aiokatcp.connection.InvalidReply as E:
            self.print_command_reply(cmd, "invalid", E)
        except BrokenPipeError:
            self.print_command_reply(cmd, "not connected!")
        except ConnectionResetError:
            self.print_command_reply(cmd, "connection to server lost!")
        except Exception as E:  # pylint: disable=broad-except
            _log.error("Unhandled exeption during request handling")
            _log.exception(E)
            self.print_command_reply(cmd, "Unexpected exception during handling of command!")

    async def get_requests(self):
        """
        Get requests for device
        """
        requests = set()
        try:
            _, informs = await self.request("help")
            for inform in informs:
                requests.add(inform.arguments[0].decode("ascii"))
        except Exception as E:  # pylint: disable=broad-except
            _log.error("Error during command retrival")
            _log.exception(E)
        return requests

    def _warn_failed_connect(self, exc: Exception) -> None:
        self.logger.debug("Failed to connect to %s:%s: %s", self.host, self.port, exc)
