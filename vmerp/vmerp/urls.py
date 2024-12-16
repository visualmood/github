"""
URL configuration for vmerp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),                            # 后台管理
    path('', views.home, name='home'),                          # 首页  

    path('authentication/', include('authentication.urls')),    # 认证相关, 登录, 注册, 退出等

    # path('suppliers/', include('suppliers.urls')),              # 供应商管理

    # path('materials/', include('materials.urls')),              # 物料管理

    # path('goods/', include('goods.urls')),                      # 商品管理

    # path('orders/', include('orders.urls')),                    # 订单管理

    # path('procurements/',include('procurements.urls')),         # 采购管理

    # path('production/', include('production.urls')),            # 生产管理

    # path('stock/', include('stock.urls')),                      # 库存管理

    # path('expenses/', include('expenses.urls')),                # 费用管理

    # path('reports/', include('reports.urls')),                  # 报表管理





]
