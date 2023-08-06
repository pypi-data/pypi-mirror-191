# Copyright © 2023 Daniele Tricoli <eriol@mornie.org>
# SPDX-License-Identifier: BSD-3-Clause

"""A simple tool to send messages into FreakWAN over Bluetooth low energy."""

import asyncio
import logging

from .cli import get_cli


def run():
    """Main entrypoint."""  # noqa: D401
    # ble-serial fire a warning on disconnect, but our main use case is to just
    # send a message and disconnect, so we disable logging here.
    # TODO: Make configurable by the user.
    logging.disable()
    asyncio.run(get_cli())


if __name__ == "__main__":
    run()
