import pandas as pd
import subprocess
from datetime import datetime

# 현재 시간 설정
nowtime = datetime.today().strftime("%Y-%m-%d")

'''
account = [daily_gamsung, gamsung_bnb, gamsung_curation, hi_stay_tour, rest_behappyhere, sookso_diary, sookso_hada]

for i in account:

'''


# daily_gamsung (1)
daily_gamsung = pd.read_csv(f'/home/ubuntu/DE/instagram crawling to csv/+URL/daily_gamsung_{nowtime}.csv')
daily_gamsung_DF = pd.DataFrame(daily_gamsung)
daily_gamsung_DF.drop('Unnamed: 0', axis=1, inplace=True)
daily_gamsung_DF.to_parquet('daily_gamsung_' + nowtime + '.parquet')

# gamsung_bnb (2)
gamsung_bnb = pd.read_csv(f'/home/ubuntu/DE/instagram crawling to csv/+URL/gamsung.bnb_{nowtime}.csv')
gamsung_bnb_DF = pd.DataFrame(gamsung_bnb)
gamsung_bnb_DF.drop('Unnamed: 0', axis=1, inplace=True)
gamsung_bnb_DF.to_parquet('gamsung_bnb_' + nowtime + '.parquet')

# gamsung_curation (3)
gamsung_curation = pd.read_csv(f'/home/ubuntu/DE/instagram crawling to csv/+URL/gamsung_curation_{nowtime}.csv')
gamsung_curation_DF = pd.DataFrame(gamsung_curation)
gamsung_curation_DF.drop('Unnamed: 0', axis=1, inplace=True)
gamsung_curation_DF.to_parquet('gamsung_curation_' + nowtime + '.parquet')

# hi.stay.tour (4)
hi_stay_tour = pd.read_csv(f'/home/ubuntu/DE/instagram crawling to csv/+URL/hi.stay.tour_{nowtime}.csv')
hi_stay_tour_DF = pd.DataFrame(hi_stay_tour)
hi_stay_tour_DF.drop('Unnamed: 0', axis=1, inplace=True)
hi_stay_tour_DF.to_parquet('hi_stay_tour_' + nowtime + '.parquet')


# rest_behappyhere (5)
rest_behappyhere = pd.read_csv(f'/home/ubuntu/DE/instagram crawling to csv/+URL/rest_behappyhere_{nowtime}.csv')
rest_behappyhere_DF = pd.DataFrame(rest_behappyhere)
rest_behappyhere_DF.drop('Unnamed: 0', axis=1, inplace=True)
rest_behappyhere_DF.to_parquet('rest_behappyhere_' + nowtime + '.parquet')

# sookso.diary (6)
sookso_diary = pd.read_csv(f'/home/ubuntu/DE/instagram crawling to csv/+URL/sookso.diary_{nowtime}.csv')
sookso_diary_DF = pd.DataFrame(sookso_diary)
sookso_diary_DF.drop('Unnamed: 0', axis=1, inplace=True)
sookso_diary_DF.to_parquet('sookso_diary_' + nowtime + '.parquet')

# sookso.hada (7)
sookso_hada = pd.read_csv(f'/home/ubuntu/DE/instagram crawling to csv/+URL/sookso.hada_{nowtime}.csv')
sookso_hada_DF = pd.DataFrame(sookso_hada)
sookso_hada_DF.drop('Unnamed: 0', axis=1, inplace=True)
sookso_hada_DF.to_parquet('sookso_hada_' + nowtime + '.parquet')

# total dataset (8)


# HDFS와 연결
def run_cmd(args_list):
        """
        run linux commands
        """
        # import subprocess
        print('Running system command: {0}'.format(' '.join(args_list)))
        proc = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        s_output, s_err = proc.communicate()
        s_return =  proc.returncode
        return s_return, s_output, s_err

# (1) ~ (7) HDFS에 적재
(ret, out, err)= run_cmd(['hdfs', 'dfs', '-moveFromLocal', '/home/ubuntu/DE/daily_gamsung_' + nowtime + '.parquet', '/data/insta'])
(ret, out, err)= run_cmd(['hdfs', 'dfs', '-moveFromLocal', '/home/ubuntu/DE/gamsung_bnb_' + nowtime + '.parquet', '/data/insta'])
(ret, out, err)= run_cmd(['hdfs', 'dfs', '-moveFromLocal', '/home/ubuntu/DE/gamsung_curation_' + nowtime + '.parquet', '/data/insta'])
(ret, out, err)= run_cmd(['hdfs', 'dfs', '-moveFromLocal', '/home/ubuntu/DE/hi_stay_tour_' + nowtime + '.parquet', '/data/insta'])
(ret, out, err)= run_cmd(['hdfs', 'dfs', '-moveFromLocal', '/home/ubuntu/DE/rest_behappyhere_' + nowtime + '.parquet', '/data/insta'])
(ret, out, err)= run_cmd(['hdfs', 'dfs', '-moveFromLocal', '/home/ubuntu/DE/sookso_diary_' + nowtime + '.parquet', '/data/insta'])
(ret, out, err)= run_cmd(['hdfs', 'dfs', '-moveFromLocal', '/home/ubuntu/DE/sookso_hada_' + nowtime + '.parquet', '/data/insta'])

(ret, out, err)= run_cmd(['hdfs', 'dfs', '-moveFromLocal', '/home/ubuntu/DE/sookso_hada_' + nowtime + '.parquet', '/data/modeldata'])

'''