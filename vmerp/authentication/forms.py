# forms.py文件中定义了注册表单类RegisterForm和登录表单类LoginForm,用于处理前端页面输入时页面的校对和验证。
from django import forms                                # 导入forms模块 
from django.contrib.auth.models import User             # 导入User模型 
from django.contrib import auth                         # 导入auth模块 
import re

# 定义注册表单类
class RegisterForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=20)             # 定义用户名字段，长度限制为4-20个字符
    email = forms.EmailField(required=False)                            # 定义邮箱字段  重置密码时验证没有这个字段，所以设置为可选字段
    password = forms.CharField(min_length=6, max_length=20,)            # 定义密码字段，长度限制为6-20个字符
    confirm_password = forms.CharField(min_length=6,                    # 定义确认密码字段，长度限制为6-20个字符  
                                       max_length=20,
                                       error_messages={'required': '请再次输入密码,二次密码输入要一致!',
                                                       'min_length': '密码长度不能小于6位', 
                                                       'max_length': '密码长度不能大于12位'},)                                                                        
    verify_code = forms.CharField(max_length=4, required=False)         # 定义验证码字段，长度限制为4个字符，可选字段

    # clean_username方法,局部钩子函数，验证用户名是否全部数字或包含特殊字符
    def clean_username(self):
        val=self.cleaned_data.get('username')                           # 使用cleaned_data字典的get方法获取用户名字段的值
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]+$', val):                # 判断用户名是否包含特殊字符   这里使用re正则表达式验证用户名是否全部数字或包含特殊字符                         
            self.add_error('username', '用户名以字母开头，只包含字母、数字和下划线，不能包含其他字符') # 使用add_error方法添加错误信息，错误信息用字典的形式传入，键为字段名，值为错误信息

        if User.objects.filter(username=val).exists():                  # 判断用户名是否已被注册过了       
            self.add_error('username', '用户名已被注册过了')
        return val
    
    # clean_email方法,局部钩子函数，验证邮箱是否已被注册
    def clean_email(self):                                                # 定义clean_email方法，用于验证邮箱是否已被注册
        val=self.cleaned_data.get('email')                                # 使用cleaned_data字典的get方法获取邮箱字段的值
        if len(val) < 8 or len(val) > 50:                                 # 如果email字段值长度不在8到50个字符之间，返回错误信息
            self.add_error('email', '邮箱长度不在8到50个字符之间，如果邮箱不正确，无法激活账户')          # 使用add_error方法添加错误信息，错误信息用字典的形式传入，键为字段名，值为错误信息
        if User.objects.filter(email=val).exists():                       # 判断邮箱是否已被注册过了          
            self.add_error('email', '邮箱已被注册过了，如果邮箱不正确，无法激活账户')                     # 使用add_error方法添加错误信息，错误信息用字典的形式传入，键为字段名，值为错误信息
        return val

    # clean_password方法,局部钩子函数，验证密码是否全部数字或包含特殊字符,
    def clean_password(self):
        val=self.cleaned_data.get('password')
        if  val is None: #or val.isdigit():这里允许密码全为数字
            self.add_error('password', '密码不能为空，且不能全是数字')
        if not re.match(r'^[a-zA-Z0-9_]+$', val):
            self.add_error('password', '密码只能包含字母、数字和下划线，不能包含其他字符')
        return val
    
    # clena_verify_code方法,局部钩子函数，验证验证码是否为空
    def clean_verify_code(self):
        val=self.cleaned_data.get('verify_code')
        if val is None:
            self.add_error('verify_code', '验证码不能为空')
        return val

    # clean全局钩子函数，验证确认密码是否与密码一致
    def clean(self):                                                        # 定义clean方法，这是全局钩子函数，用于验证确认密码是否与密码一致
        # 调用父类的 clean 方法，获取 cleaned_data 字典
        self.cleaned_data = super().clean()
        
        # 检查 cleaned_data 是否存在
        if not self.cleaned_data:
            return self.cleaned_data
        
        password = self.cleaned_data.get('password')                        # 获取密码字段的值              
        confirm_password = self.cleaned_data.get('confirm_password')        # 获取确认密码字段的值
        if password != confirm_password:                                    # 判断确认密码是否与密码一致                            
            self.add_error('confirm_password', '二次密码不一致')  # 使用add_error方法添加错误信息，错误信息用字典的形式传入，键为字段名，值为错误信息   
        return self.cleaned_data                                            # 返回cleaned_data字典，用于保存表单数据 


# 定义登录表单类
class LoginForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=20)             # 定义用户名字段，长度限制为4-20个字符
    password = forms.CharField(min_length=6, max_length=20,)            # 定义密码字段，长度限制为6-20个字符
    verify_code = forms.CharField(max_length=4, required=False)         # 定义验证码字段，长度限制为4个字符，可选字段
                            
    # clean_username方法,局部钩子函数，验证用户名是否全部数字或包含特殊字符
    def clean_username(self):
        val=self.cleaned_data.get('username')                           # 使用cleaned_data字典的get方法获取用户名字段的值

        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]+$', val):               # 判断用户名是否包含特殊字符                            
            self.add_error('username', '用户名以字母开头，只包含字母、数字和下划线，不能包含其他字符') # 使用add_error方法添加错误信息，错误信息用字典的形式传入，键为字段名，值为错误信息

        if not User.objects.filter(username=val).exists():              # 判断用户名是否已被注册过了       
            self.add_error('username', '用户名不存在！')
        return val
    
    # clena_verify_code方法,局部钩子函数，验证验证码是否为空
    def clean_verify_code(self):
        val=self.cleaned_data.get('verify_code')
        if val is None:
            self.add_error('verify_code', '验证码不能为空')
        return val




                  
                                                   
                