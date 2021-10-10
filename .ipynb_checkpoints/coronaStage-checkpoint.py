from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display

from datetime import datetime, timedelta
from pymongo import MongoClient
import pandas as pd 
import numpy as np
import json


display = Display(visible=0, size=(1024, 768)) 
display.start()
 
path = '/home/ubuntu/chromedriver' 
driver = webdriver.Chrome(path)


def stage_call():
    driver.get('http://ncov.mohw.go.kr/regSocdisBoardView.do')
    info_df = pd.DataFrame(columns=("Area","Stage","Description"))
    idx = 0

    for i in range(1,18):
        location = driver.find_element_by_xpath(f'//*[@id="main_maplayout"]/button[{i}]')
        location.click()

        area = driver.find_element_by_xpath(f'//*[@id="step_map_city{i}"]/h3').text
        stage =  driver.find_element_by_xpath(f'//*[@id="step_map_city{i}"]/h4').text
        description = driver.find_element_by_xpath(f'//*[@id="step_map_city{i}"]/p').text

        # 확인용
        area_info = [area,stage,description]
        info_df.loc[idx] = area_info
        idx += 1

        driver.implicitly_wait(3)

    info_df.to_parquet('coronaStage_'+ nowtime)
    
    