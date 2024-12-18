# authentication/views.py文件用于处理用户登录、注册、注销等操作，包括登录页面视图函数、注册页面视图函数、注销退出页面视图函数。
##############################################################################################
# 导入相关模块的顺序，一般是：1、python内置模块；2、django模块；3、第三方模块；4、自己编写的模块。
# 1、python内置模块，
import json                                                        # 导入json模块，用于jscript中能够处理json数据 
from threading import Thread                                       # 导入Thread模块，用于异步处理，这里发送邮件是异步处理
# 2、django模块，
from django.conf import settings                                    # 导入settings模块，用于获取settings.py中的配置信息
from django.views import View                                       # 导入View类，用于定义视图类
from django.shortcuts import resolve_url, render,redirect,HttpResponse,get_object_or_404    # 导入render函数，用于渲染模板文件
from django.http import HttpResponse                                # 导入HttpResponse类，用于返回响应对象
from django.db.models import Q                                      # 导入Q类，用于构建复杂的查询条件
from django.contrib import messages                                 # 导入messages模块   
from django.contrib.auth.models import User                         # 导入User模型类，用于处理用户信息
from django.contrib.auth import authenticate, login, logout         # 导入authenticate、login、logout函数，用于用户登录、注册、注销
from django.contrib.sites.shortcuts import get_current_site         # 导入get_current_site方法，用于获取当前站点的域名,以免用其它端口时报错。
from django.contrib.auth.tokens import default_token_generator      # 导入default_token_generator方法，用于生成token
from django.contrib.auth.decorators import login_required           # 导入login_required装饰器，用于验证用户是否登录
from django.core.mail import send_mail                              # 导入send_mail方法，用于发送邮件，要在seeting.py中配置EMAIL_BACKEND                  
from django.http.request import HttpRequest                         # 导入HttpRequest类
from django.http.response import JsonResponse                       # 导入JsonResponse类，返回json数据，主要是在ajax中使用校验输入用户名、邮箱是否合法
from django.http.response import HttpResponseBadRequest, FileResponse# 导入HttpResponseBadRequest类，用于返回400错误，FileResponse类，用于返回文件下载
#3、第三方模块，
import email_validator as ev                                        # 导入email_validator模块，用于验证邮箱格式有二个方法：validate_email, EmailNotValidError
# 4、自己编写的模块。
from .forms import RegisterForm,LoginForm                   # 导入注册表单类RegisterForm和登录表单类LoginForm
from .utils import generate_verify_code,get_client_ip       # 导入生成验证码函数generate_verify_code和获取客户端IP地址函数get_client_ip
################################################################################################
# 注册相关视图类共 <7> 个,这是基于CBV的视图类，继承自View类，类命名规则为驼峰命名法，类名首字母大写，以表示其是一个类视图。定义def get()和def post()方法，分别处理GET和POST请求。
# 本视图类用于处理用户注册，包括注册页面的渲染，注册验证，注册成功后跳转到登录页面。
# 新注册用户账号初始默认为未激活状态，需要通过邮件激活才能登录。注册后成功后自动发送一封邮件通知注册用户在邮件中激活账号。在邮件中放上链接，点击链接激活账号。
class RegisterView(View):                                         # 定义视图类RegisterView，继承自View类，类命名规则为驼峰命名法，类名首字母大写，以表示其是一个类视图。
    def get(self, request):                                       # 定义get方法，用于处理GET请求，有二个参数，self表示视图对象，request表示请求对象。
        form_obj=RegisterForm()                                   # 实例化RegisterForm表单类
        return render(request, 'authentication/register.html', {'form':form_obj})   # 渲染注册页面authentication/register.html，并传递表单对象form_obj到模板中。    
    def post(self, request):                                      # 定义post方法，用于处理POST请求，有二个参数，self表示视图对象，request表示请求对象。
        form_obj=RegisterForm(request.POST)                       # 实例化RegisterForm表单类，并传入请求对象request.POST作为参数,结果存储在form_obj对象中
        # 验证表单数据是否合法,如果验证成功创建对象保存数据,from表单会自动验证数据的合法性，下面业务逻辑只需要判断是否为空
        if form_obj.is_valid():                                   # 验证表单数据成功返回True，否则返回False
            username=form_obj.cleaned_data.get('username')        # 获取用户名,从form_obj对象中获取cleaned_data字典，中的键对应的value值
            email=form_obj.cleaned_data.get('email')              # 获取邮箱,从form_obj对象中获取cleaned_data字典，中的键对应的value值
            password=form_obj.cleaned_data.get('password')        # 获取密码，从form_obj对象中获取cleaned_data字典，中的键对应的value值，字典取值 get方法不会报错，如果不存在，返回None
            verify_code=request.POST.get('verify_code')           # 获取验证码，从请求对象request.POST中获取verify_code值


            print('-----------verify_code:',verify_code)
            print('-----------session:',request.session.get('verify_code'))

            if verify_code.lower() != request.session.get('verify_code').lower():  # 验证验证码是否正确
                messages.error(request, '验证码错误！请重新输入！')  # 验证码错误，提示错误信息
                context={
                    'username':request.POST.get('username'),       # 获取注册页面提交的用户名
                    'email':request.POST.get('email'),             # 获取注册页面提交的邮箱
                    'form_obj': form_obj,                          # 实例化的表单类对象,主要是为了在注册页面显示错误信息（form_obj.errors），并回显用户填写的内容
                }
                return render(request, 'authentication/register.html', context)  # 将输入的username、email值回显到注册页面，并提示验证码错误
            user=User(username=username, email=email)             # 实例化User模型类对象user，设置username、email属性值
            user.set_password(password)                           # 设置密码,set_password()方法加密密码,如果直接设置密码，密码将明文存储在数据库中
            user.is_active=False                                  # 注册用户账号初始 默认未激活状态，需要通过邮件激活才能登录
            user.save()                                           # 保存用户信息到数据库


            print('-----------user:',user)

            # 初始化邮件参数主题，内容，发件人，收件人，失败静默。配置邮件中链接的token参数
            current_site=get_current_site(request).domain       # 获取当前站点的域名，用于发送邮件 get_current_site(request)方法，用于获取当前站点的域名, .domain属性获取域名
            token=default_token_generator.make_token(user)      # 生成token，default_token_generator对象，make_token方法生成token，参数为用户对象user   
            reurl=resolve_url('activate-account', user.pk, token)# 拼接激活链接 resolve_url()方法，用于获取视图函数的URL,参数为路由别名name，用户id，token
            link=f'http://{current_site}{reurl}'                # 拼接激活链接
            # print(f'-----------url：{link}')
            subject=f"激活账号 [VisaulMood管理系统] "              # 定义邮件主题，赋值给subject变量                                                                
            message=f'''尊敬的《{user.username}》用户，欢迎注册 [Viusalmood管理系统] ，请点击下面的链接激活您的账号：\n \n  
            激活链接（或点不开请复制到浏览器打开）：\n              {link} \n\n\n   点击链接激活账号后，您就可以登录系统了。 ''' # 定义邮件内容，赋值给message变量。这里的{user.pk}和{token}是激活链接中需要用到的参数，{current_site}是当前站点的域名，注意下面拼接形式
            
            print('*'*99)

            print('-----------link:',link)
            # 异步发送邮件，优化注册流程，提高用户体验,先定义一个异步函数send_email，然后再调用该函数，异步发送邮件，优化注册流程
            def send_email(user):                           # 定义一个异步函数send_email，用于发送邮件 外层是send_email函数，里层是send_mail函数，这个是django的异步发送邮件的写法,区别是一个字母e
                send_mail(                                  # 调用django.core.mail.send_mail函数，用于发送邮件   
                    subject = subject,
                    message = message,
                    from_email = settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False,)
            # 创建一个线程，并将异步函数send_email和user对象作为参数传递给线程，启动线程
            try:
                t = Thread(target=send_email, args=(user,))     # 创建一个线程，并将异步函数send_email和user作为参数传递给线程，启动线程
                t.start()                                       # 启动线程
                msg=f'您好，尊敬的新用户： 《 {user.username} 》 ，恭喜你注册成功！ 请打开邮箱激活账号再登录！ 邮箱地址：{user.email}'
                return HttpResponse(msg)                         # 注册成功，返回注册成功信息到前端，并跳转到登录页面。        
            except Exception as e:
                msg=f'  您好，尊敬《{user.username}》用户，我们向邮箱【{user.email}】发送邮件失败，无法激活账户，请联系管理员！错误信息:{e}'
                return HttpResponse(msg)                                                    

        # 验证表单失败，返回注册页面并提示错误信息
        else:
            messages.error(request, '注册失败！请检查填写的内容是否正确！重新注册！')
            context={
                'username':request.POST.get('username'),               # 获取注册页面提交的用户名
                'email':request.POST.get('email'),                     # 获取注册页面提交的邮箱
                'form_obj': form_obj,                                  # 实例化的表单类对象,主要是为了在注册页面显示错误信息（form_obj.errors），并回显用户填写的内容
            }
            return render(request, 'authentication/register.html', context)   # 渲染注册页面authentication/register.html，并传递表单对象form_obj到模板中。

# 实时验证注册界面的用户名是否已存在，如果已存在，则提示错误信息，如果不存在，则返回True。利用js来监听输入，调用对应接口，验证用户名是否存在。
class VerifyRegisterUserView(View):
    def post(self, request):                                     # post方法，用于实时验证用户名是否为空或已存在，并且增加AJAX局部刷新效果。
        data = json.loads(request.body)                          # 解析请求体数据，body是页面request.body中的数据，这里是json格式
        username = data['username'].strip()                      # 获取请求参数中的用户名，并去除前后空格
        if not username:
            return JsonResponse({'status': 'error', 'msg': '用户名不能为空'}, status=401)        
        if  not username[0].isalpha():
            return JsonResponse({'status': 'error', 'msg': '用户名要以字母开头，不能以数字开头'}, status=401)        
        if len(username) < 4 or len(username) > 20:
            return JsonResponse({'status': 'error', 'msg': '用户名长度必须在4到20个字符之间'}, status=401)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'msg': '用户名已存在'}, status=401)        
        else:
            return JsonResponse({'status': 'success', 'msg': '用户名可用'},status=200)

# 实时验证注册界面的邮箱是否已存在，如果已存在，则提示错误信息，如果不存在，则返回True。利用js来监听输入，调用对应接口，验证邮箱是否存在。
class VerifyRegisterEmailView(View):
    def post(self, request):                                     # post方法，用于实时验证邮箱是否为空或已存在，并且增加AJAX局部刷新效果。
        data = json.loads(request.body)                          # 获取请求参数中的数据,
        email = data.get('email', '').strip()                    # 获取请求参数中email字段值，并去除前后空格
        # 邮箱是否为空或字符数是否8-50个字符，在forms.py中已经有验证，这里不再重复验证
        try:                                                    # 尝试使用email_validator模块验证邮箱格式是否正确 
            ev.validate_email(email)                            # 验证邮箱格式是否正确,如果from email_validator import validate_email 这样导入email_validator模块，直接调用validate_email的方法与本函数同名，则运行报错，此处用ev.validate_email(email)来调用,
        except ev.EmailNotValidError:                           # 如果邮箱格式不正确，返回错误信息    
            return JsonResponse({'status': 'error', 'msg': '邮箱如果不正确，无法激活账号，邮箱正确格式为：xxx@xxx.xxx'}, status=401)        
        if User.objects.filter(email=email).exists():           # 如果邮箱已存在，返回错误信息
            return JsonResponse({'status': 'error', 'msg': '邮箱已存在，如果邮箱不正确，无法激活账号，请更换邮箱注册'}, status=401)        
        else:
            return JsonResponse({'status': 'success', 'msg': '此邮箱可用'},status=200)

# 实时验证注册界面的密码是否为空或格式是否正确，利用js来监听输入，调用对应接口，验证密码是否为空或字符是否合格
class VerifyRegisterpwdView(View):        
    def post(self, request):                                     # post方法，用于实时验证密码是否为空或格式是否正确，并且增加AJAX局部刷新效果。    
        data = json.loads(request.body)                          # 解析请求体数据，body是页面request.body中的数据，这里是json格式
        password = data.get('password', '').strip()              # 获取请求参数中的密码字段值，并去除前后空格
        if not password:
            return JsonResponse({'status': 'error', 'msg': '密码不能为空'}, status=401)        
        if len(password) < 6 or len(password) > 20:
            return JsonResponse({'status': 'error', 'msg': '密码长度必须在6到20个字符之间'}, status=401)        
        else:
            return JsonResponse({'status': 'success', 'msg': '密码格式正确'},status=200)

# 生成注册验证码图片 的视图类，用于生成注册码图片返回给前端，并将注册码存入session中，供注册页面使用。
class GetRegisterCodeView(View):
    def get(self, request):                                      # 定义get方法，用于处理GET请求，返回注册码图片。并将注册码存入session中，供注册页面使用。                             
        verify_code, buf = generate_verify_code()                # 生成验证码，验证码verify_code，和图片数据buf
        request.session['verify_code'] = verify_code             # 将验证码存入session中,后面可以使用request.session.get('verify_code')获取验证码
        return HttpResponse(buf, content_type='image/gif')       # 返回验证码图片，content_type指定返回图片类型为gif格式

# 激活账号视图类，用于点击邮箱中的链接，激活用户账号，激活成功后跳转到登录页面。
class ActivateAccountView(View):   
    def get(self, request, uid, token):                           # 定义get方法，用于处理GET请求，有三个参数，self表示视图对象，request表示请求对象，pk表示用户id，token表示激活token                      
        user = get_object_or_404(User, pk=uid)                    # 获取用户对象，如果获取不到用户对象，返回404错误页面

        print('-----activate_account:',user.username,'\n-----------这是激活账号的视图函数，这里打印只是为了测试,看未激活之前的效果，之前状态：',user.is_active)

        if not default_token_generator.check_token(user, token):    # 验证token是否有效,利用django.contrib.auth.tokens.default_token_generator对象, check_token方法验证token是否有效，参数为用户对象user和token
            return HttpResponseBadRequest('非法的请求！获取的token无效！请一定要通过邮件链接激活账号！否则这是恶意请求！')

        if not user.is_active:
            user.is_active = True
            user.save()

        print('-----activate_account:',user.username,'\n-----------这是激活账号的视图函数，这里打印只是为了测试,看激活之后的效果，之后状态：',user.is_active) 

        messages.success(request, '您的账号已激活，请登录！')
        return render(request, 'authentication/login.html',{'username':user.username})


# 下面是登录相类的视图函数 --FBV ,共计 <6> 个，1登录，2登录图片码，3实时验证用户名，4忘记密码，5重置密码，6退出登录。
################################################################################################
# 登录页面视图函数
def login_view(request):
    if request.method == 'GET':
        form_obj = LoginForm()
        return render(request, 'authentication/login.html', {'form_obj': form_obj})
    if request.method == 'POST':
        form_obj = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        verify_code = request.POST.get('verify_code')
        if not form_obj.is_valid():
            messages.error(request, '登录失败！请输入正确的用户名和密码！')
            return render(request, 'authentication/login.html', {'form_obj': form_obj})
        if not request.session.get('verify_code'):
            messages.error(request, '验证码已失效！请重新输入！')
            return render(request, 'authentication/login.html', {'form_obj': form_obj})
        if verify_code.lower() != request.session.get('verify_code').lower():
            messages.error(request, '验证码错误！请重新输入！')
            return render(request, 'authentication/login.html', {'form_obj': form_obj})
        user = authenticate(username=username, password=password)
        if not user:
            messages.error(request, '登录失败！请输入正确的用户名和密码！')
            return render(request, 'authentication/login.html', {'form_obj': form_obj})
        if not user.is_active:
            messages.error(request, '登录失败！您的账号未激活！请先激活账号！')
            return render(request, 'authentication/login.html', {'form_obj': form_obj})
        login(request, user)
        messages.success(request, '登录成功！欢迎回来！')

        print('-'*99)
        print('username:',request.POST.get('username'))
        print('password:',request.POST.get('password'))
        print('verify_code:',request.POST.get('verify_code'))
        print('authenticate user is success!')

        return redirect(to='home')

# 生成登录验证码图片，并将验证码存入session中，供登录页面使用。
def get_logincode(request):
    verify_code, buf = generate_verify_code()           # 生成验证码，验证码verify_code，和图片数据buf
    request.session['verify_code'] = verify_code        # 将验证码存入session中,后面可以使用request.session.get('verify_code')获取验证码
    return HttpResponse(buf, content_type='image/gif')  # 返回验证码图片，content_type指定返回图片类型为gif格式

# 实时验证登录界面的输入的用户名是否存在，将数据用json格式传递前端，利用js来监听输入，调用对应接口，验证用户名是否存在。
def verify_loginuser(request):
    data=json.loads(request.body)                        # 解析请求体数据，body是页面request.body中的数据，这里是json格式
    username=data['username'].strip()                    # 获取请求参数中的用户名，并去除前后空格
    # 利用js监听输入，调用verify_registeruser接口，验证用户名是否存在并实时反馈结果
    if not username:
        return JsonResponse({'status': 'error', 'msg': '用户名不能为空'}, status=401)
    if  not username[0].isalpha():
        return JsonResponse({'status': 'error', 'msg': '用户名要以字母开头，不能以数字开头'}, status=401)
    if len(username) < 4 or len(username) > 20:
        return JsonResponse({'status': 'error', 'msg': '用户名长度必须在4到20个字符之间'}, status=401)
    if User.objects.filter(username=username).exists():
        return JsonResponse({'status': 'error', 'msg': '用户名不存在'}, status=401)
    else:
        return JsonResponse({'status': 'success', 'msg': '用户名可用'},status=200)

# 登录时忘记密码，发送密码重置的 链接到邮箱的视图函数
def forget_password(request):
    if request.method == 'GET':
        return render(request, 'authentication/forget-password.html')
    if request.method == 'POST':
        email = request.POST.get('email')                                       # 获取输入的邮箱
        username = request.POST.get('username')                                 # 获取输入用户名    
        user = User.objects.filter(Q(email=email)|Q(username=username)).first() # 根据用户名或邮箱查询用户对象是否存在,Q()方法用于创建查询条件相当于or,只要有一个条件满足即可执行查询。
        if not user:                                                            # 如果用户不存在     
            messages.error(request, '输入用户名或邮箱不存在！请至少要输入一个正确才能重置密码！')
            return render(request, 'authentication/forget-password.html')
        
        # 初始化邮件参数主题，内容，发件人，收件人，失败静默。配置邮件中链接的token参数
        token=default_token_generator.make_token(user)      # 生成token，default_token_generator对象，make_token方法生成token，参数为用户对象user  
        current_site=get_current_site(request).domain       # 获取当前站点的域名，用于发送邮件 get_current_site(request)方法，用于获取当前站点的域名, .domain属性获取域名 
        reurl=resolve_url('reset-password', user.pk, token)# 拼接激活链接 resolve_url()方法，用于获取视图函数的URL,三个参数为路由别名name，用户id，token
        link=f'http://{current_site}{reurl}'                # 拼接激活链接
        subject=f"找回密码 [VisaulMood管理系统] "              # 定义邮件主题，赋值给subject变量                                                                
        message=f'''尊敬的《{user.username}》用户，您好！您正在申请找回密码，请点击下面的链接重置您的密码：\n \n 
            重置密码链接：{link} \n\n      如果链接无法打开，请复制url到浏览器打开。 \n\n重置密码后，您就可以使用新密码登录系统了。 '''

        # 定义异步发送邮件函数，参数为用户对象user，内层函数send_mail()引用外层user对象参数。
        def send_email(user):
            send_mail(                                  # 调用django.core.mail.send_mail函数，用于发送邮件   
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,)

        # 异步发送邮件
        try:
            t=Thread(target=send_email,args=(user,))
            t.start()
            msg=f'  您好，尊敬的《{user.username}》用户，我们已向您发送了一封重置密码的邮件， 请打开邮箱重置密码再登录！ 邮箱地址：{user.email}'
            return HttpResponse(msg) 
        except Exception as e:
            msg=f'  您好，尊敬《{user.username}》用户，我们向邮箱【{user.email}】发送邮件失败，请检查邮箱地址是否正确！错误信息:{e}'
            return HttpResponse(msg)  

# 点击邮箱中重置密码链接，重置密码的视图函数
def reset_password(request, uid, token):
    user=get_object_or_404(User,pk=uid)                             # 获取用户对象，通过用户id获取用户对象，get_object_or_404()方法，如果用户不存在，返回404错误页面
    context={'uid':uid, 'token':token, 'username':user.username}
    if request.method == 'GET':
        if not default_token_generator.check_token(user, token):    # 验证token是否有效,利用django.contrib.auth.tokens.default_token_generator对象, check_token方法验证token是否有效，参数为用户对象user和token
            return HttpResponseBadRequest('非法的请求！获取的token无效！请一定要通过邮件链接重置密码！否则这是恶意请求！')
        return render(request, 'authentication/reset-password.html', context)  
      
    if request.method == 'POST': 
        password1 = request.POST.get('password')                                 # 获取输入的密码
        password2 = request.POST.get('confirm_password')                         # 获取输入的确认密码
        if len(password1) < 6 or len(password1) > 20:                            # 验证密码长度是否在6到20个字符之间
            messages.error(request, '密码长度必须在6到20个字符之间！')             # 密码长度不符合要求，提示错误信息
            return render(request, 'authentication/reset-password.html',context) # 返回密码重置页面        
        if password1 != password2:                                               # 验证两次输入的密码是否一致
            messages.error(request, '两次输入的密码不一致！')                      # 两次输入的密码不一致，提示错误信息
            return render(request, 'authentication/reset-password.html',context) # 返回密码重置页面
        
        user.set_password(password1)                                    # 设置密码,set_password()方法加密密码,如果直接设置密码，密码将明文存储在数据库中
        user.save()                                                     # 保存用户信息到数据库 
        messages.success(request, '密码重置成功！请使用新密码登录系统！')  # 提示密码重置成功信息
        return redirect(to='login')                                     # 重定向到登录页面

# 注销退出页面视图函数
def logout_view(request):
    logout(request)                      # 注销用户
    request.session.flush()              # 清除session
    response = redirect('login')         # 重定向到登录页面
    response.delete_cookie('sessionid')  # 删除cookie
    return response                      # 返回响应对象

# 修改密码视图函数,这个必须是登录用户才可以访问，所以需要判断用户是否登录，如果用户未登录，则返回登录页面。
def change_password(request):
    user=request.user                                       # 获取当前登录用户对象
    if not user.is_authenticated:                           # 如果用户未登录，返回登录页面
        return redirect('login')
    if request.method == 'GET':
        return render(request, 'authentication/change-password.html')
    if request.method == 'POST':
        old_password = request.POST.get('old_password')     # 获取输入的旧密码
        new_password1 = request.POST.get('new_password1')   # 获取输入的新密码
        new_password2 = request.POST.get('new_password2')   # 获取输入的确认密码
        if not user.check_password(old_password):           # 验证旧密码是否正确
            messages.error(request, '旧密码错误！请重新输入！')
            return render(request, 'authentication/change-password.html')
        if len(new_password1) < 6 or len(new_password1) > 20:  # 验证新密码长度是否在6到20个字符之间
            messages.error(request, '新密码长度必须在6到20个字符之间！')
            return render(request, 'authentication/change-password.html')
        if new_password1 != new_password2:                      # 验证两次输入的密码是否一致
            messages.error(request, '两次输入的密码不一致！')
            return render(request, 'authentication/change-password.html')
        user.set_password(new_password1)                        # 设置新密码
        user.save()                                             # 保存用户信息到数据库
        messages.success(request, '密码修改成功！请使用新密码登录系统！')  # 提示密码修改成功信息
        return redirect(to='login')                             # 重定向到登录页面