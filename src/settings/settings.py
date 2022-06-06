from .telegram import *  # noqa

DEBUG = False
DIFF_HOURS = 0

try:
    from .settings_local import *  # noqa
except (ImportError, ModuleNotFoundError):
    pass