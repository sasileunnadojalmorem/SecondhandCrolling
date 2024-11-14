from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pyperclip
import pandas as pd
from define import total_next, thing, last_page, user_id, user_pw, driver_path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def filter_articles(driver):
    articles = []
    article_elements = driver.find_elements(By.CSS_SELECTOR, 'td.td_article')
    
    for element in article_elements:
        article_title_element = element.find_element(By.CSS_SELECTOR, 'a.article')
        article_title = article_title_element.text

        # "앱 상품"이 포함되지 않은 경우만 추가
        if "앱 상품" not in article_title:
            article_url = article_title_element.get_attribute('href')
            articles.append({
                "title": article_title,
                "url": article_url
            })
    
    return articles

def crolling(driver, num, datas, datas_yet, page):
    # Retrieve URLs of articles to avoid stale element errors
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.article')))
    articles = filter_articles(driver)

    current_page_link = driver.find_element(By.CSS_SELECTOR, '.prev-next a.on').get_attribute('href')

    for article in articles:
        driver.get(article["url"])
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'cafe_main')))

        try:
            write_date = driver.find_element(By.CSS_SELECTOR, '.date').text
            product_name_element = driver.find_element(By.CSS_SELECTOR, 'p.ProductName')
            product_name = product_name_element.text.replace("", "").strip()

            product_title = product_name_element.text if product_name_element else ''
            price_element = driver.find_element(By.CSS_SELECTOR, 'div.ProductPrice strong.cost')
            price_text = price_element.text.replace("원", "").replace(",", "").strip()
            price = int(price_text)
            
            seller_name = driver.find_element(By.CSS_SELECTOR, '.nick_box').text
            current_url = driver.current_url

            # 이미지 URL 가져오기
            try:
                image_url = driver.find_element(By.CSS_SELECTOR, '.product_thumb img').get_attribute('src')
            except:
                image_url = ''  # 이미지가 없을 경우 빈 문자열

            try:
                status = driver.find_element(By.CSS_SELECTOR, '.SaleLabel').text
                product_price_str = driver.find_element(By.CSS_SELECTOR, '.ProductPrice').text
                price_no_won = product_price_str[:-1]
                product_price = int(price_no_won.replace(',', ''))
            except:
                product_price = ''
                status = ''

            datas_yet.append([write_date, status, seller_name, product_name, current_url, price, image_url])
            print(write_date, status, seller_name, product_name, current_url, price, image_url)

        except Exception as e:
            print(f'Exception occurred while extracting data: {e}')
            datas.append(['', '', '', '', url, '', ''])

        driver.back()
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'cafe_main')))

    driver.get(current_page_link)

def start():
    datas = []
    datas_yet = []

    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    driver.get('https://cafe.naver.com/joonggonara')
    driver.maximize_window()
    time.sleep(1)

    # Login sequence
    login_btn = driver.find_element(By.CSS_SELECTOR, '#gnb_login_button')
    login_btn.click()
    time.sleep(1)

    tag_id = driver.find_element(By.NAME, 'id')
    tag_pw = driver.find_element(By.NAME, 'pw')
    tag_id.clear()
    time.sleep(1)

    # Enter credentials
    tag_id.click()
    pyperclip.copy(user_id)
    tag_id.send_keys(Keys.CONTROL + 'v')
    time.sleep(1)

    tag_pw.click()
    pyperclip.copy(user_pw)
    tag_pw.send_keys(Keys.CONTROL + 'v')
    time.sleep(1)

    login_btn = driver.find_element(By.ID, 'log.login')
    login_btn.click()

    # Search
    driver.find_element(By.CSS_SELECTOR, '#topLayerQueryInput').send_keys(thing)
    driver.find_element(By.CSS_SELECTOR, '#cafe-search .btn').click()
    time.sleep(1)

    driver.switch_to.frame('cafe_main')

    driver.find_element(By.CSS_SELECTOR, '#currentSearchByTop').click()
    time.sleep(1)
    driver.find_elements(By.CSS_SELECTOR, '#sl_general li')[1].click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, '.btn-search-green').click()
    time.sleep(1)

    for i in range(total_next + 1):
        if i == 0:
            if total_next == 0:
                for page in range(last_page):
                    crolling(driver, 0, datas, datas_yet, page)
                break
            for page in range(10):
                crolling(driver, 0, datas, datas_yet, page)
        elif i > 0 and i != total_next:
            for page in range(10):
                crolling(driver, 1, datas, datas_yet, page)
        elif i == total_next:
            for page in range(last_page):
                crolling(driver, 1, datas, datas_yet, page)

    function_df = pd.DataFrame(data=datas, columns=['작성날짜', '판매 상태', '판매자', '제목', 'url', 'price', 'image_url'])
    function_yet_df = pd.DataFrame(data=datas_yet, columns=['작성날짜', '판매 상태', '판매자', '제목', 'url', 'price', 'image_url'])
    print(function_df)
    driver.quit()

    return function_df, function_yet_df
