import os

import requests
from bs4 import BeautifulSoup
import re
import json

from src.exception.CustomException import CustomException
from src.exception.EmptyViewingDistributionException import \
    EmptyViewingDistributionException
from src.exception.ParseViewingUnknownException import \
    ParseViewingUnknownException


async def html_parsing(url, videoId, folder):
    filename = videoId+'.json'
    file_path = os.path.join(folder,filename)
    if os.path.exists(file_path):
        print(f"파일 '{filename}'이 이미 존재하여 넘어갑니다.")
    else:
        # 특정 URL에서 HTML 가져오기

        response = requests.get(url)
        html_content = response.text

        # BeautifulSoup으로 HTML 파싱
        soup = BeautifulSoup(html_content, "html.parser")

        # <script> 태그 내의 모든 내용을 찾기
        script_tags = soup.find_all("script")

        # ytInitialData 변수가 있는 <script> 태그를 찾기 위한 정규 표현식
        pattern = re.compile(r"var ytInitialData = ({.*?});", re.DOTALL)

        # <script> 태그 순회하며 ytInitialData(분포데이터) 추출
        json_data = None
        for script in script_tags:
            script_content = script.string
            if script_content:
                match = pattern.search(script_content)
                if match:
                    json_data = match.group(1)
                    break

        # 추출한 JSON 데이터를 파싱
        if json_data:
            data = json.loads(json_data)

            try:
                # frameworkUpdates -> entityBatchUpdate -> mutations -> [0] -> payload -> macroMarkersListEntity -> markersList -> markers
                markers = data["frameworkUpdates"]["entityBatchUpdate"]["mutations"][0]["payload"]["macroMarkersListEntity"][
                    "markersList"
                ]["markers"]
                # markers 배열을 JSON 파일로 저장
                with open(f"./{folder}/{videoId}.json", "w") as json_file:
                    json.dump(markers, json_file, indent=4)
            except Exception as e:
                if type(e).__name__ == "KeyError":
                    raise CustomException("분포데이터가 없습니다.")
                else:
                    raise CustomException("[Parse Viewing] 알 수 없는 ERROR")
