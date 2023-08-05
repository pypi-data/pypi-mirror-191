#!/usr/bin/python3
"""
KATCPcli - a text client for KATCP devices.
"""

import asyncio
import logging
import sys
import argparse
import os

import katcpcli.app
import katcpcli.config

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,
    format="%(asctime)s - %(name)s - %(filename)s:"
    "%(lineno)s - %(levelname)s - %(message)s",
)

_log = logging.getLogger("katcpcli")

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 1235


def device2hostport(device, favorites):
    """
    Split a device string into host, port. considering the default port and the favorites
    """
    if ":" in device:
        _log.debug('Port and host split')
        host, port = device.split(":")
    elif device in favorites:
        _log.debug('Device found in favorites')
        host, port = favorites[device].split(':')
    else:
        _log.debug('Using devce only')
        host = device
        port = DEFAULT_PORT

    return host, port


async def async_main():
    """
    Run katcpcli program.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
            "--cfgfile",
            default=os.path.join(os.path.expanduser('~'), '.katcpclirc'),
            help="Config file to use. Default: ~/.katcpclirc",
        )
    parser.add_argument(
        "-a",
        "--host",
        help="Host Device to connect to. Updates device setting if both are given.",
    )
    parser.add_argument(
        "-p",
        "--port",
        help="Port to connect to. Updates device setting if both are given.",
    )
    parser.add_argument(
        "-f",
        "--favorites",
        help="Show favorites from config",
        action='store_true'
    )
    parser.add_argument(
        "device",
        nargs="?",
        help="Device to connect to [ip:port]",
        default=f"{DEFAULT_HOST}:{DEFAULT_PORT}",
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print debug output"
    )
    parser.add_argument("--nofs", action="store_true", help="Start as simple prompt app.")

    args = parser.parse_args()
    if args.verbose:
        _log.setLevel("DEBUG")

    cfg = katcpcli.config.from_file(os.path.abspath(args.cfgfile))

    if args.favorites:
        print('Configured favorites:')
        for k, v in cfg['favorites'].items():
            print(f'  * {k:30} --> {v}')
        sys.exit(0)

    host, port = device2hostport(args.device, cfg['favorites'])

    if args.host:
        host = args.host
    if args.port:
        port = args.port

    dispatcher, app = katcpcli.app.create_app_and_dispatcher(args.nofs)
    asyncio.create_task(dispatcher.connect(host, port))

    print("Starting katcp CLI ... ")
    await app.run_async()


def main():
    """
    Run asyncio main
    """
    asyncio.run(async_main())
    print("Exiting katcp CLI ...")


if __name__ == "__main__":
    main()
