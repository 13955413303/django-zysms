import json
from django.http import JsonResponse
from db_common.models import Customer


def dispatcher(request):
    if 'usertype' not in request.session:
        return JsonResponse({'ret':302,'msg':'未登录','redirect':'/mgr/sign.html'},status=302)
    if request.session['usertype'] != 'mgr':
        return JsonResponse({'ret':302,'msg':'用户非mgr类型','redirect':'/mgr/sign.html'},status=302)


    if request.method == 'GET':
        request.params = request.GET
    elif request.method in ['POST','PUT','DELETE']:
        request.params = json.loads(request.body)

    action = request.params['action']
    if action == 'list_customer':
        return list_customer(request)
    elif action == 'add_customer':
        return  add_customer(request)
    elif action == 'modify_customer':
        return  modify_customer(request)
    elif action == 'del_customer':
        return del_customer(request)
    else:
        return JsonResponse({'ret': 1,'msg':'不支持该类型http请求'})


def list_customer(request):
    if request.method != 'GET':
        return JsonResponse({'ret': 1, 'msg': '请求方式错误'})

    qs = Customer.objects.values()
    ret_list = list(qs)
    return JsonResponse({'ret': 0, 'retlist': ret_list})


def add_customer(request):
    if request.method != 'POST':
        return JsonResponse({'ret': 1, 'msg': '请求方式错误'})
    info = request.params['data']
    print(info)
    qs = Customer.objects.filter(phonenumber=info['phonenumber']).values()
    if len(qs) != 0 :
        return JsonResponse({'ret': 1, 'msg': '手机号已使用'})
    record = Customer.objects.create(name=info['name'], phonenumber=info['phonenumber'], address=info['address'])
    return JsonResponse({'ret': 0, 'id': record.id, 'msg': '新增用户成功'})


def modify_customer(request):
    if request.method != 'PUT':
        return JsonResponse({'ret': 1, 'msg': '请求方式错误'})
    cid = request.params['id']
    new_data = request.params['newdata']

    try:
        customer = Customer.objects.get(id=cid)
    except Customer.DoesNotExist:
        return JsonResponse({'ret': 1, 'msg': f'id 为`{cid}`的客户不存在'})

    if 'name' in new_data:
        customer.name = new_data['name']
    if 'phonenumber' in new_data:
        qs = Customer.objects.filter(phonenumber=new_data['phonenumber']).values()
        if len(qs) > 1 or (len(qs)==1 and list(qs)[0]['id'] != cid):
            return JsonResponse({'ret': 1, 'msg': '手机号已使用'})
        customer.phonenumber = new_data['phonenumber']
    if 'address' in new_data:
        customer.address = new_data['address']

    customer.save()
    return JsonResponse({'ret': 0, 'msg': '信息修改成功'})


def del_customer(request):
    if request.method != 'DELETE':
        return JsonResponse({'ret': 1, 'msg': '请求方式错误'})
    cid = request.params['id']
    try:
        customer = Customer.objects.get(id=cid)
    except Customer.DoesNotExist:
        return JsonResponse({'ret': 1, 'msg': f'id 为`{cid}`的客户不存在'})
    customer.delete()
    return JsonResponse({'ret': 0, 'msg': '删除成功'})
