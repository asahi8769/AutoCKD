import calendar
from datetime import datetime, timedelta, date


class KeyValue:
    combo_box_E2 = {'처리결과사유': 'ComboBox1', '이의처리상태': 'ComboBox2', '이의유형': 'ComboBox3',
                 '고객사': 'ComboBox4', '처리결과': 'ComboBox5'}
    edits_E2 = {'Ro_no': 'Edit1', '처리일자_to': 'Edit2', '처리일자_from': 'Edit3', '통보서년월_to': 'Edit4',
             '그룹이의제기번호': 'Edit5', '원인부품번호': 'Edit7', '업체': 'Edit9', '통보서년월_from': 'Edit10'}
    customer_E2 = {'전체': 0, 'HAOS': 1, 'HMB': 2, 'HMMR': 3, 'KMMG': 4, 'KMS': 5, 'DWI': 6,'HTBC': 7, 'KMI': 8,
                   'HMI': 9, 'KMM': 10, 'HMMA': 11, 'HMMC': 12, 'KMC': 13}
    image_E2 = {'search': 'Image4'}
    combo_box_E2_2 = {'처리결과변경': 'ComboBox2'}
    edits_E2_2 = {'회신내용': 'Edit6', '회신제목': 'Edit7'}
    image_E2_2 = {'close': 'Image4', 'save' : 'Image2'}
    combo_box_MH = {'상태': 'ComboBox10'}
    image_MH = {'search': 'image9', '품번돋보기' : 'Image27', '세이브' : 'Image8', '상신' : 'Image7', '승인' : 'Image6',
                '항목추가' : 'Image24'}
    edits_MH = {'상신자' : 'Edit2', '전체작업시간_sec' : 'Edit8', '전체작업시간_mh' : 'Edit5', '대포장시간' : 'Edit11',
                '대박스분류별_대포장시간' : 'Edit14', '포장방법' : 'Edit19', '적입수(대)' : 'Edit20', '부품명' : 'Edit21',
                '묶음수량' : 'Edit22', '적입수(중)' : 'Edit23', '품번' : 'Edit24', '개당CBM' : 'Edit25',
                '대박스코드' :'Edit26', '차종' : 'Edit27', '단중(g)' : 'Edit28', '중박스코드' : 'Edit29',
                '고객사' : 'Edit30', '품번검색' : 'Edit31'}
    inbox_image_MH = {'닫기' : 'Image2', 'search' : 'Image3', '돋보기' : 'Image1'}
    inbox_edits_combo_MH = {'내부포장재' : 'Edit3', '포장재코드' : 'Edit4', '업체코드' : 'Edit2', '포장재유형' : 'ComboBox'}
    table_MH = {'포장재시간': u'AfxWnd80u2', '부품번호목록' : u'AfxWnd80u4'}
    combo_box_AD = {'고객사': 'ComboBox2'}
    edits_AD = {'업체통보대상년월' : 'Edit3', '사정년월' : 'Edit5', '환율기준일' : 'Edit4', '사정년월_headinfo' :'Edit2'}
    customer_AD = {'HMMA': 0, 'HMMR': 1, 'KMS':2, 'HMI': 3, 'HTBC': 4, 'YOUNGSAN': 5, 'HAOS': 6, 'KMC': 7, 'KMM': 8, 'KMI': 9,
                   'HMMC': 10, 'KMMG': 11, 'HMB': 12, 'DWI': 13}
    image_AD = {'Search' : 'Image3' , 'Run' : 'Image4'}
    edits_OL = {'거래명세서년월': 'Edit3'}
    combo_box_OL = {'전송여부': 'ComboBox1', '상태': 'ComboBox2', '사업장': 'ComboBox3', 'CKD고객사코드': 'ComboBox4',
                    '정산유형': 'ComboBox5', '업무구분': 'ComboBox6'}
    image_OL = {'search': 'Image4'}
    screen_sel = {1: 'UI-CL-011', 2: 'UI-CL-103', 3: 'UI-CL-102', 4: 'UI-CL-005', 5: 'UI-CL-032', 6: 'UI-CL-017',
                  7: 'UI-CL-015', 8: 'UI-MM-003', 9: 'UI-CL-010'}
    screen_nm = {0: '로그인', 1: '사정결과조회', 2: '보상금액조정', 3: '클레임통보', 4: '분담조건등록', 5: '귀책조건등록',
                 6: '업체이의처리', 7:'고객사이의처리', 8:'고객차종별부품등록', 9:'사정마감'}


class DateConfig:
    def getFirstDay(self, dt, d_months=0, d_years=0):
        # d_years, d_months are "deltas" to apply to dt
        y, m = dt.year + d_years, dt.month + d_months
        a, m = divmod(m - 1, 12)
        return datetime(y + a, m + 1, 1)

    def isWeekend(self, dt=date.today()):
        int_day_of_week = dt.weekday()
        day_of_week = calendar.day_name[int_day_of_week]
        if day_of_week in ['Saturday', 'Sunday']:
            return True
        else:
            return False

    def isWeekday(self, dt=date.today()):
        int_day_of_week = dt.weekday()
        day_of_week = calendar.day_name[int_day_of_week]
        if day_of_week not in ['Saturday', 'Sunday']:
            return True
        else:
            return False

    def daterange(self, start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    def getFirstWorkingDayOfMonth(self, dt=date.today()):
        first_day_of_month = self.getFirstDay(dt)
        seventh_day_of_month = first_day_of_month + timedelta(days=6)
        for d in self.daterange(first_day_of_month, seventh_day_of_month):
            if self.isWeekday(d):
                return d.date()
            else:
                continue

    def isFirstWorkingDayOfMonth(self, dt=date.today()):
        if dt == self.getFirstWorkingDayOfMonth(dt):
            return True
        else:
            return False


