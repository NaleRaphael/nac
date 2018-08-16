from __future__ import absolute_import
import sys


try:
    __NAC_SETUP__
except NameError:
    __NAC_SETUP__ = False

if __NAC_SETUP__:
    sys.stderr.write('Running from nac source directory.\n')
else:
    from . import core
    from .core import *
    from . import logger
    from . import plotter
    from .version import version as __version__

    __all__ = []
    __all__.extend(core.__all__)
    __all__.extend(['logger'])
    __all__.extend(['plotter'])
