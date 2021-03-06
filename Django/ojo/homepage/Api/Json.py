<<<<<<< HEAD

from homepage.MongoDbManager import MongoDbManager_corona,MongoDbManager_insta
import urllib.request
import json

def corona_info(nowtime):
    # def get(nowtime):
    context = {}
    dbData = MongoDbManager_corona().get_data_from_collection({'날짜': nowtime})
    for data in dbData:
        del data['_id']
        del data['날짜']
        context[data['지역']] = data
    context['time'] = nowtime
    return context
 
def insta_info(theme):
    filter = {'나홀로 여행' : 0 , '도심속 휴식' : 1, '정적인 휴식': 2,'아이와 함께': 3,'시티뷰': 4,'한옥':5,'오션 뷰':6,'숲 속':7}
    idx = 0 
    context = {}
    themeData = MongoDbManager_insta().get_data_from_collection({'topic': filter[theme]})#,{'_id':0, "name":1, "description":1, 'area':1,'imgUrl':1})
    for data in themeData[:6]:
        del data['_id']
        url = data['imgUrl']
        # urllib.request.urlretrieve(url, f"/Django/homepage/static/img/filter{idx}.jpg")
        context['a'+f'{idx}'] = data
        idx += 1
    
    return context
 
 
    # if request.method == 'GET':
    #     return get()
    # else:
    #     return HttpResponse(status=405)
 
# def all_users( request):
#     def get():
#         dbUserData = MongoDbManager().get_users_from_collection({})
#         responseData = []
#         for user in dbUserData:
#             del user['_id']
#             responseData.append(user)
 
#         return HttpResponse(json.dumps(responseData), status=200)
 
#     if request.method == 'GET':
#         return get()
#     else:
#         return HttpResponse(status=405)
=======

from homepage.MongoDbManager import MongoDbManager_corona,MongoDbManager_cluster,MongoDbManager_insta
from urllib.error import URLError, HTTPError
import urllib.request
import pymongo
import json

def corona_info(nowtime):
    # def get(nowtime):
    context = {}
    dbData = MongoDbManager_corona().get_data_from_collection({'날짜': nowtime})
    for data in dbData:
        del data['_id']
        del data['날짜']
        context[data['지역']] = data
    context['time'] = nowtime
    return context
 


def insta_info(theme):
    filter = {'오롯이 나를 위해 보내는 하루': 0 ,'너와 나, 우리 둘만의 하루': 2,'당신의 하루를 특별하게': 3,'고즈넉한 사색의 공간': 4,'우리들만의 파티 플레이스':5,\
         '자연 그대로를 품다':6, '자연에서의 놀이터':7 ,'따듯하고 포근한 공간을 그리며' :8, '하늘과 바다가 가득 밀려드는':9}
    client = pymongo.MongoClient( host='localhost',
                                  port=27017)
    database = client['ojo_db']['cluster']
    idx = 0
    li = []
    context = {}
    themeData = database.find({"$and": [{"place" : {"$ne": ''}},{"category": filter[theme]}]}).sort("_id", pymongo.ASCENDING)#,{'_id':0, "name":1, "description":1, 'area':1,'imgUrl':1})
    for data in themeData[:20]:
        del data['_id']
        if data['imgUrl'] == 'not-image':
            pass
        else:
            url = data['imgUrl']
            try:
                urllib.request.urlretrieve(url, f"/home/ubuntu/Django/ojo/homepage/static/img/filter{idx}.jpg")
            except (HTTPError,TypeError) as e:
                continue

        context['a'+f'{idx}'] = data
        imgurl = f"filter{idx}"
        data['img'] = imgurl
        li.append(data)
        # context.append(data)
        idx += 1
    
    return li, context


def all_info():
    context = {}
    tmp = []
    li = []
    idx = 0 
    client = pymongo.MongoClient( host='localhost',
                                  port=27017)
    database = client['ojo_db']['cluster']
    # result_data = list(database.find())
    # result_data = list(database.find().limit(16))
    result_data = list(database.find({}).limit(80))#database.aggregate([{"$sample":{ "size": 80}}])
    for data in result_data:
        if data['name'] not in tmp :
            tmp.append(data['name'])
            del data['_id']
            if data['imgUrl'] == 'not-image':
                pass
            else:
                url = data['imgUrl']
                try:
                    urllib.request.urlretrieve(url, f"/home/ubuntu/Django/ojo/homepage/static/img/all{idx}.jpg")
                except (HTTPError,TypeError) as e:
                    continue

            # context[f'random{idx}'] = data
            imgurl = f"all{idx}"
            data['img'] = imgurl
            li.append(data)
            idx += 1
        else:
            pass
    return li


def most_like():
    context = {}
    tmp = []
    li = []
    idx = 0 
    client = pymongo.MongoClient( host='localhost',
                                  port=27017)
    database = client['ojo_db']['cluster']
    result_data = list(database.find().sort([("like", pymongo.DESCENDING),("_id", pymongo.ASCENDING)]).limit(83))
    for data in result_data:
        if data['name'] not in tmp :
            tmp.append(data['name'])
            del data['_id']
            if data['imgUrl'] == 'not-image':
                pass
            else:
                url = data['imgUrl']
                try:
                    urllib.request.urlretrieve(url, f"/home/ubuntu/Django/ojo/homepage/static/img/pop{idx}.jpg")
                except (HTTPError,TypeError) as e:
                    continue
            # context[f'like{idx}'] = data
            imgurl = f"pop{idx}"
            data['img'] = imgurl
            li.append(data)
            idx += 1
        else:
            pass
    return li 


def find_name(insta_indices):
    client = pymongo.MongoClient( host='localhost',
                                  port=27017)
    database = client['ojo_db']['cluster']
    return database.find({'name' : {'$in': insta_indices }})



def  name_info(name):
    context = {}
    idx = 0
    for key,value in name.items():
        print(value)
        click_info = list(MongoDbManager_cluster().get_data_from_collection({'name': value }))[0] #database.find({"$and": [{"place" : {"$ne": ''}},{"name": value}]})
        del click_info['_id']
        if click_info['imgUrl'] == 'not-image': # 
            pass
        else:
            url = click_info['imgUrl']
            try:
                urllib.request.urlretrieve(url, f"/home/ubuntu/Django/ojo/homepage/static/img/det{idx}.jpg")
            except (HTTPError,TypeError) as e:
                continue
        idx += 1

        context[key] = click_info
    return context


def tag_local_find_name(tag, local):
    context ={}
    tmp = []
    li = []
    idx = 0
    client = pymongo.MongoClient( host='localhost',
                                  port=27017)
    database = client['ojo_db']['cluster']
    # result_data = list(database.find({'content' : keyword }))
    result_data = list(database.find({'$and' : [{'local' : local},{'content' : tag }]}).limit(80))
    for data in result_data:
        if data['name'] not in tmp :
            tmp.append(data['name'])
            del data['_id']
            if data['imgUrl'] == 'not-image':
                pass
            else:
                url = data['imgUrl']
                try:
                    urllib.request.urlretrieve(url, f"/home/ubuntu/Django/ojo/homepage/static/img/all{idx}.jpg")
                except (HTTPError,TypeError) as e:
                    continue
            # context[f'random{idx}'] = data
            imgurl = f"all{idx}"
            data['img'] = imgurl
            li.append(data)
           
            idx += 1
        else:
            pass
    return li


def tag_find_name(tag):
    context ={}
    tmp = []
    li = []
    idx = 0
    client = pymongo.MongoClient( host='localhost',
                                  port=27017)
    database = client['ojo_db']['cluster']
    # result_data = list(database.find({'content' : keyword }))
    result_data = list(database.find({'content' : tag }).limit(80))
    for data in result_data:
        if data['name'] not in tmp :
            tmp.append(data['name'])
            del data['_id']
            if data['imgUrl'] == 'not-image':
                pass
            else:
                url = data['imgUrl']
                try:
                    urllib.request.urlretrieve(url, f"/home/ubuntu/Django/ojo/homepage/static/img/all{idx}.jpg")
                except (HTTPError,TypeError) as e:
                    continue
            # context[f'random{idx}'] = data
            imgurl = f"all{idx}"
            data['img'] = imgurl
            li.append(data)
            idx += 1
        else:
            pass
    return li

def local_find_name(local):
    context ={}
    tmp = []
    li = []
    idx = 0
    client = pymongo.MongoClient( host='localhost',
                                  port=27017)
    database = client['ojo_db']['cluster']
    # result_data = list(database.find({'content' : keyword }))
    result_data = list(database.find({'local' : local }).limit(80))
    for data in result_data:
        if data['name'] not in tmp :
            tmp.append(data['name'])
            del data['_id']
            if data['imgUrl'] == 'not-image':
                pass
            else:
                url = data['imgUrl']
                try:
                    urllib.request.urlretrieve(url, f"/home/ubuntu/Django/ojo/homepage/static/img/all{idx}.jpg")
                except (HTTPError,TypeError) as e:
                    continue
            # context[f'random{idx}'] = data
            imgurl = f"all{idx}"
            data['img'] = imgurl
            li.append(data)
            idx += 1
        else:
            pass
    return li




    # if request.method == 'GET':
    #     return get()
    # else:
    #     return HttpResponse(status=405)
 
# def all_users( request):
#     def get():
#         dbUserData = MongoDbManager().get_users_from_collection({})
#         responseData = []
#         for user in dbUserData:
#             del user['_id']
#             responseData.append(user)
 
#         return HttpResponse(json.dumps(responseData), status=200)
 
#     if request.method == 'GET':
#         return get()
#     else:
#         return HttpResponse(status=405)
>>>>>>> 26f4beea27c7167f6d41785eb695130952d1665e
