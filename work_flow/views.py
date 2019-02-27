from django.shortcuts import render, redirect,HttpResponse,Http404
from .models import orders_list, order_stat
from account.models import Profile
from django.db.models import Count
from django.views import generic
from .forms import WorkFlowForm,WorkFlowDetailForm
from django.contrib import messages
from account.models import WeixinUser,Company
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .helpers import ajax_required,get_company_and_memb_list
import json
import requests
from datetime import datetime

def refresh_token(request):
    appid='wxec4567a41338530d'
    secret = 'f81a45edfb0ebb4607c8441fac0876d9'
    access_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (appid,secret) #用于调用微信接口的api
    raw_access_token = requests.get(access_url).json()
    access_token = raw_access_token['access_token']
    request.session['access_tok'] = access_token


def verified(request):
    f=open('MP_verify_YUe1siIcc5wabsNm.txt','rb')
    return HttpResponse(f)


def islogin(request):
    return request.session.get('islogin', False)

def get_info(request):
    openid = request.session.get('openid','null')
    user = WeixinUser.objects.get(openid=openid)
    real_name = user.profile.realname
    company = user.profile.company.name
    return openid,real_name,user,company

class IndexView(generic.ListView):
    template_name = 'order_list.html'
    context_object_name = 'results'

    def get_queryset(self):
        openid = self.request.session.get('openid', 'null')
        company = self.request.session.get('company','null')
        results = orders_list.objects.raw(
            "select a.*,b.stat_nam from work_flow_orders_list a left join work_flow_order_stat b on a.order_status = b.stat_cd "
            "where a.company  = '%s' and a.order_status <> 7" % company) ##这里需要到数据库确认company的外键
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
        _company = self.request.session.get('company')
        for i in Company.objects.get(name=_company).membs.all():
            memb_list.append(i.realname)
        kwargs['count'] = tmp_list
        kwargs['form'] = WorkFlowForm()
        kwargs['memb'] = memb_list
        return super(IndexView, self).get_context_data(**kwargs)

def add_order(request):
    _islogin = islogin(request)
    openid,real_name,user,company = get_info(request)
    _company,memb_list = get_company_and_memb_list(request)
    ass_tok = request.session.get('access_tok','null')

    if request.method == 'POST' and _islogin:
        form = WorkFlowForm(request.POST)
        if form.is_valid() and request.session.get('dept','null') == '总经理':
            _client = form.cleaned_data['client']
            _order_time = form.cleaned_data['order_time']
            _sub_time = form.cleaned_data['sub_time']
            _order_quantity = form.cleaned_data['order_quantity']
            _spec = form.cleaned_data['spec']
            #_unit = form.cleaned_data['unit']
            _person_incharge = form.cleaned_data['person_incharge']
            _requirement = form.cleaned_data['requirement']
            _remark = form.cleaned_data['remark']
            _uuidd = datetime.now().strftime("%Y%m%d%H%S")
            spec_split = _spec.split(';')
            quantity_split = _order_quantity.split(';')
            #unit_split = _unit.split(';')
            if len(spec_split)== len(quantity_split)== 1: #判断是否批量输入 否
                ol = orders_list(user_name=real_name, openid=openid, uuid=_uuidd, client=_client, order_time=_order_time,
                                 sub_time=_sub_time,company=_company,
                                 order_quantity=_order_quantity, spec=_spec,
                                 unit='支', order_status=1, person_incharge=_person_incharge,requirement=_requirement,
                                 remark=_remark)
                try:
                    user_openid = Profile.objects.get(realname=_person_incharge).user.openid
                except:
                    user_openid = ''
                send_ind = new_add_message(user_openid,ass_tok,_client,_spec,_order_quantity,_uuidd,_remark,_sub_time,_order_time)
                if send_ind == True: ##推送模板消息
                    ol.save()
                    return redirect("/flow/")
                else:
                    return HttpResponse(send_ind)

            elif len(spec_split) == len(quantity_split)  > 1: #批量输入
                for i in range(len(spec_split)):
                    ol = orders_list(user_name=real_name, openid=openid, uuid=str(int(_uuidd)+i), client=_client, order_time=_order_time,
                                     sub_time=_sub_time,company=_company,
                                     order_quantity=quantity_split[i], spec=spec_split[i],
                                     unit='支', order_status=1, person_incharge=_person_incharge,requirement=_requirement,
                                     remark=_remark)
                    ol.save()
                try:
                    user_openid = Profile.objects.get(realname=_person_incharge).user.openid
                except:
                    user_openid = ''
                send_ind = new_add_message(user_openid,ass_tok,_client,_spec,_order_quantity,_uuidd,_remark,_sub_time,_order_time)
                if send_ind == True:
                    return redirect("/flow/")
            else:
                messages.warning(request, '批量输入订单信息有误，请重新输入')
                order_form = WorkFlowForm()
                return render(request,'add_order.html',context={'order_form':order_form,'memb':memb_list})
            # try:
            #     user_openid = Profile.objects.get(realname=_person_incharge).user.openid
            # except:
            #     user_openid = ''
            # send_ind = new_add_message(user_openid,ass_tok,_client,_spec,_order_quantity,_uuidd,_remark,_sub_time,_order_time)
            # if send_ind == True: ##推送模板消息
            #     ol.save()
            #     return redirect("/flow/")
            # else:
            #     return HttpResponse(send_ind)
        else:
            messages.warning(request, "操作失败：添加失败,请联系总经理")
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
    ass_tok = request.session.get('access_tok', 'null')
    openid,real_name ,user,company= get_info(request)
    ordr = orders_list.objects.get(uuid=uuidd)
    status_cd = ordr.order_status
    per = user.profile.dept
    if request.method == 'POST':
        next_node = request.POST.get('next_node')
        remark = request.POST.get('remark')
        next_node_id = Profile.objects.get(realname=next_node).user.openid
        if status_cd < 7:
            if per == '总经理' and status_cd <= 7:
                orders_list.objects.filter(uuid=uuidd).update(order_status=status_cd + 1, person_incharge=next_node,remark=remark)
                messages.success(request, "操作成功")
                change_sts_message(next_node_id,ass_tok,ordr.client,ordr.spec,ordr.order_quantity,uuidd,remark,ordr.sub_time,ordr.order_time)
                return redirect("/flow/")
            elif per == '厂长' and status_cd <=7:
                orders_list.objects.filter(uuid=uuidd).update(order_status=status_cd + 1, person_incharge=next_node,remark=remark)
                messages.success(request, "操作成功")
                change_sts_message(next_node_id,ass_tok,ordr.client,ordr.spec,ordr.order_quantity,uuidd,remark,ordr.sub_time,ordr.order_time)
                return redirect("/flow/")
            elif per == '生产主管' and status_cd == 4 or status_cd == 5:
                orders_list.objects.filter(uuid=uuidd).update(order_status=status_cd + 1, person_incharge=next_node,remark=remark)
                messages.success(request, "操作成功")
                change_sts_message(next_node_id,ass_tok,ordr.client,ordr.spec,ordr.order_quantity,uuidd,remark,ordr.sub_time,ordr.order_time)
                return redirect("/flow/")
            elif per == '仓管' and status_cd == 6 or status_cd == 7:
                orders_list.objects.filter(uuid=uuidd).update(order_status=status_cd + 1, person_incharge=next_node,remark=remark)
                messages.success(request, "操作成功")
                change_sts_message(next_node_id,ass_tok,ordr.client,ordr.spec,ordr.order_quantity,uuidd,remark,ordr.sub_time,ordr.order_time)
                return redirect("/flow/")
            else:
                messages.error(request, '操作失败：你没有相应的权限，请联系总经理')
                return redirect("/flow/")
        else:
            messages.warning(request, "该订单已完成")
            return redirect("/flow/")
    else:
        form = WorkFlowDetailForm(request.POST)
        errors = form.errors
        return HttpResponse(errors)

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
    for i in Company.objects.get(name=company).membs.all():
        memb_list.append(i.realname)
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

def order_detail(request,uuidd):
    _,memb_list = get_company_and_memb_list(request)
    order = orders_list.objects.get(uuid=uuidd)
    order_form = WorkFlowDetailForm(instance=order)
    return render(request,'order_detail.html',context=({'order_form':order_form,'memb':memb_list,'uuid':uuidd}))

def new_add_message(openid,access_token,client,spec,quantity,uuidd,remark,sub_time,order_time): ##推送模板消息
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % access_token
    _sub_time = sub_time.strftime("%y-%m-%d")
    _order_time = datetime.now().strftime("%y-%m-%d %H:%M:%S")
    message = {
        "touser":openid,
        "template_id":"tOotk5nGMdC-Jm2gXobKqNpt0LLbyUXDBEe96m-f7oQ",
        "url":"http://www.e-fac.cn/flow/detail/%s" % uuidd,
        "data":{
            "first": {
                "value":"有新的订单，请及时处理！",
                "color":"#173177"
            },
            "keyword1":{
                "value":uuidd,
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
            "keyword4":{
                "value":_sub_time,
                "color": "#173177"
            },
            "keyword5": {
                "value": client,
                "color": "#173177"
            },
            "remark":{
                "value":remark,
                "color":"#173177"
            }

        }
    }
    j_message = json.dumps(message)
    r = requests.post(url=url,data=j_message).json()

    if r['errmsg'] == 'ok':
        return True
    else:
        return r['errmsg']


def change_sts_message(openid,access_token,client,spec,quantity,uuidd,remark,sub_time,order_time):
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % access_token
    _sub_time = sub_time.strftime("%y-%m-%d")
    _order_time = order_time.strftime("%y-%m-%d")
    ordr_info = '客户：%s\n规格：%s\n数量:%s\n下单时间:%s\n交货时间：%s\n' % (client,spec,quantity,_order_time,_sub_time)
    message = {
        "touser": openid,
        "template_id": "cSoH0M_9Q35umZ99pl8r1pZ_Rkq2j4x2_VG_hacnugo",
        "url": "http://www.e-fac.cn/flow/detail/%s" % uuidd,
        "data": {
            "first": {
                "value": "订单已流转到你这，请及时处理",
                "color": "#173177"
            },
            "keyword1": {
                "value": uuidd,
                "color": "#173177"
            },
            "keyword2": {
                "value": ordr_info,
                "color": "#173177"
            },
            "remark": {
                "value": remark,
                "color": "#173177"
            }

        }
    }
    j_message = json.dumps(message)
    r = requests.post(url=url, data=j_message).json()
    if r['errmsg'] == 'ok':
        return True
    else:

        return r['errmsg']


@ajax_required
@require_GET
def autoComplete(request):
    if not islogin(request):
        return JsonResponse({"specs":["wrong","apple"]})
    user_company,_ = get_company_and_memb_list(request)
    spec_list=[]
    specs = orders_list.objects.filter(company=user_company)
    for i in specs:
        spec_list.append(i.spec)
    return JsonResponse({"specs":spec_list})

@ajax_required
@require_GET
def remind(request):
    if not islogin(request):
        return JsonResponse({"status":"请先登录"})
    company,_ = get_company_and_memb_list(request)
    stat_2 = orders_list.objects.filter(order_status='2', company=company).aggregate(
        count_1=Count('order_status')).get('count_1')
    return JsonResponse({"status":stat_2})
