from ckd_init import AutoCKDInit
from config import *
import pyautogui
import pyperclip


class E2_Generation(AutoCKDInit):
    def __init__(self):
        super().__init__()
        self.last_group_no = 0
        self.hook = 0
        self.main()

    def main(self):
        self.select_customer (KeyValue.customer_E2)
        self.log_in()
        self.screen_transition('UI-CL-017')
        self.app_connect (re=True, wait=0)
        self.window = self.app.window (title_re=f'^({self.current_title})')
        self.combo_setting()
        self.issue_month_setting()
        self.disable_process_month()
        while True:
            terminal = self.wait_table_loading()
            if terminal:
                print('검색결과가 없습니다. 프로그램 종료')
                break
            self.in_box_operation()

    def combo_setting(self):
        self.wait_until_ready (self.window[KeyValue.combo_box_E2['고객사']])
        while True:
            try:
                self.window[KeyValue.combo_box_E2['처리결과사유']].select (11)
                self.window[KeyValue.combo_box_E2['처리결과']].select (3)
                self.window[KeyValue.combo_box_E2['고객사']].select (self.customer)
                break
            except Exception as e:
                continue

    def issue_month_setting(self):
        while True:
            try:
                self.window[KeyValue.edits_E2['통보서년월_from']].click ()
                pyautogui.hotkey ('home')
                pyautogui.write ('201001')
                if str (self.window[KeyValue.edits_E2['통보서년월_from']].texts ()[0]) == '2010-01':
                    break
                else:
                    continue
            except Exception as e:
                continue

    def disable_process_month(self):
        while self.window[KeyValue.edits_E2['처리일자_from']].is_enabled ():
            self.window.child_window (class_name="Button", top_level_only=True).click ()
        self.window.Image4.click ()
        self.window[KeyValue.image_E2['search']].click()

    def wait_table_loading(self):
        self.current_title = r"KD SYSTEM"
        self.app_connect (re=True, wait=0)
        self.window = self.app.window (title_re=f'^({self.current_title})')
        self.wait_until_ready (self.window[u'AfxWnd80u'], timeout=0.1)
        self.wait_until_image_shows(r'images\header.png')
        self.wait_until_image_disappears (r'images\searching.png')
        num = 0
        pyperclip.copy('')
        while self.hook == self.last_group_no:
            self.window[u'AfxWnd80u'].click_input (coords=(700, 30))
            pyautogui.hotkey ('ctrl', 'c')
            self.hook = pyperclip.paste ()
            num += 1
            print('그룹이의제기번호를 검증합니다.', self.hook)
            if num == 5 :
                return True
            elif self.hook == '' and self.last_group_no == 0:
                self.hook = 0
            elif self.hook == '' and self.last_group_no != 0:
                self.hook, self.last_group_no = 0, 0
        self.last_group_no = self.hook
        print('그룹이의제기번호를 클릭합니다.', self.hook)
        self.window[u'AfxWnd80u'].click_input(coords=(700, 30))
        pyautogui.click (button='left', clicks=2, interval=0.1)

    def in_box_operation(self):
        self.current_title = r"업체이의처리결과 등록"
        self.app_connect (re=True, wait=0)
        self.window = self.app.window (title_re=f'^({self.current_title})')
        self.wait_until_ready(self.window[KeyValue.combo_box_E2_2['처리결과변경']], timeout=0.1)
        self.window[KeyValue.combo_box_E2_2['처리결과변경']].select (1)
        self.wait_until_image_shows(r'images\checkbox.png')
        pyautogui.click(r'images\checkbox.png', button='left', clicks=3)
        self.window[KeyValue.edits_E2_2['회신제목']].type_keys('이의승인')
        self.window[KeyValue.edits_E2_2['회신내용']].type_keys('이의승인')
        self.window[KeyValue.image_E2_2['save']].click()
        self.wait_until_image_shows(r'images\alert.png')
        pyautogui.press('enter')
        self.wait_until_image_shows(r'images\alert.png')
        pyautogui.press('enter')
        # self.window_find_n_kill (u'\uc5c5\uccb4\uc774\uc758\ucc98\ub9ac\uacb0\uacfc \ub4f1\ub85d',
        #                          u'\ud655\uc778', class_name=r'#32770')
        self.window[KeyValue.image_E2_2['close']].click()

    def __del__(self):
        pyautogui.alert(text='프로그램 종료', title='프로세스종료알림', button='OK')


if __name__ == '__main__':
    E2_Generation()
    # os.startfile(r'images\header.png')