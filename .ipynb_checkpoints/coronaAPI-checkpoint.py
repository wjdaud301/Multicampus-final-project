# import pyarrow
import requests
import xmltodict
import time
import pandas as pd
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
import os


url_district_base = "http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson"
url_district_serviceKey = "S8%2Ftx%2BhEP7bZDZI%2By0P1ZKvPuHpx%2BVUKpt6ay8faxnxR%2FTRO9M5UAy8%2BafhJBNVzQG%2Fgwoym2S4Xbe1dUXivUw%3D%3D"

# corona open api 가져오기
nowtime = datetime.today().strftime("%Y-%m-%d")
url_pages = "1000" #페이지당열갯수
url_start_date = datetime.today().strftime("%Y%m%d%H%M%S")[:8]#"20200303" #시작날짜
url_end_date = datetime.today().strftime("%Y%m%d%H%M%S")[:8] #끝날짜

# open api 가져오기
url_district= url_district_base + "?serviceKey=" + url_district_serviceKey + "&pageNo=1&numOfRows=" + url_pages + "&startCreateDt="+ url_start_date + "&endCreateDt=" + url_end_date
# type 변환 

def API_call():
    req = requests.get(url_district).content
    xmlObject = xmltodict.parse(req)
    dict_data = xmlObject['response']['body']['items']['item']

    # 전처리
    dfDistrict = pd.DataFrame(dict_data)

    # 합계, 검역 삭제 후 dataframe 내에서 index 다시 0부터 차례대로 지정
    dfDistrict = dfDistrict[(dfDistrict['gubun'] != '합계') & (dfDistrict['gubun'] != '검역')].reset_index(drop=True).copy()
    dfDistrict.drop(['stdDay', 'updateDt', 'seq', 'qurRate', 'gubunCn'], axis=1, inplace=True)
    dfDistrict = dfDistrict.astype({"createDt":"datetime64[ns]"}).copy()
    # dfDistrict['createDt'] = dfDistrict['createDt'] - pd.DateOffset(days=2)
    dfDistrict['stateDt'] = dfDistrict['createDt'].dt.date         # YYYY-MM-DD(문자)
    dfDistrict.drop(['createDt'], axis=1, inplace=True)
    dfDistrict.drop(['gubunEn'], axis=1, inplace=True)

    # type 변환
    dfDistrict = dfDistrict.astype({"stateDt":"datetime64[ns]", "defCnt":"int64", "deathCnt":"int64", "incDec":"int64"}).copy()
    dfDistrict = dfDistrict[['stateDt', 'gubun', 'defCnt', 'deathCnt', 'incDec', 'isolClearCnt', 'isolIngCnt', 'localOccCnt', 'overFlowCnt']].copy()

    # null값 처리
    dfDistrict['isolClearCnt'] = dfDistrict['isolClearCnt'].fillna(0).astype("int64")
    dfDistrict['isolIngCnt'] = dfDistrict['isolIngCnt'].fillna(0).astype("int64")
    dfDistrict['localOccCnt'] = dfDistrict['localOccCnt'].fillna(0).astype("int64")
    dfDistrict['overFlowCnt'] = dfDistrict['overFlowCnt'].fillna(0).astype("int64")

    # Dataframe 형태 정리
    dfDistrict = dfDistrict.astype({"isolClearCnt":"int64", "isolIngCnt":"int64", "localOccCnt":"int64", "overFlowCnt":"int64"}).copy()
    dfDistrict.rename(columns={'stateDt':'날짜', 'gubun':'Area', 'defCnt':'확진자수', 'deathCnt':'사망자수', 'incDec':'전일대비증감수',
                               'isolClearCnt':'격리해제수', 'isolIngCnt':'격리중환자수', 'localOccCnt':'지역발생수', 
                               'overFlowCnt':'해외유입수'}, inplace=True)

    dfDistrict.to_parquet('coronaAPI_'+ nowtime)
    os.system("hdfs dfs -moveFromLocal 'coronaAPI_'+ nowtime /data/corona ")

    
    
if __name__=='__main__':
    API_call()
