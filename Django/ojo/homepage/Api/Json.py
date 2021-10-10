
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
