from selenium import webdriver
import time
from openpyxl import Workbook
import datetime
from selenium.webdriver.common.keys import Keys
import pyperclip

# 로그인
driver = webdriver.Chrome()
driver.implicitly_wait(3)
driver.get('https://www.naver.com/')
time.sleep(1)

# 로그인 버튼을 찾고 클릭합니다
login_btn = driver.find_element_by_class_name('link_login')
login_btn.click()
time.sleep(1)

# id, pw 입력할 곳을 찾습니다.
tag_id = driver.find_element_by_name('id')
tag_pw = driver.find_element_by_name('pw')
tag_id.clear()
time.sleep(1)

# id 입력
tag_id.click()
pyperclip.copy('아이디')
tag_id.send_keys(Keys.CONTROL, 'v')
time.sleep(1)

# pw 입력
tag_pw.click()
pyperclip.copy('비밀번호')
tag_pw.send_keys(Keys.CONTROL, 'v')
time.sleep(1)

# 로그인 버튼을 클릭합니다
login_btn = driver.find_element_by_id('log.login')
login_btn.click()

# datetime
now = datetime.datetime.now()
today = now.strftime('%Y-%m-%d')

# 엑셀
wb = Workbook(write_only=True)
ws = wb.create_sheet(today)
ws.append(['작성날짜', '제목', '가격', 'url'])


driver.get('https://cafe.naver.com/joonggonara')
driver.maximize_window()
time.sleep(1)

# 맥북 검색
driver.find_element_by_css_selector('#topLayerQueryInput').send_keys('맥북 m1')
driver.find_element_by_css_selector('#cafe-search .btn').click()
time.sleep(1)

# iframe 들어가기
driver.switch_to.frame('cafe_main')

for i in range(len(driver.find_elements_by_css_selector('.article'))):

    # 로그인
    # driver.find_element_by_css_selector('.gnb_btn_login').click()
    # driver.find_element_by_css_selector('#id').send_keys('dnjswnsdlaos')
    # driver.find_element_by_css_selector('#pw').send_keys('wnsla13')
    # driver.find_element_by_css_selector('.btn_global').click()


    # 게시글 들어가기
    articles = driver.find_elements_by_css_selector('a.article')[i]
    articles.click()
    time.sleep(1)

    # 정보추출
    write_date = driver.find_element_by_css_selector('.date').text
    product_title = driver.find_element_by_css_selector('.ProductName').text
    product_price = driver.find_element_by_css_selector('.ProductPrice').text
    url = driver.find_element_by_css_selector('.button_url').get_attribute('href')

    # 엑셀에 작성
    ws.append([write_date, product_title, product_price, url])

    # 뒤로가기
    driver.back()
    driver.switch_to.frame('cafe_main')


driver.quit()
wb.save('중고나라 맥북 m1 매물.xlsx')