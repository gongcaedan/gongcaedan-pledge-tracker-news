from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from naver_news_fetcher import fetch_and_save_naver_news
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = FastAPI()

# 공약 이행 판단 키워드 = 크롤링 대상 키워드
must_have_keywords = [
    # 1. 정책 실행 관련 키워드
    "추진", "시행", "착수", "착공", "집행", "승인", "확정", "발표",

    # 2. 성과 지표/변화 키워드
    "증가", "감소", "개통", "개소", "개관", "보급", "지급", "지원", "도입",

    # 3. 행정 및 제도 관련 키워드
    "법안", "의결", "통과", "공포", "고시", "협약", "MOU"
]

class KeywordRequest(BaseModel):
    keywords: List[str]  

@app.get("/")
def hello():
    return {"message": "FastAPI 서버가 성공적으로 작동 중입니다!"}

# 크롤링 요청 엔드포인트
@app.post("/fetch-news")
def fetch_news(req: KeywordRequest):
    results = []
    for keyword in req.keywords:
        result = fetch_and_save_naver_news(keyword)
        results.append(result)
    return {"results": results}

# 스케줄링 함수: 매일 오전 10시에 must_have_keywords 전부 크롤링
def scheduled_fetch_job():
    print(" 스케줄러 실행] 매일 10시: 공약 이행 키워드 기반 뉴스 크롤링 시작")
    for keyword in must_have_keywords:
        result = fetch_and_save_naver_news(keyword)
        print(f" {keyword} 크롤링 완료 → {result.get('file', '저장 실패')}")

# APScheduler 등록 (한국시간 기준)
scheduler = BackgroundScheduler(timezone="Asia/Seoul")
scheduler.add_job(scheduled_fetch_job, 'cron', hour=10, minute=0)  # 매일 오전 10시
scheduler.start()

# 앱 종료 시 스케줄러 종료
atexit.register(lambda: scheduler.shutdown())
