from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm,LoginForm
from blogs.models import Category
from django.contrib.auth import authenticate,login,logout

def Register(request):
    cat_manu = Category.objects.all()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user to the database
            messages.success(request, 'Your account has been created successfully!')
            return redirect('user_login')  # Redirect to login page after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'User/user_register.html', {'form': form,'cat_manu':cat_manu})

def Login(request):
    cat_manu = Category.objects.all()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Log the user in
                login(request, user)
                return redirect('blogs')  # Redirect to the home page or any other page
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'User/user_login.html', {'form': form,'cat_manu':cat_manu})

def Logout(request):
    logout(request)
    messages.info(request,'You are logout successfully, thanks for your time!.')
    return redirect ('blogs')

@login_required
def Profile(request):
    cat_manu = Category.objects.all()
    template = 'User/profile.html'
    return render(request,template,{'user':request.user,'cat_manu':cat_manu})