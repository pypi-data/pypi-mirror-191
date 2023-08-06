import os
import sys
import shlex

MODES = {
    'NORMAL_MODE': lambda args=None: '{} {} {}'.format(sys.executable, sys.argv[0], shlex.join(sys.argv[1:] if args is None else args)),
    'MODULE_MODE': lambda args=None: '{} -m {}'.format(sys.executable, sys.argv[0], shlex.join(sys.argv[1:] if args is None else args)),
    'PYINSTALLER_MODE': lambda args=None: '{} {}'.format(sys.executable, shlex.join(sys.argv[1:] if args is None else args)),
}

def module_mode():
    os.environ.update({'RERUN_MODULE_MODE': '1'})

def current_mode():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return 'PYINSTALLER_MODE'
    elif 'RERUN_MODULE_MODE' in os.environ:
        return 'MODULE_MODE'
    else:
        return 'NORMAL_MODE'

def current_executable(args=None):
    return MODES[current_mode()](args)