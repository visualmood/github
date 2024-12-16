from django.shortcuts import render

# Create your views here.
def login_view(request):
    print("login")

    return render(request, 'authentication/login.html')

def register_view(request):
    print("register")

    return render(request,'authentication/register.html')


def logout_view(request):
    print("logout")

    return render(request, 'authentication/logout.html')