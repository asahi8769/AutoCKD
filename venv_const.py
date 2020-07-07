from compiler import subprocess_cmd

dir_venv_32 = r'venv\Scripts'

def install(lib):
    return f'pip --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org install {lib}'


subprocess_cmd(f'cd {dir_venv_32} & {install("opencv_python")} & {install("pywinauto")} & {install("pyinstaller")} & {install("pyautogui")} & {install("python-dateutil")} & {install("pyperclip")}')
# subprocess_cmd(f'cd {dir_venv_32} {install("dateutil")}')