import os, shutil
from subprocess import Popen, PIPE
from datetime import datetime
from os.path import basename
from zipfile import ZipFile


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


def open_zipfile(zip_, filename):
    z = ZipFile(zip_, "r")
    with z.open(filename, 'r') as file:
        temp_file = os.path.join(os.environ['temp'], filename)
        temp = open(temp_file, "wb")
        shutil.copyfileobj(file, temp)
        temp.close()
    return temp_file


def packaging(filename, *bindings):
    zipname = r'dist\autom.zip'
    while True:
        if os.path.exists(os.path.join('dist',filename)):
            with ZipFile(zipname, 'w') as zipObj:
                zipObj.write(os.path.join('dist',filename), basename(os.path.join('dist',filename)))
                for binding in bindings:
                    for folderName, subfolders, filenames in os.walk(binding):
                        for filename in filenames:
                            filePath = os.path.join(folderName, filename)
                            zipObj.write(filePath, os.path.join(binding, basename(filePath)))
            print(f'패키징을 완료하였습니다. {zipname}')
            break
        else:
            print('파일이 존재하지 않습니다.')
