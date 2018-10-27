from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from .form import LoginForm,UserRegistrationForm,UserEditForm,ProfileEditForm,UserEditForm2,SearchForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import messages
@login_required
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
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Profile update successfully')
        else:
            messages.error(request,'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,'account/edit.html',context={'user_form':user_form,
                                                        'profile_form':profile_form})
def permission_denied(request):
    messages.error(request,'操作失败')
    return render(request,'order_list.html')

@login_required
def edit_2(request):
    search_form = SearchForm()
    if request.user.profile.dept == '总经理':
        if request.method == 'POST':
            ## 需要判断输入账户是否存在
            search_name = request.POST.get('search_name')
            if User.objects.filter(username=search_name):
                user_id = User.objects.filter(username=search_name)[0].id
                user_info = Profile.objects.filter(user_id=user_id)
                return render(request,'account/edit_2.html',context={'user_info':user_info,'search_form':search_form})
            else:
                messages.warning(request,'没有这个用户')
                search_form = SearchForm()
                return render(request,'account/edit_2.html',context={'search_form':search_form})
        else:
            return render(request,'account/edit_2.html',context={'search_form':search_form})
    else:
        messages.warning(request,"你没有权限")
        return redirect("/flow/")

@login_required
def update_per(request,usr_name):
    search_form = SearchForm()
    if request.user.profile.dept == '总经理':
        if request.method == 'POST':
            dept = request.POST.get('dept')
            com = request.POST.get('com')
            user_id = User.objects.filter(username=usr_name)[0].id
            user_info = Profile.objects.filter(user_id=user_id)
            if user_info[0].company != request.user.profile.company and user_info[0].company !='空': ##无法编辑非本公司员工
                messages.error(request,'操作失败：这不是你公司的员工')
                return render(request,'account/edit_2.html',context={'search_form':search_form})
            elif user_info[0].company == '空':
                Profile.objects.filter(user_id=user_id).update(dept=dept,company=com)
                messages.success(request,'修改成功')
                return render(request,'account/edit_2.html',context={'user_info':user_info})
            else:
                Profile.objects.filter(user_id=user_id).update(dept=dept,company=com)
                messages.success(request,'修改成功')
                return render(request,'account/edit_2.html',context={'user_info':user_info})
        else:
            return render(request,'account/edit_2.html',context={'search_form':search_form})
    else:
        return render(request,'account/edit_2.html',context={'search_form':search_form})

