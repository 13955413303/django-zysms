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
    pass


def add_medicine(request):
    pass


def modify_medicine(request):
    pass


def del_medicine(request):
    pass
