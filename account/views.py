from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from .form import LoginForm,UserRegistrationForm,ProfileEditForm,SearchForm,WxUserEditForm
from django.contrib.auth.decorators import login_required
from .models import WeixinUser
from .models import Profile
from django.contrib import messages
import hashlib
import requests
from .models import WeixinUser
import json
re = requests

def is_login(self,request):
    return request.session.get('islogin',False)


def dashboard(request):
    return render(request,'account/dashboard.html',{'section':'dashboard'})
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],password=cd['password'])
            if user is not None :
                if user.is_active:
                    login(request,user)
                    return HttpResponse('Authenticated successfuly')
                else:
                     return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request,'account/login.html',context={"form":form})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            return render(request,'account/register_done.html',context={'new_user':new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'account/register.html',context={'user_form':user_form})

def edit(request):
    wxu = WeixinUser.objects.get(openid=request.session.get('openid','null'))
    profile = wxu.profile
    if request.method == 'POST':
        #user_form = WxUserEditForm(instance=wxu,data=request.POST)
        profile_form = ProfileEditForm(instance=profile,data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            profile_form.save()
            messages.success(request,'Profile update successfully')
        else:
            messages.error(request,'Error updating your profile')
        request.session['dept'] = profile.dept
        request.session['company'] = profile.company
        return redirect('/flow/')
    else:
        profile_form = ProfileEditForm()
        return render(request,'account/edit.html',context={'profile_form':profile_form})


def permission_denied(request):
    messages.error(request,'操作失败')
    return render(request,'order_list.html')

def edit_2(request):
    search_form = SearchForm()
    staff_list = []
    if request.session.get('dept') == '总经理':
        if request.method == 'POST':
            ## 需要判断输入账户是否存在
            search_name = request.POST.get('staff')
            if Profile.objects.get(real_name=search_name):
                user_info = Profile.objects.get(real_name=search_name)
                return render(request,'account/edit_2.html',context={'user_info':user_info,'search_form':search_form})
            else:
                messages.warning(request,'没有这个用户')
                search_form = SearchForm()
                return render(request,'account/edit_2.html',context={'search_form':search_form})
        else:
            for i in Profile.objects.filter(company=request.session.get('company')):
                staff_list.append(i.real_name)
            return render(request,'account/edit_2.html',context={'search_form':search_form,'staff_list':staff_list})
    else:
        messages.warning(request,"你没有权限")
        return redirect("/flow/")

def update_per(request,usr_name):
    search_form = SearchForm()
    staff_list = []
    if request.session.get('dept') == '总经理':
        if request.method == 'POST':
            dept = request.POST.get('dept')
            com = request.POST.get('com')
            user_info = Profile.objects.get(real_name=usr_name)
            if user_info.company != request.session.get('company') and user_info.company !='空': ##无法编辑非本公司员工
                messages.error(request,'操作失败：这不是你公司的员工')
                return render(request,'account/edit_2.html',context={'search_form':search_form})
            elif user_info.company == '空' or user_info.company == request.session.get('company'):
                for i in Profile.objects.filter(company=request.session.get('company')):
                    staff_list.append(i.real_name)
                Profile.objects.filter(real_name=usr_name).update(dept=dept,company=com)
                messages.success(request,'修改成功')
                return render(request,'account/edit_2.html',context={'user_info':user_info,'staff_list':staff_list})
        else:
            return render(request,'account/edit_2.html',context={'search_form':search_form})
    else:
        return render(request,'account/edit_2.html',context={'search_form':search_form})

class WeiXin():
    def __init__(self):
        self.appid='wxf6d9517d8a850ecd'
        self.secret = '177546a750a8c8d12e45f94f39c18a61'
        self.all_user = []

    def get_all_user(self):
        for i in WeixinUser.objects.all():
            self.all_user.append(i.openid)
        return self.all_user

    def get_token(self):
        self.raw = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (self.appid,self.secret)
        token=re.get(self.raw).json()['access_token']


    def weixin(self,request):
        self.signature = request.GET.get('signature')
        self.timestamp = request.GET.get('timestamp')
        self.nonce = request.GET.get('nonce')
        self.echostr = request.GET.get('echostr')
        self.token = 'xincheng'
        self.tmpraw = [self.token,self.timestamp,self.nonce]
        self.raw = ("").join(sorted(self.tmpraw))
        self.hash_raw_tmp = hashlib.sha1(bytes(self.raw,encoding='utf-8'))
        self.hash_raw = self.hash_raw_tmp.hexdigest()
        if self.hash_raw == self.signature:
            return HttpResponse(self.echostr)
        else:
            return False


    def get_usr(self,request):
        self.cd = request.GET.get('code')
        self.url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code" % (self.appid,self.secret,self.cd)
        self.raw = re.get(self.url).json()
        ass_tok = self.raw['access_token']
        open_id = self.raw['openid']
        self.usr_url = 'https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN' % (ass_tok,open_id)
        self.info_raw = re.get(self.usr_url).json()
        self.nickname = self.info_raw['nickname']
        self.city = self.info_raw['city']
        self.sex = self.info_raw['sex']
        self.all_user = self.get_all_user()
        if open_id in self.all_user:
            request.session['islogin'] = True
            request.session['openid'] = open_id
            request.session['nickname'] = self.nickname
            self.wx_user = WeixinUser.objects.filter(openid=open_id)[0]
            request.session['dept'] = self.wx_user.profile.dept
            request.session['company'] = self.wx_user.profile.company
            return redirect('/flow/')
        else:
            wxu = WeixinUser(openid=open_id,nickname=self.nickname,sex=self.sex,city=self.city)
            wxu.save()
            Profile.objects.create(user=wxu)
            request.session['islogin'] = True
            request.session['openid'] = open_id
            request.session['nickname'] = self.nickname
            
            return redirect('/account/edit/') ##初次登陆时没有设置session因此在edit页面无法获取session的openid等内容

