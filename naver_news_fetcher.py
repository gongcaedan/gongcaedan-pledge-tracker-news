import os
import urllib.request
import json
import datetime
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 네이버 API 키 가져오기
client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")

# 뉴스 저장 함수
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

    # logs 디렉토리 생성
    log_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_dir, exist_ok=True)

    # 파일 저장
    filename = f"news_{keyword}_{today}.json"
    file_path = os.path.join(log_dir, filename)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(response_result, f, ensure_ascii=False, indent=4)

    return {"message": f"{keyword} 뉴스 저장 성공", "file": file_path}
