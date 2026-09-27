"""Top-level package execution entrypoint: `python -m wg`"""

import sys

from .main import main

if __name__ == "__main__":
    sys.exit(main())
