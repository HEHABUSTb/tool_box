import logging
import subprocess


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
