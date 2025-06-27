from dotenv import load_dotenv
load_dotenv()   
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from naver_news_fetcher import fetch_and_save_naver_news


app = FastAPI()

# 공약 이행 판단 키워드 = 크롤링 대상 키워드
must_have_keywords = [
    "추진", "시행", "착수", "착공", "집행", "승인", "확정", "발표",
    "증가", "감소", "개통", "개소", "개관", "보급", "지급", "지원", "도입",
    "법안", "의결", "통과", "공포", "고시", "협약", "MOU"
]

class KeywordRequest(BaseModel):
    keywords: List[str]

# FastAPI 엔드포인트 정의
@app.get("/")
def hello():
    return {"message": "FastAPI 서버가 성공적으로 작동 중입니다!"}

# FastAPI 엔드포인트: 키워드 기반 뉴스 크롤링
@app.post("/fetch-news")
def fetch_news(req: KeywordRequest):
    results = []
    for keyword in req.keywords:
        results.append(fetch_and_save_naver_news(keyword))
    return {"results": results}

# FastAPI 엔드포인트: 전체 공약 이행 키워드 기반 뉴스 크롤링
def fetch_all_must_have():
    print("전체 공약 이행 키워드 기반 뉴스 크롤링 시작")
    for keyword in must_have_keywords:
        res = fetch_and_save_naver_news(keyword)
        print(f"{keyword}: {res.get('message', '실패')}")

if __name__ == "__main__":
    fetch_all_must_have()
