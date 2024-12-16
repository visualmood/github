from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),                 # 登录页面
    path('logout/', views.logout_view, name='logout'),              # 登出页面
    path('register/', views.register_view, name='register'),        # 注册页面

]