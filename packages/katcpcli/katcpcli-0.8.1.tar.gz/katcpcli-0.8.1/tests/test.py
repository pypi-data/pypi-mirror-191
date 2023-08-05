
import unittest
import unittest.mock
import sys
import socket
import asyncio
import time
import tempfile
import logging
import os

from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.input import create_pipe_input
from prompt_toolkit.application import create_app_session
from prompt_toolkit.shortcuts import print_formatted_text
from prompt_toolkit.output import DummyOutput

import aiokatcp
from katcpcli.StreamClient import sensor_status_format
from katcpcli.CommandDispatcher import CommandDispatcher
from katcpcli import app, config, main

sys.path.insert(0, '..')


class MockServer(aiokatcp.DeviceServer):
    VERSION = "mock-1.0"
    BUILD_STATE = 'mock-1.0'

    def __init__(self):
        with socket.socket() as sock:
            sock.bind(('', 0))
            self.port = sock.getsockname()[1]

        aiokatcp.DeviceServer.__init__(self, '127.0.0.1', self.port)
        self.mock = unittest.mock.Mock()

    async def request_echo(self, ctx, line):
        """
        foo doc
        """
        self.mock.echo(line)
        return line

    async def request_sendloginform(self, ctx, msg):
        """
        Send a log-inform
        """
        self.mass_inform("log", "info", time.time(), f"log inform at info level with {msg.decode('ascii')}")




class SimpleBuffer:
    def __init__(self):
        self.data = []

    def __call__(self, line):
        self.data.append(line)



class TestFormattingHelpers(unittest.TestCase):
    def test_sensor_status_format(self):
        """
        a valid string should be returned for all posible status values.
        """
        for v in aiokatcp.Sensor.Status:
            self.assertTrue(isinstance(sensor_status_format(v), str), msg=f'Error with {v}')

        for v in aiokatcp.Sensor.Status:
            self.assertTrue(isinstance(sensor_status_format(v.value), str), msg=f'Error with {v}')

        for v in aiokatcp.Sensor.Status:
            self.assertTrue(isinstance(sensor_status_format(v.name), str), msg=f'Error with {v}')


class TestCommandDispatcher(unittest.IsolatedAsyncioTestCase):
    def setUp(self):

        self.ostream = SimpleBuffer()
        self.lstream = SimpleBuffer()

        self.server = MockServer()
        self.dispatcher = CommandDispatcher(self.ostream, self.lstream)

    async def asyncTearDown(self):
        await self.server.stop()

    async def asyncSetUp(self):
        await self.server.start()
        await self.dispatcher.connect('127.0.0.1', self.server.port)

    async def testCompletionAfterConnect(self):
        """
        After connect the compeltion set should contain the requests of the server.
        """
        self.assertIn('?echo', self.dispatcher.completion_set)

    async def testRequestDispatch(self):
        await self.dispatcher("?echo foo")
        await asyncio.sleep(.1)
        self.server.mock.echo.assert_called_once()
        # The echo line should be the end of the last line in the ostream
        self.assertTrue(self.ostream.data[-1].value.endswith('foo'))

    async def testUnescapedHTMLCommand(self):
        # special characters should not raise an exception but onlyc reate an
        # error
        await self.dispatcher("<")
        await self.dispatcher(">")

    async def testSingleQuotationMarks(self):
        # single quotation amrks should not raise an exception but only an
        # error message
        await self.dispatcher("'")
        await self.dispatcher('"')


    async def testLogInformToggle(self):
        # Log informs should be supressed
        await self.dispatcher.log_inform('enabled')
        self.assertEqual(self.dispatcher.supressed_logs, 0)
        await self.dispatcher("?sendloginform foo")
        await asyncio.sleep(.1)
        self.assertTrue(self.lstream.data[-1].value.endswith('foo'))
        self.assertIn("log inform at info level", self.lstream.data[-1].value)

        await self.dispatcher.log_inform('disabled')
        await self.dispatcher("?sendloginform bar")
        await asyncio.sleep(.1)
        self.assertFalse(self.lstream.data[-1].value.endswith('bar'))
        self.assertEqual(self.dispatcher.supressed_logs, 1)


    async def testConnect(self):
        "Connect should work with host:port and host port"
        await self.dispatcher.connect('127.0.0.1', self.server.port)
        self.assertTrue(self.ostream.data[-1].endswith('established.'))

        self.ostream.data.clear()
        await self.dispatcher.connect(f'127.0.0.1:{self.server.port}')
        self.assertTrue(self.ostream.data[-1].endswith('established.'))

        # invalid connect string should give error message and no exception
        await self.dispatcher.connect(f'127.0.0.1')
        self.assertIn('Error', self.ostream.data[-1].value)


class TestConfig(unittest.TestCase):
    def test_non_existin_config_file(self):
        # should just ignore this and return default config
        cfg = config.from_file('/path/to/non/existing_file_foo_bar')
        self.assertEqual(len(cfg['favorites']), 0)

    def test_existing_file_favourites(self):
        with tempfile.NamedTemporaryFile(mode='w') as f:
            f.write("""
            [favorites]
            foo=bar
            spam=eggs
            """)
            f.flush()
            cfg = config.from_file(f.name)

            self.assertEqual(cfg['favorites']['foo'], 'bar')
            self.assertEqual(cfg['favorites']['spam'], 'eggs')

    def testDevice2HostPort(self):

        favorites = {'foo': 'bar:123'}

        host, port = main.device2hostport('spam:1234', favorites)
        self.assertEqual(host, 'spam')
        self.assertEqual(port, '1234')

        host, port = main.device2hostport('ham', favorites)
        self.assertEqual(host, 'ham')

        host, port = main.device2hostport('foo', favorites)
        self.assertEqual(host, 'bar')
        self.assertEqual(port, '123')


if __name__ == "__main__":
    import coloredlogs

    logging.getLogger().addHandler(logging.NullHandler())
    log = logging.getLogger('katcpcli')
    if os.environ.get('VERBOSE', '').upper() == 'TRUE':
        log.setLevel(logging.DEBUG)
        level = logging.DEBUG
    else:
        log.setLevel(logging.INFO)
        level = logging.CRITICAL

    coloredlogs.install(
        fmt=("[ %(levelname)s - %(asctime)s - %(name)s "
             "- %(filename)s:%(lineno)s] %(message)s"),
        level=level,            # We manage the log level via the logger, not the handler
        logger=log)

    unittest.main()


