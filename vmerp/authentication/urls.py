from django.urls import path                            # 导入path函数，因于设置路由              
from django.views.decorators.csrf import csrf_exempt    # 导入csrf_exempt装饰器，用于取消csrf保护，这里用于js中ajax请求，以免报错，使用时在视图函数中加上@csrf_exempt装饰器即可。
from . import views                                     # 导入views模块，用于定义视图函数，能在路由中调用。注册相关的使用CBV视图类，登录相关的使用FBV视图函数   


urlpatterns = [
    # CBV 注册相关视图全部使用《Class-based views》模式，使用as_view()方法来调用。这样代码
    path('register', views.RegisterView.as_view(), name='register'),                                                    # 注册页面 
    path('verify-registeruser',csrf_exempt(views.VerifyRegisterUserView.as_view()), name='verify-registeruser'),        # 实时验证注册的【用户名】是否符合要求
    path('verify-registeremail',csrf_exempt(views.VerifyRegisterEmailView.as_view()), name='verify-registeremail'),     # 实时验证注册的【邮箱】是否符合要求
    path('verify-registerpwd', csrf_exempt(views.VerifyRegisterpwdView.as_view()), name='verify-registerpwd'),          # 实时验证注册的【密码】是否符合要求
    path('get-registercode',views.GetRegisterCodeView.as_view(), name='get-registercode'),                              # 实时获取注册的【验证码】，传递给前端页面验证码图片
    path('activate-account/<int:uid>/<token>/', views.ActivateAccountView.as_view(), name='activate-account'),          # 激活注册账号并跳转到登录页面,token是防止恶意链接操作 

    # FBV 登录相关视图全部使用函数视图模式F《Function-based views》，直接调用函数名。
    path('login', views.login_view, name='login'),                              # 登录页面
    path('verify-loginuser', views.verify_loginuser, name='verify-loginuser'),  # 验证登录页面【用户名】是否符合要求
    path('get-logincode', views.get_logincode, name='get-logincode'),           # 实时获取登录【验证码】，传递给前端页面验证码图片
    path('forget-password', views.forget_password, name='forget-password'),     # 忘记密码页面，发送密码重置链接到邮箱中
    path('reset-password/<int:uid>/<token>/', views.reset_password, name='reset-password'), # 点击密码重置链接后 重置密码页面,token是防止恶意链接的校验

    path('logout', views.logout_view, name='logout'),                           # 注销账号并跳转到登录页面
    path('change-password', views.change_password, name='change-password'),     # 修改密码页面,这个是登录后修改密码的页面(未使用token)，忘记重置密码是登录之前修改，这二个要分清楚。不能混淆，否则乱七八糟。

]