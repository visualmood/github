# 这是主路由文件，负责将各个子应用的路由进行分发，并将其合并到主路由中。
# 并且在settingspy中设置了ROOT_URLCONF = 'vmerp.urls'，如果你要修改主路由，同时settingspy中的ROOT_URLCONF，请务必同时修改。
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),              # 后台管理
    path('', views.home, name='home'),                          # 首页
    path('authentication/', include('authentication.urls')),    # 认证相关, 登录, 注册, 退出等

    # path('suppliers/', include('suppliers.urls')),              # 供应商管理

    # path('materials/', include('materials.urls')),              # 物料管理

    # path('goods/', include('goods.urls')),                      # 商品管理

    # path('orders/', include('orders.urls')),                    # 订单管理

    # path('purchases/',include('purchases.urls')),               # 采购管理

    # path('production/', include('production.urls')),            # 生产管理

    # path('stock/', include('stock.urls')),                      # 库存管理

    # path('expenses/', include('expenses.urls')),                # 费用管理

    # path('reports/', include('reports.urls')),                  # 报表管理



]
