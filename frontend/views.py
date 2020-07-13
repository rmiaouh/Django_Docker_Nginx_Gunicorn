from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def list(request):
    return render(request, 'frontend/list.html')


@login_required(login_url='login')
def orangepage(request):
    return render(request, 'frontend/orangepage.html')


@login_required(login_url='login')
def pinkpage(request):
    return render(request, 'frontend/pinkpage.html')


@login_required(login_url='login')
def yellowpage(request):
    return render(request, 'frontend/yellowpage.html')


@login_required(login_url='login')
def redpage(request):
    return render(request, 'frontend/redpage.html')


@login_required(login_url='login')
def bluepage(request):
    return render(request, 'frontend/bluepage.html')


@login_required(login_url='login')
def greenpage(request):
    return render(request, 'frontend/greenpage.html')


@login_required(login_url='login')
def home(request):
    return render(request, 'frontend/index.html')


@login_required(login_url='login')
def about(request):
    return render(request, 'frontend/about.html')


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'frontend/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')
