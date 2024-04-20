"""
Helper to run code remotely using mpremote command.
"""

# Sanity check that runtime is MicroPython.
from platform import platform
assert platform().startswith("MicroPython"), "This code is for MicroPython, (not CPython)"

# mpremote fix to enable lib loading 
# For more information see https://github.com/micropython/micropython/issues/9734
import os
if os.getcwd() == "/remote":
    import sys
    sys.path[2] = "lib" # replace /lib with lib

try:
    # Load boot.py (if it exists)
    import boot
except:
    pass

try:
    # Load main.py (if it exists)
    import main
except:
    pass
