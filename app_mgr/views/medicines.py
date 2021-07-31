import json
from django.http import JsonResponse
from db_common.models import Medicine


def dispatcher(request):
    if 'usertype' not in request.session:
        return JsonResponse({'ret': 302, 'msg': '未登录', 'redirect': '/mgr/sign.html'}, status=302)
    if request.session['usertype'] != 'mgr':
        return JsonResponse({'ret': 302, 'msg': '用户非mgr类型', 'redirect': '/mgr/sign.html'}, status=302)

    if request.method == 'GET':
        request.params = request.GET
    elif request.method in ['POST', 'PUT', 'DELETE']:
        request.params = json.loads(request.body)

    action = request.params['action']
    if action == 'list_medicine':
        return list_medicine(request)
    elif action == 'add_medicine':
        return add_medicine(request)
    elif action == 'modify_medicine':
        return modify_medicine(request)
    elif action == 'del_medicine':
        return del_medicine(request)
    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})


def list_medicine(request):
    if request.method != 'GET':
        return JsonResponse({'ret':1,'msg':'请求方式错误'})
    qs = Medicine.objects.values()
    retList = list(qs)

    return JsonResponse({'ret':0,'retlist':retList})


def add_medicine(request):
    if request.method != 'POST':
        return JsonResponse({'ret':1,'msg':'请求方式错误'})
    info = request.params['data']
    qs = Medicine.objects.filter(sn=info['sn']).values()
    if len(qs) != 0:
        return JsonResponse({'ret':1,'msg':'sn已存在'})
    recode= Medicine.objects.create(sn=info['sn'],name=info['name'],desc=info['desc'])
    return JsonResponse({'ret':0,'msg':f'id:{recode.id} 药品已添加'})

def modify_medicine(request):
    if request.method != 'PUT':
        return JsonResponse({'ret':1,'msg':'请求方式错误'})
    newData = request.params['newdata']
    mid = request.params['id']
    try:
        medicine = Medicine.objects.get(id=mid)
    except Medicine.DoesNotExist:
        return JsonResponse({'ret':1,'msg':f'id:{id} 药品不存在'})

    if 'name' in newData:
        medicine.name =newData['name']
    if 'sn' in newData:
        qs = Medicine.objects.filter(sn=newData['sn']).values()
        if len(qs) >1 or (len(qs)==1 and list(qs)[0]['sn'] != newData['sn']):
            return JsonResponse({'ret': 1, 'msg': 'sn已使用'})
        medicine.sn=newData['sn']
    if 'desc' in newData:
        medicine.desc = newData['desc']

    medicine.save()
    return JsonResponse({'ret':0,'msg':'药品修改成功'})

def del_medicine(request):
    if request.method != 'DELETE':
        return JsonResponse({'ret':1,'msg':'请求方式错误'})
    mid = request.params['id']
    try:
        medicine = Medicine.objects.get(id=mid)
    except Medicine.DoesNotExist:
        return JsonResponse({'ret':1,'msg':f'id:{id} 药品不存在'})

    medicine.delete()
    return JsonResponse({'ret':0,'msg':'药品删除成功'})