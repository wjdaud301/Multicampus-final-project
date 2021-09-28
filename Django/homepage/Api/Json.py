
from homepage.MongoDbManager import MongoDbManager_corona,MongoDbManager_insta
import urllib.request
import json 

# 특정 조회 값의 특정 필드만 조회
# db.getCollection('wow').find({"korean":"사이즈"},{_id:0, "english":1})

def corona_info(nowtime):
    # def get(nowtime):
    context = {}
    dbData = MongoDbManager_corona().get_data_from_collection({'date_st': nowtime})
    for data in dbData:
        del data['_id']
        del data['date_st']
        context[data['area']] = data
    context['time'] = nowtime
    return context
 
def insta_info(theme):
    idx = 0 
    context = {}
    themeData = MongoDbManager_insta().get_data_from_collection({'theme': theme},{'_id':0, "name":1, "description":1, 'area':1,'imgUrl':1})
    for data in themeData[:6]:
        url = data['imgUrl']
        urllib.request.urlretrieve(url, f"/Django/homepage/static/img/filter{idx}.jpg")
        context[str(idx)] = data
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
