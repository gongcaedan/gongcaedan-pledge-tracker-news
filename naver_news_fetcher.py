import os
import urllib.request
import json
import datetime
import psycopg2
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")

# PostgreSQL 연결 함수
def get_pg_conn():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=os.getenv("POSTGRES_PORT")
    )

# 뉴스 크롤링 후 DB에 저장
def fetch_and_save_naver_news(keyword: str) -> dict:
    encText = urllib.parse.quote(keyword)
    today = datetime.datetime.now().strftime('%Y-%m-%d')

    url = f"https://openapi.naver.com/v1/search/news.json?query={encText}&start=1&display=100"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if rescode != 200:
        return {"error": f"요청 실패: {rescode}"}

    response_body = response.read()
    response_result = json.loads(response_body.decode("utf-8"))
    items = response_result.get("items", [])

    # PostgreSQL에 저장
    try:
        conn = get_pg_conn()
        cursor = conn.cursor()

        for item in items:
            title = item["title"]
            description = item["description"]
            link = item["link"]
            pub_date_str = item["pubDate"] 
            pub_date = datetime.datetime.strptime(pub_date_str, '%a, %d %b %Y %H:%M:%S %z')

            cursor.execute("""
                INSERT INTO news (keyword, title, description, link, pub_date)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (keyword, title, description, link, pub_date))

        conn.commit()
        cursor.close()
        conn.close()

        return {"message": f"{keyword} 뉴스 {len(items)}건 DB 저장 완료"}

    except Exception as e:
        return {"error": str(e)}
