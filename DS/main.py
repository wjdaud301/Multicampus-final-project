import doc_classification as dc
import insta_prepro as ipp
import make_all as ma
import modeling as md
import naver_prepro as npp
import preprocessing_2 as pp
import pandas as pd
import numpy as np
import re
import time
from kiwipiepy import Kiwi
import tomotopy as tp

#############################

#

def main():
    userdic = './word.txt'
    stoptext = './stopwords_korean.txt'
    naver = './naverfilepath.csv'
    insta = './instafilepath.csv'

    pp.make_userdic(userdic) #사용자사전 생성

    stopwords = pp.make_stopwords(stoptext) #불용어 리스트 생성

    naver_data = npp.naver_preprocessing(naver=naver) #네이버 데이터 전처리

    insta_data = ipp.insta_preporcessing(insta=insta) #인스타 데이터 전처리 

    all_items = ma.make_total_list(naver_data, insta_data) #네이버 / 인스타 데이터 병합

    model = md.create_model(all_items) #모델링 작업

    merged_data = dc.doc_classification(insta_data, all_items, model)

    return merged_data


if __name__ == '__main__':
    main()