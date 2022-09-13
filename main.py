import subprocess
import time

import os
import logging
from GetLogger import configure_logging

root_dir = os.path.dirname(os.path.abspath(__file__))
dir = os.path.abspath(os.curdir)

adb_dir = os.path.join(root_dir, "adb")
print(dir)
print(root_dir)
print(adb_dir)

configure_logging()

cmd_str = f'cd {adb_dir}'
cmd_str_2 = f'adb.exe'
cmd_str_3 = f'adb install D:\Builds\Release_0.1.2.apk'
#cmd.exec_cmd(cmd_str)
#cmd.exec_cmd(cmd_str_2)
#print(cmd.exec_cmd(cmd_str_3))


def logcat(cmd, timeout=None):
    try:
        logcat_filename = 'function/unity.log'
        logcat_file = open(os.path.join(root_dir, logcat_filename), 'w')
        process = subprocess.Popen(cmd, shell=True, stdout=logcat_file, stderr=subprocess.PIPE, text=True)
        time.sleep(5)
        process.kill()
    except Exception as e:
        print(f'Something go wrong {e}')
        logging.debug(f'Something go wrong {e}')
        raise e


logcat()