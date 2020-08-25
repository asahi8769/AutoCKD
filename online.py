from ckd_init import AutoCKDInit
from config import *
from utils import *
from datetime import datetime
from pywinauto import mouse
import pyautogui
import pyperclip
import os, time


class OnlineReceipt(AutoCKDInit):
    def __init__(self):
        super().__init__()
        self.full_path = None
        self.month = datetime.today().strftime('%Y-%m')
        self.counter = 0
        self.paste = ''
        self.file_name = None
        self.hook = None
        self.main()

    def uploade_file(self):
        os.startfile('online')
        while True:
            self.file_name = pyautogui.prompt(text='업로드하려는 파일명을 입력하세요. \n파일을 바탕화면 또는 현재 폴더에 위치시켜주세요.', title='파일 업로드')
            self.full_path = path_find(self.file_name, r'C:\Users\glovis-laptop\Desktop', os.path.join(os.getcwd(), 'online'))
            if os.path.exists(self.full_path):
                print(f'업로드할 파일을 찾았습니다. {self.full_path}')
                break
        self.window.set_focus()

    def month_setting(self):
        self.wait_until_ready(self.window[KeyValue.edits_OL['거래명세서년월']], timeout=0.1)
        while True:
            if self.window[KeyValue.edits_OL['거래명세서년월']].texts()[0] == self.month:
                break
            else :
                self.window[KeyValue.edits_OL['거래명세서년월']].click()
                pyautogui.hotkey('home')
                pyautogui.write(self.month)

    def task_setting(self):
        while True:
            try:
                self.window[KeyValue.combo_box_OL['업무구분']].select (1)
                break
            except Exception as e:
                continue

    def type_search(self):
        ans_dic = {'보상' : 0, '변제' : 1, '환불' : 2}
        ans = pyautogui.confirm(text='정산유형 선택', title='정산유형 확인', buttons=['보상', '변제', '환불'])
        while True:
            try:
                self.window[KeyValue.combo_box_OL['정산유형']].select (ans_dic[ans])
                break
            except Exception as e:
                continue
        self.window[KeyValue.image_OL['search']].click()
        self.wait_until_image_disappears(r'images\searching.png')

    def upload_receipt(self):
        self.wait_until_image_disappears(r'images\searching.png')
        num = 0
        while True :
            self.hook =  self.file_name
            pyautogui.click(x=840, y=415)

            num_=0
            while self.hook == self.file_name and num_ < 10:
                pyautogui.hotkey('ctrl', 'c')
                self.hook = pyperclip.paste()
                num_ +=1

            print('다음 Hook을 찾았습니다. :', self.hook == '')
            pyautogui.hotkey('ctrl', 'c')   # double fool-proof
            if pyperclip.paste() == '':
                self.counter += 1
                print(f'hook : "{self.hook}",  증빙업로드 {self.counter}')
                mouse.press(button='left', coords=(865, 415))
                mouse.release(button='left', coords=(865, 415))
                break
            else :
                num += 1
                print(f'hook : "{self.hook}", 재시도 {num}/30')
                pyautogui.click(x=840, y=395)
                pyautogui.click(x=840, y=395)
                pyautogui.click(x=840, y=395)
                if num == 30:
                    return True
                continue
        self.wait_until_ready(self.app.Dialog.Edit, timeout=0.1)
        while self.app.Dialog.Edit.texts()[0] != self.full_path:
            self.app.Dialog.Edit.set_text(self.full_path)
        self.app.Dialog.Button1.click()
        self.wait_until_image_shows(r'images\searching.png')

    def main(self):
        self.launch()
        self.log_in()
        self.screen_transition('UI-MM-464')
        self.app_connect(re=True)
        self.window = self.app.window(title_re=f'^({self.current_title})', found_index=0)
        self.month_setting()
        self.task_setting()
        self.type_search()
        self.uploade_file()
        while True:
            terminal = self.upload_receipt()
            if terminal:
                pyautogui.alert(text='프로그램 종료', title='프로세스종료알림', button='OK')
                break