import time
from function.GetLogger import configure_logging
import cmd
import os
import logging
import sys

configure_logging()


class AdbExecutor:

    def __init__(self):
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.adb_dir = os.path.join(self.root_dir, "adb")
        self.adb_exe = os.path.join(self.adb_dir, 'adb.exe')
        self.aab_dir = os.path.join(self.root_dir, "aab")
        self.aab_path = os.path.join(self.aab_dir, "aab.apks")
        self.apk_path = os.path.join(self.aab_dir, "universal.apk")
        self.bundletool_path = os.path.join(self.aab_dir, "bundletool-all-1.11.0.jar")

    def adb_install(self, path):
        logging.info(f'Installing build {self.adb_dir}')
        cmd.exec_cmd(f'{self.adb_exe} install {path}')

    def convert_aab(self, path):
        logging.info(f'Stating to convert aab to apk build {path}')
        cmd1 = f"java -jar {self.bundletool_path} build-apks --bundle={path} --output={self.aab_path} --mode=universal" \
               f" --overwrite"
        cmd.exec_cmd(cmd1)

    def install_aab(self, path):
        self.convert_aab(path)
        logging.info('Unzip aab apks')
        cmd.exec_cmd(f'7z x -aoa -o{self.aab_dir} {self.aab_path}')
        self.adb_install(self.apk_path)

    def go_to_adb(self):
        logging.info(f'Starting adb in  {self.adb_exe}')
        cmd.exec_cmd(f'{self.adb_exe}')

adb = AdbExecutor()
adb.install_aab('D:\Builds\AAB\stable.aab')


