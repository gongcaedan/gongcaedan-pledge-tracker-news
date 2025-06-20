'''
    Google 뉴스에서 정치/사회 관련 뉴스만 크롤링하는 모듈
    생각보다 크롤링 결과 값이 좋지 않아서, 안 쓸 예정
'''

import time
from typing import List
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def init_driver():
    """셀레니움 드라이버 초기화"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=chrome_options)

def is_politically_relevant(title: str) -> bool:
    """정치/사회 관련 키워드 필터링"""
    political_keywords = [
        "정책", "공약", "후보", "정부", "대통령", "국회", "의원", "정당", 
        "행정", "정치", "지자체", "시정", "구정", "선거", "공천", "시의회", "도정"
    ]
    return any(kw in title for kw in political_keywords)

def fetch_google_news(keyword: str, max_results: int = 5) -> List[dict]:
    """Google 뉴스에서 키워드로 정치/사회 관련 뉴스만 검색"""
    driver = init_driver()
    
    # 정치 관련 문맥 강화를 위한 검색어 조정
    query = f"{keyword} 정책 OR 정치 OR 공약"
    query = query.replace(" ", "+")
    url = f"https://www.google.com/search?q={query}&tbm=nws"
    
    driver.get(url)
    time.sleep(2)

    news_list = []
    try:
        articles = driver.find_elements(By.CSS_SELECTOR, "a")
        for a_tag in articles:
            href = a_tag.get_attribute("href")
            title = a_tag.text.strip()

            if (
                href and "http" in href and title and "google.com" not in href
                and is_politically_relevant(title)
            ):
                news_list.append({
                    "url": href,
                    "title": title,
                })
            if len(news_list) >= max_results:
                break
    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")
    finally:
        driver.quit()

    return news_list
