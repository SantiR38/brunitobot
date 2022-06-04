from .telegram import *  # noqa

DEBUG = False

try:
    from .settings_local import *  # noqa
except (ImportError, ModuleNotFoundError):
    pass