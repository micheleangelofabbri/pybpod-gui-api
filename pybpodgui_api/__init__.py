# !/usr/bin/python3
# -*- coding: utf-8 -*-

""" pybpod gui API

"""

import sys
import os
from confapp import conf

__version__ = "1.8.3"
__author__ = "Ricardo Jorge Vieira Ribeiro"
__credits__ = ["Ricardo Ribeiro", "Carlos Mão de Ferro", 'Luís Teixeira']
__license__ = "MIT"
__maintainer__ = ["Ricardo Ribeiro", "Carlos Mão de Ferro", 'Luís Teixeira']
__email__ = ["ricardojvr@gmail.com", "cajomferro@gmail.com", 'micboucinha@gmail.com']
__status__ = "Development"

# Load settings using pyforms library
# Include user settings in case the file exists

conf += 'pybpodgui_api.settings'

# try:
# 	import pycontrolapi.user_settings_api as user_settings
#
# 	conf += user_settings
# except:
# 	pass

# Workaround for pyInstaller and multiprocessing on Windows
# https://github.com/pyinstaller/pyinstaller/wiki/Recipe-Multiprocessing
# Module multiprocessing is organized differently in Python 3.4+
try:
    # Python 3.4+
    if sys.platform.startswith('win'):
        import multiprocessing.popen_spawn_win32 as forking
    else:
        import multiprocessing.popen_fork as forking
except ImportError:
    import multiprocessing.forking as forking

if sys.platform.startswith('win'):
    # First define a modified version of Popen.

    class _Popen(forking.Popen):
        def __init__(self, *args, **kw):
            if hasattr(sys, 'frozen'):
                # We have to set original _MEIPASS2 value from sys._MEIPASS
                # to get --onefile mode working.
                os.putenv('_MEIPASS2', sys._MEIPASS)
            try:
                super(_Popen, self).__init__(*args, **kw)
            finally:
                if hasattr(sys, 'frozen'):
                    # On some platforms (e.g. AIX) 'os.unsetenv()' is not
                    # available. In those cases we cannot delete the variable
                    # but only set it to the empty string. The bootloader
                    # can handle this case.
                    if hasattr(os, 'unsetenv'):
                        os.unsetenv('_MEIPASS2')
                    else:
                        os.putenv('_MEIPASS2', '')

    # Second override 'Popen' class with our modified version.
    forking.Popen = _Popen
