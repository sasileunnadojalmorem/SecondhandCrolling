import datetime
# 검색할 물건

thing = '애플워치 se'

# 총 몇 페이지 자료를 모을지 선택
total_page = 1

# 페이지 개수 나누기
total_next = total_page // 10
last_page = total_page - total_next * 10

# datetime
now = datetime.datetime.now()
today = now.strftime('%Y-%m-%d')

# 네이버 아이디, 비번 입력
user_id = ''
user_pw = ''