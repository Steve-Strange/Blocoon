from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

def XTol(keyword, key):

    url_list = []
    href, name, cover, detail, play_num, comments_num, score, time_start, time_span = 0, 0, 0, 0, 0, 0, 0, 0, 0

    js = "window.open('{}','_blank');"
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument("blink-settings=imagesEnabled=false")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=chrome_options)

    print("start scrapping")

    for i in range(1, 4):
        if(len(url_list) >= 20):     # 最大数量
            break

        print("scrapping page " + str(i))
        
        for j in range(0,10):
            if(len(url_list) >= 20):
                break
            
            search_url = "https://www.xuetangx.com/search?query=" + keyword + "&classify=&type=&status=2&ss=manual_search&page=" + str(i)
            driver.get(search_url)
            time.sleep(0.5)
            
            click_places = driver.find_elements(By.CLASS_NAME, "resultListCon")
            covers = driver.find_elements(By.CLASS_NAME, "leftImg")
            time.sleep(0.1)
            try:
                click_place = click_places[j]
                cover = covers[j].find_elements(By.TAG_NAME, "img")[-1].get_attribute("src")      
            except Exception:
                continue
            ActionChains(driver).move_to_element(click_place).click().perform()
            time.sleep(0.6)
            href = driver.current_url
            html_class = driver.page_source
            soup_class = BeautifulSoup(html_class, "lxml")
            if(href.find("training") != -1):
                continue
            
            print(href)
            try:
                name = soup_class.find(class_="title f32 c_f").get_text()
                detail = soup_class.find(class_="f14 c_6 lh23").get_text()
            except Exception:
                continue
            try:
                play_num = int(soup_class.find(class_="entry-count").get_text().split(' ')[0][:-4])
            except Exception:
                play_num = int(0)    
            try:
                time_start = soup_class.find(class_="list list1").get_text().replace('\t', '').replace('\n', '').strip()[-10:]
            except Exception:
                time_start = ""
            
            url_list.append([href, name, cover, detail, play_num, comments_num, score, time_start, time_span])
        if(len(click_places) < 10):
            break
    driver.quit()
    print("finish scrapping")

    if key == "0":
        url_list.sort(key=lambda x: x[1], reverse=True)   # 名称排序
    elif key == "1":
        url_list.sort(key=lambda x: float(x[4]), reverse=True)   # 播放量 / 参与用户数
    elif key == "2":
        url_list.sort(key=lambda x: float(x[5]), reverse=True) # 评论数量
    elif key == "3":
        url_list.sort(key=lambda x: float(x[6]), reverse=True) # 评分
    elif key == "4":
        url_list.sort(key=lambda x: x[7], reverse=True) # 视频发布日期
    else:
        url_list.sort(key=lambda x: x[8], reverse=True) # 视频时长

    if len(url_list) == 0:
        print("No results")

    return url_list

if __name__ == "__main__":
    final_list = XTol(input(), input())
    print(final_list)