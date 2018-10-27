from django.shortcuts import render,redirect
from .models import orders_list,order_stat
from uuid import uuid4
from django.db.models import Count
from django.views import generic
from .forms import WorkFlowForm
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib import messages
# Create your views here.
class IndexView(generic.ListView):
    template_name = 'order_list.html'
    context_object_name = 'results'

    def get_queryset(self):
        user_name = self.request.user.username
        results = orders_list.objects.raw("select a.*,b.stat_nam from work_flow_orders_list a left join work_flow_order_stat b on a.order_status = b.stat_cd where a.user_name = '%s' " % user_name)
        return results
    def get_context_data(self,  **kwargs):
        user_name = self.request.user.username
        tmp_list = []
        stat_1 = orders_list.objects.filter(order_status='1',user_name=user_name).aggregate(count_1=Count('order_status')).get('count_1')
        tmp_list.append(stat_1)
        stat_2 = orders_list.objects.filter(order_status='2',user_name=user_name).aggregate(count_1=Count('order_status')).get('count_1')
        tmp_list.append(stat_2)
        stat_3 = orders_list.objects.filter(order_status='3',user_name=user_name).aggregate(count_1=Count('order_status')).get('count_1')
        tmp_list.append(stat_3)
        stat_4 = orders_list.objects.filter(order_status='4',user_name=user_name).aggregate(count_1=Count('order_status')).get('count_1')
        tmp_list.append(stat_4)
        stat_5 = orders_list.objects.filter(order_status='5',user_name=user_name).aggregate(count_1=Count('order_status')).get('count_1')
        stat_6 = orders_list.objects.filter(order_status='6',user_name=user_name).aggregate(count_1=Count('order_status')).get('count_1')
        stat_7 = orders_list.objects.filter(order_status='7',user_name=user_name).aggregate(count_1=Count('order_status')).get('count_1')
        tmp_list.append(stat_5)
        tmp_list.append(stat_6)
        tmp_list.append(stat_7)
        kwargs['count'] = tmp_list
        kwargs['form'] = WorkFlowForm()
        return super(IndexView,self).get_context_data(**kwargs)
@login_required
def add_order(request):
    if request.method == 'POST':
        form = WorkFlowForm(request.POST)
        if  form.is_valid() and request.user.profile.dept == '总经理':
            _client = form.cleaned_data['client']
            _order_time = form.cleaned_data['order_time']
            _sub_time = form.cleaned_data['sub_time']
            _order_num = form.cleaned_data['order_num']
            _order_detail = form.cleaned_data['order_detail']
            _ps = form.cleaned_data['ps']
            _person_incharge = form.cleaned_data['person_incharge']
            ol = orders_list(user_name=request.user.username,uuid=uuid4(),client=_client,order_time=_order_time,sub_time=_sub_time,
                             order_num=_order_num,order_detail=_order_detail,
                             ps=_ps,order_status=1,person_incharge=_person_incharge)
            ol.save()
            messages.success(request,"添加成功")
            return redirect("/flow/")
        else:
            erros = form.errors
            messages.warning(request,str(request.user.profile.dept)+"操作失败：添加失败,请联系总经理")
            return redirect("/flow/")
@login_required
def delete_order(request,uuidd):
    status_cd = orders_list.objects.filter(uuid=uuidd)[0].order_status
    per = request.user.profile.dept
    if per == '总经理' and status_cd <7:
        orders_list.objects.filter(uuid=uuidd).delete()
        messages.success(request,"操作成功")
        return redirect("/flow/")
    elif per == '厂长' and status_cd == 2 or status_cd == 3:
        orders_list.objects.filter(uuid=uuidd).delete()
        messages.success(request,"操作成功")
        return redirect("/flow/")
    elif per == '生产主管' and status_cd == 4 or status_cd == 5:
        orders_list.objects.filter(uuid=uuidd).delete()
        messages.success(request,"操作成功")
        return redirect("/flow/")
    elif per == '仓管' and status_cd == 6 or status_cd == 7:
        orders_list.objects.filter(uuid=uuidd).delete()
        messages.success(request,"操作成功")
        return redirect("/flow/")
    else:
        messages.error(request,per+str(status_cd)+'操作失败：你没有这个权限')
        return redirect("/flow/")



@login_required
def update_order(request,uuidd):
    status_cd = orders_list.objects.filter(uuid=uuidd)[0].order_status
    per = request.user.profile.dept
    if status_cd < 7:
        if per == '总经理' and status_cd <7:
            orders_list.objects.filter(uuid=uuidd).update(order_status=status_cd+1)
            messages.success(request,"操作成功")
            return redirect("/flow/")
        elif per == '厂长' and status_cd == 2 or status_cd ==3:
            orders_list.objects.filter(uuid=uuidd).update(order_status=status_cd+1)
            messages.success(request,"操作成功")
            return redirect("/flow/")
        elif per == '生产主管' and status_cd == 4 or status_cd == 5:
            orders_list.objects.filter(uuid=uuidd).update(order_status=status_cd+1)
            messages.success(request,"操作成功")
            return redirect("/flow/")
        elif per == '仓管' and status_cd == 6 or status_cd == 7:
            orders_list.objects.filter(uuid=uuidd).update(order_status=status_cd+1)
            messages.success(request,"操作成功")
            return redirect("/flow/")
        else:
            messages.error(request,per+str(status_cd)+'操作失败：你没有相应的权限，请联系总经理')
            return redirect("/flow/")
    else:
        messages.warning(request,"该订单已完成")
        return redirect("/flow/")

def roll_back(request,uuidd):
    status_cd = orders_list.objects.filter(uuid=uuidd)[0].order_status
    if status_cd >1:
        orders_list.objects.filter(uuid=uuidd).update(order_status=status_cd-1)
        messages.success(request,"操作成功")
        return redirect("/flow/")
    else:
        return redirect("/flow/")

def status(request,status_cd):
    user_name = request.user.username

    forms = WorkFlowForm()
    tmp_list = []
    stat_1 = orders_list.objects.filter(order_status='1',user_name=user_name).aggregate(count_1=Count('order_status')).get('count_1')
    tmp_list.append(stat_1)
    stat_2 = orders_list.objects.filter(order_status='2',user_name=user_name).aggregate(count_1=Count('order_status')).get('count_1')
    tmp_list.append(stat_2)
    stat_3 = orders_list.objects.filter(order_status='3',user_name=user_name).aggregate(count_1=Count('order_status')).get('count_1')
    tmp_list.append(stat_3)
    stat_4 = orders_list.objects.filter(order_status='4',).aggregate(count_1=Count('order_status')).get('count_1')
    tmp_list.append(stat_4)
    stat_5 = orders_list.objects.filter(order_status='5',user_name=user_name).aggregate(count_1=Count('order_status')).get('count_1')
    stat_6 = orders_list.objects.filter(order_status='6',user_name=user_name).aggregate(count_1=Count('order_status')).get('count_1')
    stat_7 = orders_list.objects.filter(order_status='7',user_name=user_name).aggregate(count_1=Count('order_status')).get('count_1')
    tmp_list.append(stat_5)
    tmp_list.append(stat_6)
    tmp_list.append(stat_7)
    if status_cd:
        results = orders_list.objects.raw("select a.*,b.stat_nam from work_flow_orders_list a left join work_flow_order_stat b on a.order_status = b.stat_cd where a.order_status=%d and a.user_name='%s'" % (status_cd,user_name))
    elif status_cd == 0:
        results = orders_list.objects.raw("select a.*,b.stat_nam from work_flow_orders_list a left join work_flow_order_stat b on a.order_status = b.stat_cd where a.user_name='%s'" % user_name)
    return render(request,'order_list.html',context={"results":results,"count":tmp_list,"form":forms})

def permission_denied(request):
    messages.error(request,'操作失败')
    return render(request,'order_list.html')