from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from .form import ProfileEditForm,SearchForm,WxUserEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile,WeixinUser,Company
from django.contrib import messages
import hashlib
import requests
import time
import json
re = requests
re.encoding='utf-8'
def is_login(self,request):
    return request.session.get('islogin',False)

#
# def dashboard(request):
#     return render(request,'account/dashboard.html',{'section':'dashboard'})
# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(username=cd['username'],password=cd['password'])
#             if user is not None :
#                 if user.is_active:
#                     login(request,user)
#                     return HttpResponse('Authenticated successfuly')
#                 else:
#                      return HttpResponse('Disabled account')
#             else:
#                 return HttpResponse('Invalid login')
#     else:
#         form = LoginForm()
#     return render(request,'account/login.html',context={"form":form})
#
# def register(request):
#     if request.method == 'POST':
#         user_form = UserRegistrationForm(request.POST)
#         if user_form.is_valid():
#             new_user = user_form.save(commit=False)
#             new_user.set_password(user_form.cleaned_data['password'])
#             new_user.save()
#             profile = Profile.objects.create(user=new_user)
#             return render(request,'account/register_done.html',context={'new_user':new_user})
#     else:
#         user_form = UserRegistrationForm()
#     return render(request,'account/register.html',context={'user_form':user_form})

def edit(request): #姓名编辑页面
    try:
        wxu = WeixinUser.objects.get(openid=request.session.get('openid','null'))
        profile = wxu.profile
    except:
        pass
    if request.method == 'POST':
        profile_form = ProfileEditForm(instance=profile,data=request.POST)
        if  profile_form.is_valid() and profile_form.cleaned_data['realname'] != '空':
            profile_form.save()
            request.session['dept'] = profile.dept
            request.session['company'] = profile.company.name
            request.session['realname'] = profile.realname
            return redirect('/flow/')
        else:
            return render(request, 'account/edit.html', context={'profile_form': profile_form})
    else:
        profile_form = ProfileEditForm(instance=profile)
        return render(request,'account/edit.html',context={'profile_form':profile_form})


def permission_denied(request):
    messages.error(request,'操作失败')
    return render(request,'order_list.html')

def edit_2(request): #企业人员权限编辑页面
    if request.method == 'GET':
        if request.session.get('dept') == '总经理':
            membs = Company.objects.get(name=request.session.get('company')).membs.all()
            return render(request, 'account/edit_2.html', {'membs': membs})
        else:
            HttpResponse("你没有权限")
    elif request.method == 'POST':
        membs = Company.objects.get(name=request.session.get('company')).membs.all()
        for i in membs:
            realname = i.realname
            dept = request.POST.get(realname)
            Profile.objects.filter(realname=realname).update(dept=dept)
            if realname == request.session.get('realname'):
                request.session['company'] = dept;
            else:
                pass
        membs = Company.objects.get(name=request.session.get('company')).membs.all()
        return render(request,'account/edit_2.html',{'membs':membs})

def addCompany(request):
    return HttpResponse("None")

class WeiXin():
    def __init__(self):
        self.appid='wxec4567a41338530d'
        self.secret = 'f81a45edfb0ebb4607c8441fac0876d9'
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
        self.url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code" % (self.appid,self.secret,self.cd) #用于调用网页授权登陆接口的api
        self.ass_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (self.appid,self.secret) #用于调用微信接口的api
        self.raw = re.get(self.url).json()
        self.raw_access_token = re.get(self.ass_url).json()
        access_token = self.raw_access_token['access_token'] #用于调用微信接口
        ass_tok = self.raw['access_token'] #用于网页授权登陆和获取用户基本信息
        open_id = self.raw['openid']
        self.usr_url = 'https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN' % (ass_tok,open_id)
        self.info_raw = re.get(self.usr_url).json()
        self.nickname = self.info_raw['nickname']
        self.city = self.info_raw['city']
        self.sex = self.info_raw['sex']
        self.all_user = self.get_all_user()
        if open_id in self.all_user:
            if request.session['realname'] != '空':
                request.session['islogin'] = True
                self.wx_user = WeixinUser.objects.filter(openid=open_id)[0]
                request.session['openid'] = open_id
                request.session['nickname'] = self.nickname
                request.session['dept'] = self.wx_user.profile.dept
                request.session['company'] = self.wx_user.profile.company.name
                request.session['realname'] = self.wx_user.profile.realname
                request.session['ass_tok'] = ass_tok
                request.session['access_tok'] = access_token
                return redirect('/flow/')
            else:
                 request.session['openid'] = open_id
                 request.session['nickname'] = self.nickname
                 request.session['ass_tok'] = ass_tok
                 return redirect('/account/edit/')
        else:
            wxu = WeixinUser(openid=open_id,nickname=self.nickname,sex=self.sex,city=self.city)
            wxu.save()
            Profile.objects.create(user=wxu)
            request.session['islogin'] = True
            request.session['openid'] = open_id
            request.session['ass_tok'] = ass_tok
            request.session['nickname'] = self.nickname
            request.session['company'] = '示例企业'
            return redirect('/account/edit/') ##初次登陆时没有设置session因此在edit页面无法获取session的openid等内容

