import os
import sys
import tempfile
import subprocess

from . import rerun
from .__log import logger as log

def daemon_mode(args=None, module_name=None, debug=False):
    if module_name is not None: rerun.module_mode()
    mode = rerun.current_mode()
    invocation = rerun.current_executable(args)
    if '__DAEMON__' in os.environ:
        log.info('running in daemon mode')
    elif mode == 'PYINSTALLER_MODE':
        log.info('running in pyinstaller mode')
    elif mode == 'MODULE_MODE':
        log.info('running in module mode')
    elif mode == 'NORMAL_MODE':
        log.info('running in create mode')
        log.info('invoke {}'.format(invocation))
        child_env = os.environ.copy()
        child_env.update({'__DAEMON__': '1'})
        subprocess.Popen(
            invocation,
            stdin=subprocess.DEVNULL,
            stdout=tempfile.TemporaryFile(),
            stderr=tempfile.TemporaryFile(),
            creationflags=subprocess.CREATE_NEW_CONSOLE if debug else subprocess.DETACHED_PROCESS,
            env=child_env
        )
        exit(0)
    else:
        log.info('unknown mode')
        exit(1)