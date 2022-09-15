from GetLogger import configure_logging
import cmd
import os
import logging

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

    def aab_install(self, path):
        self.aab_convert(path)
        logging.info('Unzip aab apks')
        cmd.exec_cmd(f'7z x -aoa -o{self.aab_dir} {self.aab_path}', timeout=30)
        result = self.adb_install(self.apk_path)

        return result

    def adb_install(self, path):
        logging.info(f'Installing build {path}')
        cmd.exec_cmd(f'cd /D {self.adb_dir}')
        result = cmd.exec_cmd(f'adb install {path}', timeout=5)

        return result

    def aab_convert(self, path):
        logging.info(f'Stating to convert aab to apk build {path}')
        cmd1 = f"java -jar {self.bundletool_path} build-apks --bundle={path} --output={self.aab_path} --mode=universal" \
               f" --overwrite"
        result = cmd.exec_cmd(cmd1, timeout=30)

        return result

    def check_device(self):
        logging.info(f'Checking device')
        cmd.exec_cmd(f'cd /D {self.adb_dir}')
        result = cmd.exec_cmd(f'adb devices', timeout=5)

        return result

    def go_to_adb(self):
        logging.info(f'Starting adb in  {self.adb_exe}')
        cmd.exec_cmd(f'{self.adb_exe}')

    def unity_logging(self):
        logging.info(f'Unity logs collecting')
        cmd.exec_cmd(f'cd /D {self.adb_dir}')
        result = cmd.logcat()

        return result

    def unity_logging2(self):
        logging.info(f'Unity logs collecting')
        cmd.exec_cmd(f'cd /D {self.adb_dir}')
        result = cmd.exec_cmd(f'adb logcat -s Unity')

        return result


#adb = AdbExecutor()
#adb.check_device()




