import logging
import os
import signal
import subprocess
import time


class ProcResult:
    def __init__(self, cmd, rc, stdout, stderr):
        self.cmd = cmd
        self.rc = rc
        self.stdout = stdout
        self.stderr = stderr

    def __str__(self):
        as_string = f'Command exited with status {self.rc}.\n'
        as_string += f'=== stdout ===\n{self.stdout}\n' if self.stdout else '(no stdout)\n'
        as_string += f'=== stderr ===\n{self.stderr}\n' if self.stderr else '(no stderr)\n'
        return as_string


def exec_cmd(cmd, timeout=None):
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        process.wait(timeout=timeout)
    except Exception as e:
        print(f'Something go wrong {e}')
        logging.debug(f'Something go wrong {e}')
        raise e

    return_code = process.returncode
    result = ProcResult(cmd, return_code, stdout, stderr)

    logging.debug(f'stdout:\n{result.stdout}')
    logging.debug(f'stderr:\n{result.stderr}')

    return result

def logcat(timeout=None):
    try:
        root_dir = os.getcwd()
        logging.info(f'root dir {root_dir}')
        logcat_filename = 'unity.log'
        logcat_file = open(os.path.join(root_dir, logcat_filename), 'w')
        cmd = 'adb logcat -s Unity'
        process = subprocess.Popen(cmd, shell=True, stdout=logcat_file, stderr=subprocess.PIPE, text=True)
        result = ProcResult(cmd, 0, logcat_file, '')
        time.sleep(5)
        process.terminate()
        logcat_file.close()
        print( f' Closed ? {logcat_file.closed}')
        print('Terminated')

        return result

    except Exception as e:
        print(f'Something go wrong {e}')
        logging.debug(f'Something go wrong {e}')
        raise e
