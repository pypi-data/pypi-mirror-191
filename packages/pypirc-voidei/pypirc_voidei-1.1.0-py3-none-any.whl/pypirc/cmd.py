"""PyPiRC CLI Client."""

__author__ = "Greg Albrecht <gba@splunk.com>"
__copyright__ = "Copyright 2012 Splunk, Inc."
__license__ = "Apache License 2.0"

import argparse

from prettyprinter import cpprint  # pyright: ignore

from pypirc.pypirc import PyPiRC


def main() -> None:
    """Main."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--server",
        help="Index Server Name",
        metavar="SERVER",
    )
    parser.add_argument(
        "-r",
        "--repository",
        help="Repository URL",
        metavar="URL",
    )
    parser.add_argument(
        "-u",
        "--username",
        help="User Name",
        metavar="USERNAME",
    )
    parser.add_argument(
        "-p",
        "--password",
        help="Password",
        metavar="PASSWORD",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        help="Quiet mode",
        default=True,
        action="store_false",
    )

    options = parser.parse_args()

    myrc = PyPiRC()

    if options.server:
        server = myrc.servers.get(options.server, {}) if myrc.servers else {}

        if options.repository:
            server["repository"] = options.repository
        if options.username:
            server["username"] = options.username
        if options.password:
            server["password"] = options.password

        myrc.servers[options.server] = server
        myrc.save()

    if not options.quiet:
        pass
    elif myrc.servers:
        cpprint(myrc.servers)
    else:
        print(".pypirc empty!")
