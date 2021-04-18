from selenium import webdriver
import time
import pyperclip
from selenium.webdriver.common.keys import Keys
import pandas as pd
from define import total_next, thing, last_page, user_id, user_pw
def start():
    # 데이터프레임 만들기 위한 박스 만들기
    datas = []


    # 중고나라 들어가기
    driver = webdriver.Chrome('/Users/choewonjun/Downloads/chromedriver')
    driver.implicitly_wait(3)
    driver.get('https://cafe.naver.com/joonggonara')
    driver.maximize_window()
    time.sleep(1)

    # 로그인 버튼을 찾고 클릭합니다.
    login_btn = driver.find_element_by_css_selector('#gnb_login_button')
    login_btn.click()
    time.sleep(1)

    # id, pw 입력할 곳을 찾습니다.
    tag_id = driver.find_element_by_name('id')
    tag_pw = driver.find_element_by_name('pw')
    tag_id.clear()
    time.sleep(1)

    # id 입력
    tag_id.click()
    pyperclip.copy(user_id)
    tag_id.send_keys(Keys.COMMAND, 'v')
    time.sleep(1)

    # pw 입력
    tag_pw.click()
    pyperclip.copy(user_pw)
    tag_pw.send_keys(Keys.COMMAND, 'v')
    time.sleep(1)

    # 로그인 버튼을 클릭합니다
    login_btn = driver.find_element_by_id('log.login')
    login_btn.click()

    # 검색
    driver.find_element_by_css_selector('#topLayerQueryInput').send_keys(thing)
    driver.find_element_by_css_selector('#cafe-search .btn').click()
    time.sleep(1)

    # iframe 들어가기
    driver.switch_to.frame('cafe_main')

    # 제목만으로 바꾸기
    driver.find_element_by_css_selector('#currentSearchByTop').click()
    time.sleep(1)
    driver.find_elements_by_css_selector('#sl_general li')[1].click()
    time.sleep(1)
    driver.find_element_by_css_selector('.btn-search-green').click()
    time.sleep(1)

    # 첫줄부터 끝줄까지 크롤링 함수 정의(만약 "이전" 버튼이 있으면 num은 1 아니면 0 )
    def crolling(num):
        # 게시글 들어가는 반복문
        with_before = 0
        for i in range(len(driver.find_elements_by_css_selector('.article'))):

            # 게시글 들어가기
            articles = driver.find_elements_by_css_selector('a.article')[i]
            articles.click()
            time.sleep(1)

            # 정보추출
            write_date = driver.find_element_by_css_selector('.date').text
            product_title = driver.find_element_by_css_selector('h3.title_text').text
            url = driver.find_element_by_css_selector('.button_url').get_attribute('href')
            # 가격을 못찾으면 그냥 빈칸 입력
            try:
                # 가격 문자열을 숫자로 바꾸기
                product_price_str = driver.find_element_by_css_selector('.ProductPrice').text
                price_no_won = product_price_str[:-1]
                price_no_won_shim = price_no_won.replace(',', '')
                product_price = int(price_no_won_shim)
            except:
                # 제목에서 가격 문자열 추출
                try:
                    product_title = product_title.replace('[', '')
                    product_title = product_title.replace(']', '&')
                    product_price_str = product_title.split('&')[-2]

                    # 가격 문자열을 숫자로 바꾸기
                    price_no_won = product_price_str[:-1]
                    price_no_won_shim = price_no_won.replace(',', '')
                    product_price = int(price_no_won_shim)
                except:
                    product_price = ''
            # 판매 상태 정보 저장
            try:
                status = driver.find_element_by_css_selector('.SaleLabel').text
                # 판매 상태를 '완료' 나 '판매' 로 통일
                if status == '예약중':
                    status = '완료'
                elif status == '판매(안전)':
                    status = '판매'
            except:
                status = "알수없음"

            # 데이터프레임에 작성
            datas.append([write_date, status, product_title, url, product_price])

            # 뒤로가기
            driver.back()
            driver.switch_to.frame('cafe_main')

        # 다음 게시글 page 이동
        pages = driver.find_elements_by_css_selector('.prev-next a')[page + 1 + num]
        pages.click()

    for i in range(total_next + 1):
        # 마지막 10단위 페이지일 때
        if i == 0:
            # 다음페이지 클릭 반복문
            for page in range(10):
                crolling(0)
        elif i > 0 and i != total_next:
            for page in range(10):
                crolling(1)
        elif i == total_next:
            for page in range(last_page):
                crolling(1)

    function_df = pd.DataFrame(data=datas, columns=['작성날짜', '판매 상태', '제목', 'url', '가격'])

    # selenium 끝내기
    driver.quit()

    return function_df