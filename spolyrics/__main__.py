if __package__ is None:  # Direct call __main__.py
    import os, sys

    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, path)

import logging
import os

from spolyrics import constants
from spolyrics import Application


def main():
    if os.getenv('DEBUG') == '1':
        logging.basicConfig(level=logging.DEBUG)

    constants.Path.create_directory()

    app = Application()
    app.run()


if __name__ == '__main__':
    main()
