from utils import *
import os


if __name__ == "__main__":
    dir_py_32 = r'C:\Users\glovis-laptop\AppData\Local\Programs\Python\Python37-32\Scripts'.replace('\\', '/')
    dir_venv_32 = r'D:\devs\autom\venv\Scripts'.replace('\\', '/')

    file_to_compile = path_find('ckd_main.py', os.getcwd())
    file_to_compile = file_to_compile.replace('\\', '/')
    icon_image = path_find('Penguin_4.ico', os.path.join(os.getcwd(), 'images'))
    icon_image =  icon_image.replace('\\', '/')

    # install_command = f'pyinstaller.exe -F --hidden-import=python-dateutil --icon={icon_image} {file_to_compile}'
    install_command = f'pyinstaller.exe -F --hidden-import=python-dateutil {file_to_compile}'
    dir_loc = os.path.join(os.getcwd(), 'dist')

    subprocess_cmd(f' cd {dir_venv_32} & {install_command} & cd dist & copy ckd_main.exe {dir_loc}')
    packaging(r'ckd_main.exe', r'images', r'data', r'online')
    os.startfile('dist')