from account.models import Company

from django.http import HttpResponseBadRequest
def ajax_required(f):
    def wrap(request,*args,**kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request,*args,**kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__ = f.__name__
    return wrap

def get_company_and_memb_list(request):
    _company = request.session.get('company','null')
    memb_list=[]
    for i in Company.objects.get(name=_company).membs.all():
        memb_list.append(i.realname)
    return _company,memb_list

def islogin(request):
    return request.session.get('islogin', False)





