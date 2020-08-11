import os
from subprocess import Popen, PIPE
from datetime import datetime


def make_dir(dirname):
    try:
        os.mkdir(dirname)
        print("Directory ", dirname, " Created ")
    except FileExistsError:
        pass


def path_find(name, *paths):
    for path in paths:
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)


def subprocess_cmd(command):
    print(command)
    try :
        process = Popen(command, stdout=PIPE, shell=True, universal_newlines=True)
        proc_stdout = process.communicate()[0].strip()
    except Exception as e:
        process = Popen(command, stdout=PIPE, shell=True, universal_newlines=False)
        proc_stdout = process.communicate()[0].strip()
    print(proc_stdout)


def make_pulled_dir():
    try:
        os.mkdir(os.path.join(os.getcwd(), 'pulled'))
    except Exception as e:
        pass
    dir = os.path.join(os.getcwd(), 'pulled', f'pulled_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
    os.mkdir(dir)
    return dir