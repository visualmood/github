本人胡工于2024年12月12日终于学会git同步个人电脑上代码到线上Github平台仓库.
现在开始使用git同步线上仓库与本地代码，本地往线上用推git push  ,线上往本地用拉取git pull

线上代码仓库位于visualmoot/github目录下，
在git窗口，进入d:/,然后运行  
git clone https://github.com/visualmood/github.git创建github目录,

本地代码位于d:/github目录下,目录下.git文件夹一定不能移动，删除，修改！否则不能使用。
个人电脑主要是做一个django项目，管理公司货品，商品管理，物料管理，订单管理，采购管理，生产管理，销售管理，库存管理等

项目名称：vmerp，
目录位置：D:\github

1、创建虚拟环境：
在vmerp文件目录窗口地址栏输入cmd,在命令行输入 python -m venv env

2、激活虚拟环境：
在cmd命令行输入D:\github\env\Scripts\activate 或  .\env\Scripts\activate

3、在命令行中以(env) D:\github>  开头，表明已经进入虚拟环境
创建requirement.txt,将各种依赖包名写入文件中，一行只能写一个包名
后期上线可以使用 pip install -r requirements.txt 来批量安装依赖包
用清华源来安装比较快。
pip install django --index-url https://pypi.tuna.tsinghua.edu.cn/simple


4、在虚拟环境目录(env) D:\github>  输入创建django-admin命令
(env) D:\github>     django-admin startproject vmerp
执行命令后，会自动在github文件夹中创建一个vmerp文件夹

5、进入刚才创建的项目的目录中，然后看到一个vmerp文件夹和一个manage.py文件
(env) D:\github>cd vmerp
(env) D:\github\vmerp>python manage.py runserver

6、运行完后，按键盘Ctrl并点击 http://127.0.0.1:8000/

Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
December 14, 2024 - 15:06:05
Django version 5.1.2, using settings 'vmerp.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
出现：The install worked successfully! Congratulations!，表明django项目创建成功了

7、设置setting.py,

8、设置路由urls.py,增加一个views.py视图函数


9、创建应用
(env) D:\github\vmerp>django-admin startapp authentication



后面略


