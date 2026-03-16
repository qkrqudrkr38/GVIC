"""
[GVIC Standard Operating Procedure]
File Name: __main___082457.py
Status: RESTORED ELITE
Function: COMMAND & CONTROL
"""

"""
    pygments.__main__
    ~~~~~~~~~~~~~~~~~

    Main entry point for ``python -m pygments``.

    :copyright: Copyright 2006-2023 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import sys
from pip._vendor.pygments.cmdline import main

try:
    sys.exit(main(sys.argv))
except KeyboardInterrupt:
    sys.exit(1)
