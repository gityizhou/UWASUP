import os
import sys

sys.path.insert(0, os.getcwd())

from recorder import create_app

application = create_app()
