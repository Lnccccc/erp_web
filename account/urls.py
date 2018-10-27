from django.urls import path
from . import views
from django.contrib.auth.views import login,logout,logout_then_login
from django.contrib.auth.views import password_change_done,password_change,password_reset,password_reset_done,password_reset_complete,password_reset_confirm
app_name='account'
handler403 = views.permission_denied
urlpatterns = [
    #path("login/",views.user_login,name='user_login')
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('logout-then-login',logout_then_login,name='logout_then_login'),
    path('password-change/', password_change,name='password_change'),
    path('password-change/done',password_change_done,name='password_change_done'),
    path('password-reset/', password_reset,name='password_reset'),
    path('password-reset-done/',password_reset_done,name='password_reset_done'),
    path('password-reset-complete/',password_reset_complete,name='password_reset_compelete'),
    path('password-reset-confirm/',password_reset_confirm,name='password_reset_comfirm'),
    path('',views.dashboard,name='dashboard'),
    path('register/',views.register,name='register'),
    path('edit/',views.edit,name='edit'),
    path('people-edit/',views.edit_2,name='edit_2'),
    path('people-edit/<str:usr_name>',views.update_per,name='update_per'),


]
