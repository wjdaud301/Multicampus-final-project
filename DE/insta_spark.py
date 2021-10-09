import pandas as pd
import numpy as np
from collections import Counter
from datetime import datetime
import re

import time
import os
import sys
import urllib.request
import json

from pyspark.conf import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType, IntegerType
from pyspark.sql.functions import array_contains, udf

from pymongo import MongoClient
from datetime import datetime

# pymongo connect
client = MongoClient('localhost',27017) # mongodb 27017 port
db = client.ojo_db

spark = SparkSession\
        .builder\
        .appName('Python Spark SQL basic example')\
        .getOrCreate()

sc = spark.sparkContext

nowtime = datetime.today().strftime("%Y-%m-%d")

# (1) ~ (7)
daily_gamsung_DFP = spark.read.parquet(f"hdfs://localhost:9000/data/insta/daily_gamsung_{nowtime}.parquet")
daily_gamsung_DFP = daily_gamsung_DFP.drop('Unnamed: 0','unix')
daily_gamsung = daily_gamsung_DFP.toPandas()

gamsung_bnb_DFP = spark.read.parquet(f"hdfs://localhost:9000/data/insta/gamsung.bnb_{nowtime}.parquet")
gamsung_bnb_DFP = gamsung_bnb_DFP.drop('Unnamed: 0','unix')
gamsung_bnb = gamsung_bnb_DFP.toPandas()

gamsung_curation_DFP = spark.read.parquet(f"hdfs://localhost:9000/data/insta/gamsung_curation_{nowtime}.parquet")
gamsung_curation_DFP = gamsung_curation_DFP.drop('Unnamed: 0','unix')
gamsung_curation = gamsung_curation_DFP.toPandas()

hi_stay_tour_DFP = spark.read.parquet(f"hdfs://localhost:9000/data/insta/hi_stay_tour_{nowtime}.parquet")
hi_stay_tour_DFP = hi_stay_tour_DFP.drop('Unnamed: 0','unix')
hi_stay_tour = hi_stay_tour_DFP.toPandas()

rest_behappyhere_DFP = spark.read.parquet(f"hdfs://localhost:9000/data/insta/rest_behappyhere_{nowtime}.parquet")
rest_behappyhere_DFP = rest_behappyhere_DFP.drop('Unnamed: 0','unix')
rest_behappyhere = rest_behappyhere_DFP.toPandas()

sookso_diary_DFP = spark.read.parquet(f"hdfs://localhost:9000/data/insta/sookso_diary_{nowtime}.parquet")
sookso_diary_DFP = sookso_diary_DFP.drop('Unnamed: 0','unix')
sookso_diary = sookso_diary_DFP.toPandas()

sookso_hada_DFP = spark.read.parquet(f"hdfs://localhost:9000/data/insta/sookso_hada_{nowtime}.parquet")
sookso_hada_DFP = sookso_hada_DFP.drop('Unnamed: 0','unix')
sookso_hada = sookso_hada_DFP.toPandas()



def daily_gamsung_extract(x):
    p = re.compile('\"[가-힣\t\n\r\f\v\s\_가-힣]+\"')
    m = p.findall(x)
    try:
        return m[0][1:-1]
    except:
        return np.nan

def gamsung_bnb_extract(x):
    p = re.compile("[\'|\"][가-힣]+[\'|\"]") 
    m = p.findall(x)
    try:
        return m[0][1:-1]
    except :
        return np.nan

def gamsung_curation_extract(x):
    p = re.compile('\📍[가-힣]+') # 
    m = p.findall(x)
    try:
        return m[0][1:] 
    except :
        return ''

def hi_stay_tour_extract(x):
    p = re.compile("\#[가-힣]+") # 
    m = p.findall(x)
    try:
        return m[0][1:] 
    except :
        return ''

def rest_behappyhere_extract(x):
    p = re.compile('\#[가-힣]+')
    m = p.findall(x)
    try:
        return m[1][1:]
    except:
        return np.nan

def sookso_diary_extract(x):
    p = re.compile('\📍 [가-힣]+\s[가-힇]+|\📍[가-힣]+\s[가-힇]+')
    m = p.findall(x)
    try:
        return m[0].split(' ')[-1]
    except:
        return np.nan

def sookso_hada_extract(x):
    p = re.compile('\#[가-힣]+')
    m = p.findall(x)
    if  m[1] == '#숙소하다': m[1], m[0] = m[0], m[1]
    return m[1][1:]


## daily_gamsung 
daily_gamsung_name = daily_gamsung.content.apply(lambda x : daily_gamsung_extract(x))
daily_gamsung['name'] = daily_gamsung_name
daily_gamsung = daily_gamsung[~(daily_gamsung['name'].isna())]

# name data가 없는 index 지우기
indexNames = daily_gamsung[daily_gamsung['name'] == ''].index
daily_gamsung.drop(indexNames, inplace=True) 


# like integet 변환 후 합치기
def convert(x):
    return int(x.replace(',',''))

if daily_gamsung.like.dtype == 'O':
    daily_gamsung.like = daily_gamsung.like.apply(lambda x : convert(x))
    

# 1,2,3
dg_cnt = Counter(daily_gamsung.name)
li =[]
for name, cnt  in dg_cnt.items():
    if cnt > 1:
        li.append(name)   

# 4. 행가져와서 like집계, content, tag list append
for i in li:           # 중복된 name 반복
    ex = daily_gamsung.loc[daily_gamsung.name == i]  # 반복된 name의 행을 가져온다
    ex.reset_index(drop=True,inplace=True)     # index reset
    
    content = ex.iloc[0,:].content
    date = ex.iloc[0,:].date
    like = ex.iloc[0,:].like
    place = ex.iloc[0,:].place
    tags = ex.iloc[0,:].tags
    imgUrl = ex.iloc[0,:].imgUrl
    name = ex.name[0]
    
    for i in range(len(ex)-1):
        like += ex.iloc[i+1,:].like
        tags += ex.iloc[i+1,:].tags
    
    # 5.차례대로 기존 행 지워내기
    indexNames = daily_gamsung[daily_gamsung['name'] == ex.name[0]].index
    daily_gamsung.drop(indexNames, inplace=True) 
    daily_gamsung = daily_gamsung.append(pd.Series(data=[content,date,like,place,tags,imgUrl,name],index=daily_gamsung.columns),ignore_index=True)

dg_tmp = []
for i in daily_gamsung.name:
    dg_tmp.append(dg_cnt[i]-1)
    
daily_gamsung['overlap'] = dg_tmp


## gamsung.bnb
gamsung_bnb_name = gamsung_bnb.content.apply(lambda x : gamsung.bnb_extract(x)) 
gamsung_bnb['name'] = gamsung_bnb_name
gamsung_bnb = gamsung_bnb[~(gamsung_bnb['name'].isna())]

# name data가 없는 index 지우기
indexNames = gamsung_bnb[gamsung_bnb['name'] == ''].index
gamsung_bnb.drop(indexNames, inplace=True) 

# like integet 변환 후 합치기
def convert(x):
    return int(x.replace(',',''))

if gamsung_bnb.like.dtype == 'O':
    gamsung_bnb.like = gamsung_bnb.like.apply(lambda x : convert(x))
    
    

# 1, 중복된 이름 검색 
# 2.개수가 1인거 이상 뽑아내기 
# 3.리스트만들기
gb_cnt = Counter(gamsung_bnb.name)      # Counter 모듈로 name data count
li =[]
for name, cnt  in gb_cnt.items():            # 중복된 것만 뽑기 (cnt가 1이상이면 중복)
    if cnt > 1:
        li.append(name)

# 4. 행가져와서 like집계, content, tag list append
for i in li:           # 중복된 name 반복
    ex = gamsung_bnb.loc[gamsung_bnb.name == i]  # 반복된 name의 행을 가져온다
    ex.reset_index(drop=True,inplace=True)     # index reset
    
    content = ex.iloc[0,:].content
    date = ex.iloc[0,:].date
    like = ex.iloc[0,:].like
    place = ex.iloc[0,:].place
    tags = ex.iloc[0,:].tags
    imgUrl = ex.iloc[0,:].imgUrl
    name = ex.name[0]
    
    for i in range(len(ex)-1):
        like += ex.iloc[i+1,:].like
        tags += ex.iloc[i+1,:].tags
        
    
    # 5.차례대로 기존 행 지워내기
    indexNames = gamsung_bnb[gamsung_bnb['name'] == ex.name[0]].index
    gamsung_bnb.drop(indexNames, inplace=True) 
    gamsung_bnb = gamsung_bnb.append(pd.Series(data=[content,date,like,place,tags,imgUrl,name],index=gamsung_bnb.columns),ignore_index=True)

gb_tmp = []
for i in gamsung_bnb.name:
    gb_tmp.append(gb_cnt[i]-1)


gamsung_bnb['overlap'] = gb_tmp


## gamsung_curation
gamsung_curation_name = gamsung_curation.content.apply(lambda x : gamsung_curation_extract(x))
gamsung_curation['name'] = gamsung_curation_name
gamsung_curation = gamsung_curation[~(gamsung_curation['name'].isna())]


# name data가 없는 index 지우기
indexNames = gamsung_curation[gamsung_curation['name'] == ''].index
gamsung_curation.drop(indexNames, inplace=True) 

def convert(x):
    if x:
        return int(x.replace(',',''))
    else:
        return 0

if gamsung_curation.like.dtype == 'O':
    gamsung_curation.like = gamsung_curation.like.apply(lambda x : convert(x))


gc_cnt = Counter(gamsung_curation.name)      # Counter 모듈로 name data count
li =[]
for name, cnt  in gc_cnt.items():            # 중복된 것만 뽑기 (cnt가 1이상이면 중복)
    if cnt > 1:
        li.append(name)        
        

# 4. 행가져와서 like집계, content, tag list append
for i in li:           # 중복된 name 반복
    ex = gamsung_curation.loc[gamsung_curation.name == i]  # 반복된 name의 행을 가져온다
    ex.reset_index(drop=True,inplace=True)     # index reset
    
    content = ex.iloc[0,:].content
    date = ex.iloc[0,:].date
    like = ex.iloc[0,:].like
    place = ex.iloc[0,:].place
    tags = ex.iloc[0,:].tags
    imgUrl = ex.iloc[0,:].imgUrl
    name = ex.name[0]
    
    for i in range(len(ex)-1):
        like += ex.iloc[i+1,:].like
        tags += ex.iloc[i+1,:].tags
    
    # 5.차례대로 기존 행 지워내기
    indexNames = gamsung_curation[gamsung_curation['name'] == ex.name[0]].index
    gamsung_curation.drop(indexNames, inplace=True) 
    gamsung_curation = gamsung_curation.append(pd.Series(data=[content,date,like,place,tags,imgUrl,name],index=gamsung_curation.columns),ignore_index=True)

gc_tmp = []
for i in gamsung_curation.name:
    gc_tmp.append(gc_cnt[i]-1)

gamsung_curation['overlap'] = gc_tmp
gamsung_curation


## hi.stay.tour
hi_stay_tour_name = hi_stay_tour.content.apply(lambda x : hi.stay.tour_extract(x))
hi_stay_tour['name'] = hi_stay_tour_name
hi_stay_tour = hi_stay_tour[~(hi_stay_tour['name'].isna())]


# name data가 없는 index 지우기
indexNames = hi_stay_tour[hi_stay_tour['name'] == ''].index
hi_stay_tour.drop(indexNames, inplace=True) 

def convert(x):
    return int(x.replace(',',''))

if hi_stay_tour.like.dtype == 'O':
    hi_stay_tour.like = hi_stay_tour.like.apply(lambda x : convert(x))


# 1, 중복된 이름 검색 
# 2.개수가 1인거 이상 뽑아내기 
# 3.리스트만들기
hst_cnt = Counter(hi_stay_tour.name)      # Counter 모듈로 name data count
li =[]
for name, cnt  in hst_cnt.items():            # 중복된 것만 뽑기 (cnt가 1이상이면 중복)
    if cnt > 1:
        li.append(name)  

# 4. 행가져와서 like집계, content, tag list append
for i in li:           # 중복된 name 반복
    ex = hi_stay_tour.loc[hi_stay_tour.name == i]  # 반복된 name의 행을 가져온다
    ex.reset_index(drop=True,inplace=True)     # index reset
    
    content = ex.iloc[0,:].content
    date = ex.iloc[0,:].date
    like = ex.iloc[0,:].like
    place = ex.iloc[0,:].place
    tags = ex.iloc[0,:].tags
    imgUrl = ex.iloc[0,:].imgUrl
    name = ex.name[0]
    
    for i in range(len(ex)-1):
        like += ex.iloc[i+1,:].like
        tags += ex.iloc[i+1,:].tags
        
    
    
    # 5.차례대로 기존 행 지워내기
    indexNames = hi_stay_tour[hi_stay_tour['name'] == ex.name[0]].index
    hi_stay_tour.drop(indexNames, inplace=True) 
    hi_stay_tour = hi_stay_tour.append(pd.Series(data=[content,date,like,place,tags,imgUrl,name],index=hi_stay_tour.columns),ignore_index=True)

hst_cnt_tmp = []
for i in hi_stay_tour.name:
    hst_cnt_tmp.append(hst_cnt[i]-1)

hi_stay_tour['overlap'] = hst_cnt_tmp
hi_stay_tour


## rest_behappyhere
rest_behappyhere_name = rest_behappyhere.content.apply(lambda x : rest_behappyhere_extract(x))
rest_behappyhere['name'] = rest_behappyhere_name
rest_behappyhere = rest_behappyhere[~(rest_behappyhere['name'].isna())]

# name data가 없는 index 지우기
indexNames = rest_behappyhere[rest_behappyhere['name'] == ''].index
rest_behappyhere.drop(indexNames, inplace=True) 

def convert(x):
    if x:
        return int(x.replace(',',''))
    else:
        return 0

if rest_behappyhere.like.dtype == 'O':
    rest_behappyhere.like = rest_behappyhere.like.apply(lambda x : convert(x))


# 1, 중복된 이름 검색 
# 2.개수가 1인거 이상 뽑아내기 
# 3.리스트만들기
rb_cnt = Counter(rest_behappyhere.name)      # Counter 모듈로 name data count
li =[]
for name, cnt  in rb_cnt.items():            # 중복된 것만 뽑기 (cnt가 1이상이면 중복)
    if cnt > 1:
        li.append(name)
         

# 4. 행가져와서 like집계, content, tag list append
for i in li:           # 중복된 name 반복
    ex = rest_behappyhere.loc[rest_behappyhere.name == i]  # 반복된 name의 행을 가져온다
    ex.reset_index(drop=True,inplace=True)     # index reset
    
    content = ex.iloc[0,:].content
    date = ex.iloc[0,:].date
    like = ex.iloc[0,:].like
    place = ex.iloc[0,:].place
    tags = ex.iloc[0,:].tags
    imgUrl = ex.iloc[0,:].imgUrl
    name = ex.name[0]
    
    for i in range(len(ex)-1):
        like += ex.iloc[i+1,:].like
        tags += ex.iloc[i+1,:].tags
        
    
    
    # 5.차례대로 기존 행 지워내기
    indexNames = rest_behappyhere[rest_behappyhere['name'] == ex.name[0]].index
    rest_behappyhere.drop(indexNames, inplace=True) 
    rest_behappyhere = rest_behappyhere.append(pd.Series(data=[content,date,like,place,tags,imgUrl,name],index=rest_behappyhere.columns),ignore_index=True)

rb_cnt_tmp = []
for i in rest_behappyhere.name:
    rb_cnt_tmp.append(rb_cnt[i]-1)

rest_behappyhere['overlap'] = rb_cnt_tmp
rest_behappyhere


## sookso.diary
sookso_diary_name = sookso_diary.content.apply(lambda x : sookso_diary_extract(x))
sookso_diary['name'] = sookso_diary_name
sookso_diary = sookso_diary[~(sookso_diary['name'].isna())]


# name data가 없는 index 지우기
indexNames = sookso_diary[sookso_diary['name'] == ''].index
sookso_diary.drop(indexNames, inplace=True) 

def convert(x):
    return int(x.replace(',',''))

if sookso_diary.like.dtype == 'O':
    sookso_diary.like = sookso_diary.like.apply(lambda x : convert(x))


# 1, 중복된 이름 검색 
# 2.개수가 1인거 이상 뽑아내기 
# 3.리스트만들기
sd_cnt = Counter(sookso_diary.name)      # Counter 모듈로 name data count
li =[]
for name, cnt  in sd_cnt.items():            # 중복된 것만 뽑기 (cnt가 1이상이면 중복)
    if cnt > 1:
        li.append(name)

# 4. 행가져와서 like집계, content, tag list append
for i in li:           # 중복된 name 반복
    ex = sookso_diary.loc[sookso_diary.name == i]  # 반복된 name의 행을 가져온다
    ex.reset_index(drop=True,inplace=True)     # index reset
    
    content = ex.iloc[0,:].content
    date = ex.iloc[0,:].date
    like = ex.iloc[0,:].like
    place = ex.iloc[0,:].place
    tags = ex.iloc[0,:].tags
    imgUrl = ex.iloc[0,:].imgUrl
    name = ex.name[0]
    
    for i in range(len(ex)-1):
        like += ex.iloc[i+1,:].like
        tags += ex.iloc[i+1,:].tags
        
    
    
    # 5.차례대로 기존 행 지워내기
    indexNames = sookso_diary[sookso_diary['name'] == ex.name[0]].index
    sookso_diary.drop(indexNames, inplace=True) 
    sookso_diary = sookso_diary.append(pd.Series(data=[content,date,like,place,tags,imgUrl,name],index=sookso_diary.columns),ignore_index=True)

sd_cnt_tmp = []
for i in sookso_diary.name:
    sd_cnt_tmp.append(sd_cnt[i]-1)

sookso_diary['overlap'] = sd_cnt_tmp
sookso_diary


## sookso.hada
sookso_hada_name = sookso_hada.content.apply(lambda x : sookso_hada_extract(x))
sookso_hada['name'] = sookso_hada_name
sookso_hada = sookso_hada[~(sookso_hada['name'].isna())]

# name data가 없는 index 지우기
indexNames = sookso_hada[sookso_hada['name'] == ''].index
sookso_hada.drop(indexNames, inplace=True) 


# like integet 변환 후 합치기
def convert(x):
    return int(x.replace(',',''))

if sookso_hada.like.dtype == 'O':
    sookso_hada.like = sookso_hada.like.apply(lambda x : convert(x))


# 1, 중복된 이름 검색 
# 2.개수가 1인거 이상 뽑아내기 
# 3.리스트만들기
sh_cnt = Counter(sookso_hada.name)      # Counter 모듈로 name data count
li =[]
for name, cnt  in sh_cnt.items():            # 중복된 것만 뽑기 (cnt가 1이상이면 중복)
    if cnt > 1:
        li.append(name)        
        

# 4. 행가져와서 like집계, content, tag list append
for i in li:           # 중복된 name 반복
    ex = sookso_hada.loc[sookso_hada.name == i]  # 반복된 name의 행을 가져온다
    ex.reset_index(drop=True,inplace=True)     # index reset
    
    content = ex.iloc[0,:].content
    date = ex.iloc[0,:].date
    like = ex.iloc[0,:].like
    place = ex.iloc[0,:].place
    tags = ex.iloc[0,:].tags
    imgUrl = ex.iloc[0,:].imgUrl
    name = ex.name[0]
    
    for i in range(len(ex)-1):
        like += ex.iloc[i+1,:].like
        tags += ex.iloc[i+1,:].tags
    
    # 5.차례대로 기존 행 지워내기
    indexNames = sookso_hada[sookso_hada['name'] == ex.name[0]].index
    sookso_hada.drop(indexNames, inplace=True) 
    sookso_hada = sookso_hada.append(pd.Series(data=[content,date,like,place,tags,imgUrl,name],index=sookso_hada.columns),ignore_index=True)

sh_cnt_tmp = []
for i in sookso_hada.name:
    sh_cnt_tmp.append(sh_cnt[i]-1)

sookso_hada['overlap'] = sh_cnt_tmp
sookso_hada






## 프레임 합치기
tot_dataset = daily_gamsung
for df in [gamsung_bnb, gamsung_curation, hi_stay_tour, rest_behappyhere, sookso_diary, sookso_hada]:
    tot_dataset = tot_dataset.append(df)


def convert(x):
    return int(x.replace(',',''))

if tot_dataset.like.dtype == 'O':
    tot_dataset.like = tot_dataset.like.apply(lambda x : convert(x))
    
    
    
dg_cnt = Counter(tot_dataset.name)      # Counter 모듈로 name data count
li =[]
for name, cnt  in dg_cnt.items():            # 중복된 것만 뽑기 (cnt가 1이상이면 중복)
    if cnt > 1:
        li.append(name)
            

# 4. 행가져와서 like집계, content, tag list append
for i in li:           # 중복된 name 반복
    ex = tot_dataset.loc[tot_dataset.name == i]  # 반복된 name의 행을 가져온다
    ex.reset_index(drop=True,inplace=True)     # index reset
    
    content = ex.iloc[0,:].content
    date = ex.iloc[0,:].date
    like = ex.iloc[0,:].like
    place = ex.iloc[0,:].place
    tags = ex.iloc[0,:].tags
    imgUrl = ex.iloc[0,:].imgUrl
    name = ex.name[0]
    overlap = ex.iloc[0,:].overlap
    
    for i in range(len(ex)-1):
        like += ex.iloc[i+1,:].like
        tags += ex.iloc[i+1,:].tags
        overlap += ex.iloc[i+1,:].overlap
    
    
    # 5.차례대로 기존 행 지워내기
    indexNames = tot_dataset[tot_dataset['name'] == ex.name[0]].index
    tot_dataset.drop(indexNames, inplace=True) 
    tot_dataset = tot_dataset.append(pd.Series(data=[content,date,like,place,tags,imgUrl,name,overlap],index=tot_dataset.columns),ignore_index=True)

tot_dataset.drop('place',axis=1,inplace=True)
tot_dataset['place'] = title_et

new_df = tot_.toJSON().map(lambda x: json.loads(x)).collect()
for i in new_df:
    db.corona.insert_one(i)