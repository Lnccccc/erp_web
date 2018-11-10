from django.shortcuts import render, redirect,HttpResponse
from .models import orders_list, order_stat
from account.models import Profile
from uuid import uuid4
from django.db.models import Count
from django.views import generic
from .forms import WorkFlowForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from account.models import WeixinUser
import json
import requests

# Create your views here.
def islogin(request):
    return request.session.get('islogin', False)

def get_info(request):
    openid = request.session.get('openid','null')
    user = WeixinUser.objects.get(openid=openid)
    real_name = user.profile.realname
    company = user.profile.company
    return openid,real_name,user,company

class IndexView(generic.ListView):
    template_name = 'order_list.html'
    context_object_name = 'results'

    def get_queryset(self):
        openid = self.request.session.get('openid', 'null')
        company = self.request.session.get('company','null')
        results = orders_list.objects.raw(
            "select a.*,b.stat_nam from work_flow_orders_list a left join work_flow_order_stat b on a.order_status = b.stat_cd where a.company = '%s' " % company)
        return results

    def get_context_data(self, **kwargs):
        openid = self.request.session.get('openid', 'null')
        company = self.request.session.get('company','null')
        tmp_list = []
        memb_list = []
        stat_1 = orders_list.objects.filter(order_status='1', company=company).aggregate(
            count_1=Count('order_status')).get('count_1')
        tmp_list.append(stat_1)
        stat_2 = orders_list.objects.filter(order_status='2', company=company).aggregate(
            count_1=Count('order_status')).get('count_1')
        tmp_list.append(stat_2)
        stat_3 = orders_list.objects.filter(order_status='3', company=company).aggregate(
            count_1=Count('order_status')).get('count_1')
        tmp_list.append(stat_3)
        stat_4 = orders_list.objects.filter(order_status='4', company=company).aggregate(
            count_1=Count('order_status')).get('count_1')
        tmp_list.append(stat_4)
        stat_5 = orders_list.objects.filter(order_status='5', company=company).aggregate(
            count_1=Count('order_status')).get('count_1')
        stat_6 = orders_list.objects.filter(order_status='6', company=company).aggregate(
            count_1=Count('order_status')).get('count_1')
        stat_7 = orders_list.objects.filter(order_status='7', company=company).aggregate(
            count_1=Count('order_status')).get('count_1')
        tmp_list.append(stat_5)
        tmp_list.append(stat_6)
        tmp_list.append(stat_7)
        company = self.request.session.get('company')
        membs = Profile.objects.filter(company=company)
        try:
            for i in membs:
                memb_list.append(i.realname)
        except:
            memb_list.append('无')
        kwargs['count'] = tmp_list
        kwargs['form'] = WorkFlowForm()
        kwargs['memb'] = memb_list
        return super(IndexView, self).get_context_data(**kwargs)


def add_order(request):
    _islogin = islogin(request)
    openid,real_name,user,company = get_info(request)
    _company = request.session.get('company','null')
    memb_list=[]
    membs = Profile.objects.filter(company=_company)
    ass_tok = request.session.get('access_tok','null')
    try:
        for i in membs:
            memb_list.append(i.realname)
    except:
        memb_list.append('无')
    if request.method == 'POST' and _islogin:
        form = WorkFlowForm(request.POST)
        if form.is_valid() and request.session.get('dept','null') == '总经理':
            _client = form.cleaned_data['client']
            _order_time = form.cleaned_data['order_time']
            _sub_time = form.cleaned_data['sub_time']
            _order_quantity = form.cleaned_data['order_quantity']
            _spec = form.cleaned_data['spec']
            _unit = form.cleaned_data['unit']
            _person_incharge = form.cleaned_data['person_incharge']
            ol = orders_list(user_name=real_name, openid=openid, uuid=uuid4(), client=_client, order_time=_order_time,
                             sub_time=_sub_time,company=_company,
                             order_quantity=_order_quantity, spec=_spec,
                             unit=_unit, order_status=1, person_incharge=_person_incharge)
            try:
                user_openid = Profile.objects.get(realname=_person_incharge).user.openid
            except:
                user_openid = ''
            send_ind = send_message(user_openid,ass_tok,_client,_spec,_order_quantity)
            if send_ind == True: ##推送模板消息
                ol.save()
                return redirect("/flow/")
            else:
                return HttpResponse(send_ind)
        else:
            erros = form.errors
            messages.warning(request, str(request.user.profile.dept) + "操作失败：添加失败,请联系总经理")
            return redirect("/flow/")
    else:
        order_form = WorkFlowForm()
        return render(request,'add_order.html',context={'order_form':order_form,'memb':memb_list})


def delete_order(request, uuidd):
    _islogin = islogin(request)
    if _islogin:
        status_cd = orders_list.objects.filter(uuid=uuidd)[0].order_status
        per = request.session.get('dept','null')
        if per == '总经理' and status_cd < 7:
            orders_list.objects.filter(uuid=uuidd).delete()
            messages.success(request, "操作成功")
            return redirect("/flow/")
        elif per == '厂长' and status_cd == 2 or status_cd == 3:
            orders_list.objects.filter(uuid=uuidd).delete()
            messages.success(request, "操作成功")
            return redirect("/flow/")
        elif per == '生产主管' and status_cd == 4 or status_cd == 5:
            orders_list.objects.filter(uuid=uuidd).delete()
            messages.success(request, "操作成功")
            return redirect("/flow/")
        elif per == '仓管' and status_cd == 6 or status_cd == 7:
            orders_list.objects.filter(uuid=uuidd).delete()
            messages.success(request, "操作成功")
            return redirect("/flow/")
        else:
            messages.error(request, per + str(status_cd) + '操作失败：你没有这个权限')
            return redirect("/flow/")
    else:
        redirect('account/edit/')

def update_order(request, uuidd):
    openid,real_name ,user,company= get_info(request)
    status_cd = orders_list.objects.get(uuid=uuidd).order_status
    per = user.profile.dept
    if request.method == 'POST':
        next_node = request.POST.get('next_node')
        if status_cd < 7:
            if per == '总经理' and status_cd < 7:
                orders_list.objects.filter(uuid=uuidd).update(order_status=status_cd + 1, person_incharge=next_node)
                messages.success(request, "操作成功")
                return redirect("/flow/")
            elif per == '厂长' and status_cd == 2 or status_cd == 3:
                orders_list.objects.filter(uuid=uuidd).update(order_status=status_cd + 1, person_incharge=next_node)
                messages.success(request, "操作成功")
                return redirect("/flow/")
            elif per == '生产主管' and status_cd == 4 or status_cd == 5:
                orders_list.objects.filter(uuid=uuidd).update(order_status=status_cd + 1, person_incharge=next_node)
                messages.success(request, "操作成功")
                return redirect("/flow/")
            elif per == '仓管' and status_cd == 6 or status_cd == 7:
                orders_list.objects.filter(uuid=uuidd).update(order_status=status_cd + 1, person_incharge=next_node)
                messages.success(request, "操作成功")
                return redirect("/flow/")
            else:
                messages.error(request, per + str(status_cd) + '操作失败：你没有相应的权限，请联系总经理')
                return redirect("/flow/")
        else:
            messages.warning(request, "该订单已完成")
            return redirect("/flow/")
    else:
        pass

def roll_back(request, uuidd):
    status_cd = orders_list.objects.filter(uuid=uuidd)[0].order_status
    if status_cd > 1:
        orders_list.objects.filter(uuid=uuidd).update(order_status=status_cd - 1)
        messages.success(request, "操作成功")
        return redirect("/flow/")
    else:
        return redirect("/flow/")

def status(request, status_cd):
    openid,real_name,user,company = get_info(request)
    forms = WorkFlowForm()
    tmp_list = []
    memb_list = []
    stat_1 = orders_list.objects.filter(order_status='1', company=company).aggregate(
        count_1=Count('order_status')).get('count_1')
    tmp_list.append(stat_1)
    stat_2 = orders_list.objects.filter(order_status='2', company=company).aggregate(
        count_1=Count('order_status')).get('count_1')
    tmp_list.append(stat_2)
    stat_3 = orders_list.objects.filter(order_status='3', company=company).aggregate(
        count_1=Count('order_status')).get('count_1')
    tmp_list.append(stat_3)
    stat_4 = orders_list.objects.filter(order_status='4', company=company).aggregate(
        count_1=Count('order_status')).get('count_1')
    tmp_list.append(stat_4)
    stat_5 = orders_list.objects.filter(order_status='5', company=company).aggregate(
        count_1=Count('order_status')).get('count_1')
    stat_6 = orders_list.objects.filter(order_status='6', company=company).aggregate(
        count_1=Count('order_status')).get('count_1')
    stat_7 = orders_list.objects.filter(order_status='7', company=company).aggregate(
        count_1=Count('order_status')).get('count_1')
    tmp_list.append(stat_5)
    tmp_list.append(stat_6)
    tmp_list.append(stat_7)
    membs = Profile.objects.filter(company=company)
    try:
        for i in membs:
            memb_list.append(i.realname)
    except:
        memb_list.append('无')
    if status_cd:
        results = orders_list.objects.raw(
            "select a.*,b.stat_nam from work_flow_orders_list a left join work_flow_order_stat b on a.order_status = b.stat_cd where a.order_status=%d and a.company='%s'" % (
            status_cd, company))
    elif status_cd == 0:
        results = orders_list.objects.raw(
            "select a.*,b.stat_nam from work_flow_orders_list a left join work_flow_order_stat b on a.order_status = b.stat_cd where a.company='%s'" % company)
    return render(request, 'order_list.html', context={"results": results, "count": tmp_list, "form": forms,"memb":memb_list})

def permission_denied(request):
    messages.error(request, '操作失败')
    return render(request, 'order_list.html')

def send_message(openid,access_token,client,spec,quantity): ##推送模板消息
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % access_token
    message = {
        "touser":openid,
        "template_id":"ES2r90989DqX0QCmoGbrKYUcUOG3VG3rVnI6h-QOh4k",
        "url":"http://47.107.119.21/flow/",
        "data":{
            "first": {
                "value":"有新的订单，请及时处理！",
                "color":"#173177"
            },
            "keyword1":{
                "value":client,
                "color":"#173177"
            },
            "keyword2": {
                "value":spec,
                "color":"#173177"
            },
            "keyword3": {
                "value":quantity,
                "color":"#173177"
            },
            "remark":{
                "value":'点击立刻处理',

            }

        }
    }
    j_message = json.dumps(message)
    r = requests.post(url=url,data=j_message).json()

    if r['errmsg'] == 'ok':
        return True
    else:
        return r['errmsg']
