from ckd_init import AutoCKDInit
from pywinauto.application import Application
from pywinauto import mouse
from config import KeyValue
import sys, os, time
import pyperclip
import pyautogui
import pickle


class AutoCKDMH(AutoCKDInit):
    def __init__(self):
        super().__init__()
        self.customer = 0
        self.current_title = None
        self.screen_no = None
        self.part_infos = {}
        self.app = Application()
        self.main()

    def log_in(self):
        self.launch()
        self.current_title = r"[KD SYSTEM] Login"
        self.app_connect()
        while True:
            if self.app.Dialog.Edit2.texts()[0] != '1700564':
                self.app.Dialog.Edit2.set_text('')
                self.app.Dialog.Edit2.set_text('1700564')
            else:
                break
        while True:
            if self.app.Dialog.Edit.texts()[0] != 'JSD202006@':
                self.app.Dialog.Edit.set_text('')
                self.app.Dialog.Edit.set_text('JSD202006@')
            else:
                break
        self.app.Dialog.Image.click()

    def update_infos(self, window, part):
        self.part_infos[part] = {}
        self.part_infos[part].update({'중박스코드': window[KeyValue.edits_MH['중박스코드']].texts()[0]})
        # self.part_infos[part].update({'대박스코드': window[KeyValue.edits_MH['대박스코드']].texts()[0]})
        # self.part_infos[part].update({'상신자': window[KeyValue.edits_MH['상신자']].texts()[0]})

    def wait_for_load(self, window):
        mbox_code = ''
        while mbox_code == '':
            mbox_code = window[KeyValue.edits_MH['중박스코드']].texts()[0]

    def scraper(self, window):
        part = ''
        hook = 0
        while part == '':
            window[KeyValue.table_MH['부품번호목록']].click_input(coords=(50, 40))
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'c', interval=0.01)
            part = pyperclip.paste()
            hook += 1
            if hook == 100:
                ans = pyautogui.confirm(text='검색결과가 없습니다', title='검색결과 확인', buttons=['OK', 'Retry'])
                if ans == 'OK':
                    sys.exit()
        if part not in self.part_infos.keys():
            self.wait_for_load(window)
            self.update_infos(window, part)
            print(part, len(self.part_infos.keys()))
        while True :
            pyautogui.press('down')
            self.wait_for_load(window)
            hook = 0
            while part in self.part_infos.keys() or part == '':
                pyautogui.hotkey('ctrl', 'c', interval=0.01)
                part = pyperclip.paste()
                hook += 1
                if part not in self.part_infos.keys():
                    # self.wait_for_load(window)
                    self.update_infos(window, part)
                    print(part, len(self.part_infos.keys()))
                    break
                if hook % 10 == 0 and part in self.part_infos.keys():
                    print('중복', part, len(self.part_infos.keys()))
                    time.sleep(0.5)
                    pyautogui.press('down')
                if hook >= 20:
                    print(f'{len(self.part_infos.keys())} 건이 메모리에 저장되었습니다.')
                    with open('data/info.pkl', 'wb') as file:
                        pickle.dump(self.part_infos, file)
                    return

    def in_box_operation(self, window, mbox_code):  # todo : expand function
        window[KeyValue.image_MH['항목추가']].click()
        window[KeyValue.table_MH['포장재시간']].click_input(coords=(50, 5), double=True)
        window[KeyValue.table_MH['포장재시간']].click_input(coords=(50, 30))
        pyautogui.hotkey('ctrl', 'c', interval=0.1)
        hook = pyperclip.paste()
        if len(hook) > 1:
            window[KeyValue.table_MH['포장재시간']].click_input(coords=(50, 5))
        window[KeyValue.table_MH['포장재시간']].click_input(coords=(120, 30))
        mouse.press(button='left', coords=(pyautogui.position()))
        mouse.release(button='left', coords=(pyautogui.position()))
        self.current_title = r"포장재코드 (POP-UP)"
        self.app_connect(trial=1500, wait=1)
        window2 = self.app.window(title=self.current_title)
        if mbox_code.startswith('PB125'):
            window2[KeyValue.inbox_edits_combo_MH['내부포장재']].type_keys('MH_FOLD PBOX_M', with_spaces=True)
        else:
            window2[KeyValue.inbox_edits_combo_MH['내부포장재']].type_keys('MH_FOLDING PBOX_S', with_spaces=True)
        window2[KeyValue.inbox_image_MH['search']].click()
        hook, num = '', 0
        while hook == '':
            num += 1
            try :
                window2[u'AfxWnd80u1'].click_input(coords=(50, 40))
                pyautogui.hotkey('ctrl', 'c', interval=0.1)
                hook = pyperclip.paste()
                window2[u'AfxWnd80u1'].click_input(coords=(50, 40), double=True)
            except Exception as e:
                print(e)
                break
            if num > 100:
                break
        window[KeyValue.table_MH['포장재시간']].click_input(coords=(50, 30))
        pyautogui.hotkey('tab', 'tab', interval=0.1)
        pyautogui.write('1')
        ans = pyautogui.confirm(text='세이브합니다.', title='세이브 확인', buttons=['OK', 'NO'])
        if ans == 'OK':
            window[KeyValue.image_MH['세이브']].click()
            self.wait_until_image_shows(r'images\save.png')
            self.window_find_n_kill(u'\ud45c\uc900 M/H \ub4f1\ub85d (UI-PM-191)', u'\ud655\uc778', class_name=r'#32770')
            # self.wait_until_image_shows(r'images\save.png')
            # self.window_find_n_kill(u'\ud45c\uc900 M/H \ub4f1\ub85d (UI-PM-191)', u'\ud655\uc778', class_name=r'#32770')
            time.sleep(0.5)
            pyautogui.press('enter')
            # self.wait_until_image_disappears(r'images\error.png')
            pyautogui.press('enter')
        else:
            pass

    def mh_proof(self):
        self.screen_transition('UI-PM-191')
        self.app_connect(re=True, wait=3)
        window = self.app.window(title_re=f'^({self.current_title})')
        window[KeyValue.combo_box_MH['상태']].select(1)
        ans = pyautogui.confirm(text='스크래이핑 시행', title='스크래이핑 확인', buttons=['OK', 'NO'])
        if ans == 'OK':
            window[KeyValue.image_MH['search']].click()
            self.wait_for_load(window)
            self.scraper(window)
            with open('data/info.pkl', 'rb') as file:
                self.part_infos = pickle.load(file)
        else:
            with open('data/info.pkl', 'rb') as file:
                self.part_infos = pickle.load(file)
                print(f'기존에 저장한 정보를 사용합니다. {len(self.part_infos)} 건이 로드되었습니다.')
        for i in self.part_infos.keys():
            part_number = i[0:-5]
            print(f'다음 품번 검색중 : {part_number}')
            mbox_code = str(self.part_infos[i]['중박스코드'])
            if str(mbox_code).endswith('F') or str(mbox_code).endswith('GK') or str(mbox_code).endswith('GN') or \
                    str(mbox_code).startswith('PB323') or str(mbox_code).startswith('PB125'):
                window[KeyValue.edits_MH['품번검색']].click()
                while True:
                    if window[KeyValue.edits_MH['품번검색']].texts()[0] != part_number:
                        window[KeyValue.edits_MH['품번검색']].set_text('')
                        window[KeyValue.edits_MH['품번검색']].set_text(part_number)
                    else:
                        window[KeyValue.image_MH['search']].click()
                        break
                print(f'접철식박스 {mbox_code}')
                self.wait_for_load(window)
                self.wait_until_image_disappears(r'images\error.png')
                ans = pyautogui.confirm(text=f'접철식박스 {mbox_code} 포장재시간 입력확인', title='입력확인', buttons=['OK', 'NO'])
                if ans == 'OK':
                    self.in_box_operation(window, mbox_code)

    def __del__(self):
        pyautogui.alert(text='프로그램 종료', title='프로세스종료알림', button='OK')

    def main(self):
        self.launch()
        self.log_in()
        self.mh_proof()


if __name__ == '__main__':
    AutoCKDMH()