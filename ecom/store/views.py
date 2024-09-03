from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django.contrib.auth.models import User

def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        
        if form.is_valid():
            form.save()
            
            messages.success(request, ("User info updated"))
            return redirect('home')
        
        return render(request, "update_info.html", {"form": form})
    else:
        messages.success(request, 'Log in in order to access this page.')
        return redirect('home')
    


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Password changed succesfully')
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
                return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request,'update_password.html',{'form':form})
    else:
        messages.success(request, 'You must be logged in to update password')
        return redirect('home')

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        
        if user_form.is_valid():
            user_form.save()
            
            login(request, current_user)
            messages.success(request, ("User profile updated"))
            return redirect('home')
        
        return render(request, "update_user.html", {"user_form": user_form})
    else:
        messages.success(request, 'Log in in order to access this page.')
        return redirect('home')
    
    return render(request, 'update_user.html', {})

def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories':categories})

def category(request, var):
    var = var.replace('-',' ')
    print(var)
    try:
        category = Category.objects.get(name=var)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except:
        messages.success(request, ('Inexistent category.'))
        return redirect('home')
    

def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Logged in succesfully!"))
            return redirect('home')
        else:
            messages.success(request, ("Error logging in. Try again."))
            return redirect('login')
    else:
        return render(request, 'login.html', {})
    
def logout_user(request):
    logout(request)
    messages.success(request, ("Logged out. Thanks for shopping!"))
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            
            user = authenticate(username=username,password=password)
            login(request, user)
            messages.success(request, ("Successful registration."))
            return redirect('home')
        else:
            messages.success(request, ("Problem registering."))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})

