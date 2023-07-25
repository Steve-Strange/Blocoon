from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

def XTol(keyword, key):

    url_list = []
    href, name, cover, detail, play_num, comments_num, score, time_start, time_span = 0, 0, 0, 0, 0, 0, 0, 0, 0

    js = "window.open('{}','_blank');"
    chrome_options = Options()
    chrome_options.add_argument('headless')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=chrome_options)

    print("start scrapping")

    for i in range(1, 5):
        if(len(url_list) > 20):     # 最大数量
            break

        print("scrapping page " + str(i))
        
        for j in range(0,10):
            if(len(url_list) > 20):
                break
            
            search_url = "https://www.xuetangx.com/search?query=" + keyword + "&classify=&type=&status=2&ss=manual_search&page=" + str(i)
            driver.get(search_url)
            time.sleep(0.5)
            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            
            cover = soup.find('img').get('src')
            
            click_places = driver.find_elements(By.CLASS_NAME, "resultListCon")
            click_place = click_places[j]
            ActionChains(driver).move_to_element(click_place).click().perform()
            time.sleep(1)
            href = driver.current_url
            html_class = driver.page_source
            soup_class = BeautifulSoup(html_class, "lxml")
            
            print(href)
            
            name = soup_class.find(class_="title f32 c_f").get_text()     
            detail = soup_class.find(class_="f14 c_6 lh23").get_text()
            play_num = int(soup_class.find(class_="f16 fl").get_text().split(' ')[0])
            
            time_start = soup_class.find(class_="list list1").get_text().replace('\t', '').replace('\n', '').strip()[-10:]  
            
            url_list.append([href, name, cover, detail, play_num, comments_num, score, time_start, time_span])
            
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
        exit()

    return url_list

if __name__=="main":
    final_list = XTol(input(), input())
    print(final_list)