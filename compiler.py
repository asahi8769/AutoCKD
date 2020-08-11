from subprocess import Popen, PIPE
import os
from os.path import basename
from config import path_find
from zipfile import ZipFile


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


def subprocess_cmd(command):
    process = Popen(command, stdout=PIPE, shell=True, universal_newlines=True)
    proc_stdout = process.communicate()[0].strip()
    print(proc_stdout)


if __name__ == "__main__":
    dir_py_32 = r'C:\Users\glovis-laptop\AppData\Local\Programs\Python\Python37-32\Scripts'.replace('\\', '/')
    dir_venv_32 = r'D:\devs\autom\venv\Scripts'.replace('\\', '/')

    file_to_compile = path_find('ckd_main.py', os.getcwd())
    file_to_compile = file_to_compile.replace('\\', '/')
    icon_image = path_find('Penguin_4.ico', os.path.join(os.getcwd(), 'images'))
    icon_image =  icon_image.replace('\\', '/')

    install_command = f'pyinstaller.exe -F --hidden-import=python-dateutil --icon={icon_image} {file_to_compile}'
    dir_loc = os.path.join(os.getcwd(), 'dist')

    subprocess_cmd(f' cd {dir_venv_32} & {install_command} & cd dist & copy ckd_main.exe {dir_loc}')
    packaging(r'ckd_main.exe', r'images', r'data', r'online')
    os.startfile('dist')