# devook-crawler
FastText 모델 학습을 위한 데이터를 수집하는 크롤러 입니다.

# 기능
Surfit과 Tistory의 카테고리별 데이터를 Python 기반 Selenium을 사용해 크롤링 합니다.

1. 해당 페이지로부터 html을 가져옵니다.
2. url, title, description을 파싱합니다.
3. 해당 데이터를 csv 파일에 저장합니다.

# 실행
1. 해당 레포지토리를 git clone 합니다.
2. 사용하는 크롬 버전에 알맞은 chromedriver를 설치합니다.
3. [surfit.py](https://github.com/COOL-EWHA/devook-crawler/blob/master/crawler/surfit/surfit.py)와 [tistory.py](https://github.com/COOL-EWHA/devook-crawler/blob/master/crawler/tistory/tistory.py) 파일을 실행합니다.

