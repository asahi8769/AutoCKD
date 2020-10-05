from ckd_init import AutoCKDInit
from config import KeyValue, DateConfig
import pyautogui
from datetime import datetime
from dateutil import relativedelta


class Audition(AutoCKDInit):
    def __init__(self):
        super().__init__()
        self.last_group_no = 0
        self.main()
        self.issue_number = None
        self.first_working_day = None

    def audit_month(self):
        today = datetime.today()
        nextmonth = datetime.today() + relativedelta.relativedelta(months=1)
        while True:
            try :
                ans = input(f"사정년월 (1: {today.strftime('%Y%m')}, 2: {nextmonth.strftime('%Y%m')}) (디폴트 : 1) :")
                if ans == '' or int(ans) != 2 :
                    self.issue_number = today.strftime('%Y%m')
                    self.first_working_day = DateConfig().getFirstWorkingDayOfMonth(dt=today).strftime('%Y%m%d')
                    break
                elif int(ans) == 2:
                    self.issue_number = nextmonth.strftime('%Y%m')
                    self.first_working_day = DateConfig().getFirstWorkingDayOfMonth(dt=nextmonth).strftime('%Y%m%d')
                    break
            except Exception as e:
                print(f'잘못된 값입니다 ({e})')
                continue

    def exc_rate_date(self):
        ans = input(f'환율기준일을 변경합니까?. (디폴트 : {self.first_working_day} Y/N) :')
        if ans.lower() == 'y':
            while True:
                ans1 = input(f'환율기준일을 입력하세요. (양식 : YYYYMMDD) :')
                try:
                    if len(str(int(ans1))) != 8:
                        print('8자리 숫자로 입력하세요(YYYYMMDD)')
                        continue
                    else :
                        self.first_working_day = ans1
                        break
                except Exception as e:
                    print(f'잘못된 값입니다 ({e})')
                    continue

    def main(self):
        self.select_customer(KeyValue.customer_AD)
        self.audit_month()
        self.exc_rate_date()
        self.log_in()
        self.screen_transition('UI-CL-009')
        self.app_connect(re=True, wait=0)
        self.window = self.app.window(title_re=f'^({self.current_title})')
        self.dropdown_customer()
        self.vend_noti_month()
        self.glovis_noti_month()
        self.exc_rate()
        self.audit()

    def dropdown_customer(self):
        while True:
            try:
                self.window[KeyValue.combo_box_AD['고객사']].select(self.customer)
                break
            except:
                continue

    def vend_noti_month(self):
        while True:
            try:
                self.window[KeyValue.edits_AD['업체통보대상년월']].click()
                pyautogui.hotkey('home')
                pyautogui.write(self.issue_number)
                if str(self.window[KeyValue.edits_AD['업체통보대상년월']].texts()[0]) == self.issue_number[0:4] + '-' + self.issue_number[4:]:
                    break
                else:
                    continue
            except Exception as e:
                continue

    def glovis_noti_month(self):
        while True:
            try:
                self.window[KeyValue.edits_AD['사정년월']].click()
                pyautogui.hotkey('home')
                pyautogui.write(self.issue_number)
                if str(self.window[KeyValue.edits_AD['사정년월']].texts()[0]) == self.issue_number[0:4] + '-' + self.issue_number[4:]:
                    break
                else:
                    continue
            except Exception as e:
                continue

    def exc_rate(self):
        while True:
            try:
                self.window[KeyValue.edits_AD['환율기준일']].click()
                pyautogui.hotkey('home')
                pyautogui.write(self.first_working_day)
                if str(self.window[KeyValue.edits_AD['환율기준일']].texts()[0]) == \
                        self.first_working_day[0:4] + '-' + self.first_working_day[4:6] + '-' + self.first_working_day[6:8]:
                    # pyautogui.alert(text=f'환율일자를 확인하세요. {self.first_working_day}',
                    #                 title='적용환율확인', button='OK')
                    break
                else:
                    continue
            except Exception as e:
                continue

    def audit(self):
        self.window[KeyValue.image_AD['Search']].click()
        issuemonth = '____-__'
        while issuemonth == '____-__':
            issuemonth = self.window[KeyValue.edits_AD['사정년월_headinfo']].texts()[0]
        self.window[KeyValue.image_AD['Run']].click()
        self.wait_until_image_shows(r'images\save.png')
        pyautogui.press('enter')


