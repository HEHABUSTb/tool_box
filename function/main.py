import cmd
import os
import logging
from function.GetLogger import configure_logging

root_dir = os.path.dirname(os.path.abspath(__file__))
dir = os.path.abspath(os.curdir)

adb_dir = os.path.join(root_dir, "adb")
print(dir)
print(root_dir)
print(adb_dir)

configure_logging()

cmd_str = f'cd {adb_dir}'
cmd_str_2 = f'adb.exe'
cmd_str_3 = f'adb devices'
cmd.exec_cmd(cmd_str)
#cmd.exec_cmd(cmd_str_2)
print(cmd.exec_cmd(cmd_str_3))