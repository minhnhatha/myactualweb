from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import MyLogin
from django.contrib import messages
# ----------------------------------------
def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            mail = request.POST.get("username")[:100]
            passw = request.POST.get("password")[:100]
            user = authenticate(request, username=mail, password=passw)
            if user is not None:
                login(request,user)
                request.session['username'] = mail
                return redirect('home')
            else:
                messages.error(request, "Login failed!")
    return render(request, "login.html")

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = MyLogin()
    if request.method == "POST":
        form = MyLogin(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
        else:
            messages.error(request, "Sign up failed!")
    context = {'form': form}
    return render(request, "up.html", context)