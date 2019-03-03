from django.urls import path
from . import views
from .views import WeiXin
app_name='account'
handler403 = views.permission_denied
wx = WeiXin()
urlpatterns = [
#     path("login/",views.user_login,name='user_login')
#     path('login/',login,name='login'),
#     path('logout/',logout,name='logout'),
#     path('logout-then-login',logout_then_login,name='logout_then_login'),
#     path('password-change/', password_change,name='password_change'),
#     path('password-change/done',password_change_done,name='password_change_done'),
#     path('password-reset/', password_reset,name='password_reset'),
#     path('password-reset-done/',password_reset_done,name='password_reset_done'),
#     path('password-reset-complete/',password_reset_complete,name='password_reset_compelete'),
#     path('password-reset-confirm/',password_reset_confirm,name='password_reset_comfirm'),
#     path('register/',views.register,name='register'),
    path('edit/',views.edit,name='edit'),
    path('people-edit/',views.edit_2,name='edit_2'),
    path('weixin/',wx.weixin,name='weixin'),
    path('',wx.get_usr,name='get_usr'),
    path('add-company/',views.addCompany,name='add_company'),

]
