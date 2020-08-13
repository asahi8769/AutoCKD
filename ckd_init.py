from pywinauto.application import Application
from pywinauto.findwindows import find_windows
import pyautogui
import time
from config import *


class AutoCKDInit:
    def __init__(self):
        self.customer = 0
        self.current_title = None
        self.issue_number = None
        self.first_working_day = None
        self.screen_no = None
        self.app = Application()
        self.window = None

    def app_connect(self, re=False, trial=1000, wait=3):
        """
        connect window whose title is similar to self.current title and app pywinauto instance
        :param re: determines whether regex is used to search window title
        :param trial: number of attempts to search and connect before cease searching return False
        :param wait: number of seconds to wait after connection for element to be loaded
        :return: returns bool whether succeeded to connect desired window
        """
        n = 1
        while n < trial:
            try:
                if re:
                    self.app.connect(title_re=f'^({self.current_title})', visible_only=True, found_index=0)
                else:
                    self.app.connect(title=self.current_title, visible_only=True, found_index=0)
                time.sleep(wait)
                print(f'다음 UI를 찾았습니다. {self.current_title}')
                return True
            except Exception as e:
                n += 1
                pass
        return False

    def window_find_n_kill(self, title, confirm, class_name=None, ):
        """
        detect interrupting confirm windows and kill
        :param title: exact title of window
        :param confirm: element name that eliminates the window
        :param class_name: exact class name of the window if applicable
        :param counter: runs counter times
        :return: None
        """
        while True:
            try:
                handle = find_windows(title=title, class_name=class_name)[0]
                window = self.app.window(handle=handle)
                window[confirm].click()
                break
            except Exception as e:
                continue

    def launch(self):
        directory = path_find(
            r'KD SYSTEM.lnk',
            r'C:\\Users\glovis-laptop\Desktop',
            r'C:\Users\glovis-laptop\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar')
        if os.path.exists(directory):
            try:
                print(f'{directory} 를 찾았습니다.')
                os.startfile(directory)
            except Exception as e:
                print(f'KD SYSTEM.lnk 파일을 바탕화면이나 작업표시줄에 위치시켜주십시요. {e}')

    def log_in(self):
        self.launch()
        self.current_title = r"[KD SYSTEM] Login"
        self.app_connect()
        if os.environ.get('CKD_ID') is None or os.environ.get('CKD_PASS') is None:
            id = pyautogui.prompt(text='사번을 입력하세요', title='로그인')
            pw = pyautogui.password(text='비번을 입력하세요', title='로그인')
            while True:
                if self.app.Dialog.Edit2.texts()[0] != id:
                    self.app.Dialog.Edit2.set_text('')
                    self.app.Dialog.Edit2.set_text(id)
                else:
                    break
            while True:
                if self.app.Dialog.Edit.texts()[0] != pw:
                    self.app.Dialog.Edit.set_text('')
                    self.app.Dialog.Edit.set_text(pw)
                else:
                    break
        else:
            while True:
                if self.app.Dialog.Edit2.texts()[0] != os.environ.get('CKD_ID'):
                    self.app.Dialog.Edit2.set_text('')
                    self.app.Dialog.Edit2.set_text(os.environ.get('CKD_ID'))
                else:
                    break
            while True:
                if self.app.Dialog.Edit.texts()[0] != os.environ.get('CKD_PASS'):
                    self.app.Dialog.Edit.set_text('')
                    self.app.Dialog.Edit.set_text(os.environ.get('CKD_PASS'))
                else:
                    break
        self.app.Dialog.Image.click()

    def screen_transition(self, screen_no):
        if screen_no is None:
            return
        self.screen_no = screen_no
        self.current_title = r"KD SYSTEM - \[Main\]"
        self.app_connect(re=True)
        self.window = self.app.window(title_re=f'^({self.current_title})', found_index=0)
        self.wait_until_ready(self.window.Edit)
        self.window.Edit.click()
        pyautogui.press('f2')
        self.window.Edit.click()
        pyautogui.write(self.screen_no)
        pyautogui.press('enter')
        self.current_title = r"KD SYSTEM"

    @staticmethod
    def screen_selection():
        while True:
            ans = input(f'화면 선택 {KeyValue.screen_nm} :')
            if ans == '0':
                return None
            try :
                screen_no = KeyValue.screen_sel[int(ans)]
                return screen_no
            except Exception as e:
                print(f'잘못된 값입니다. {e}')

    def select_customer(self, reference):
        while True:
            ans = input(f'고객사 {reference} :')
            if int(ans) not in reference.values():
                print('다시 입력하십시오.')
                continue
            else:
                self.customer = int(ans)
                break

    @staticmethod
    def wait_until_ready(element, timeout=0.1):
        """with timestamp of timeout, wait permanently until the element is visible and enabled """
        while True:
            try:
                element.wait('ready', timeout=timeout)
                print(f'{element} 가 나타나길 기다리고 있습니다.')
                break
            except Exception as e:
                continue

    @staticmethod
    def wait_until_image_shows(image, region=None):
        """ 'pip install opencv_python' is needed to apply confidence argument to locateOnScreen method"""
        location = None
        while location is None:
            location = pyautogui.locateOnScreen(image, grayscale=True, confidence=.5, region=region)
            print(f'{image} 가 나타나길 기다리고 있습니다.', location)

    @staticmethod
    def wait_until_image_disappears(image, region=None):
        """ 'pip install opencv_python' is needed to apply confidence argument to locateOnScreen method"""
        location = ''
        while location is not None:
            location = pyautogui.locateOnScreen(image, grayscale=True, confidence=.5, region=region)
            print(f'{image} 가 사라지길 기다리고 있습니다.', location)

    def region_box(self):
        region = (int(self.window.rectangle().left),
                  int(self.window.rectangle().top),
                  int(self.window.rectangle().right),
                  int(self.window.rectangle().bottom))
        return region
