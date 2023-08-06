import subprocess, sys
from pathlib import Path
import adbx

def _run(file : str):
    path = Path(adbx.__path__[0]) / "bin" / "platform-tools" / file
    subprocess.run(f'"{path.as_posix()}" ' + " ".join(sys.argv[1:]), shell = True)

def adb():
    _run("adb")

def fastboot():
    _run("fastboot")

if __name__ == "__main__":
    adb()