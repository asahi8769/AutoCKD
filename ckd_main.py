from ckd_init import AutoCKDInit
from e2_generation import E2_Generation
from audition import Audition
from mh_calc import AutoCKDMH
from online import OnlineReceipt

def main():
    ans = input('작업 선택 (1: 로그인, 2: 고객사이의승인, 3: 보상변제사정, 4. 온라인증빙, 5. 맨아워계산(접철식)) :')
    if ans == '1':
        obj = AutoCKDInit()
        screen_no = obj.screen_selection()
        obj.launch()
        obj.log_in()
        obj.screen_transition(screen_no)
    elif ans == '2':
        E2_Generation()
    elif ans == '3':
        Audition()
    elif ans == '4':
        OnlineReceipt()
    elif ans == '5':
        AutoCKDMH()
    else :
        return


if __name__ == '__main__':
    while True:
        main()