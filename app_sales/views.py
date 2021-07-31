from django.http import HttpResponse

from db_common.models import Customer


def listorders(request):
    return HttpResponse('下面是系统中的所有订单信息')

def listcustomers(request):
    ph = request.GET.get('phonenumber',None)
    if ph:
        qs = Customer.objects.filter(phonenumber=ph).values()
        
    else:
        qs = Customer.objects.values()

    retStr = ''
    for customer in qs:
        for name, value in customer.items():
            retStr += f'{name} : {value} | '
        # <br> 表示换行
        retStr += '<br>'

    return HttpResponse(retStr)