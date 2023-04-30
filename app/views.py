from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import product, cart

def home(request):
    prod_list = product.objects.all()
    context = {"prod_list":prod_list}
    return render(request, 'index.html', context)

def createUser(request):
        if request.method == "POST":
            name = request.POST['FullName']
            email = request.POST['SignUpEmail']
            username = request.POST['username']
            password = request.POST['signupPass']
            c_password = request.POST['CnfSignupPass']

            first_last_name = name.split(' ', 1)

            if password == c_password:
                if User.objects.filter(email=email).exists():
                    messages.warning(request, 'Already have your account.')
                    return redirect('/')
                else:
                    if User.objects.filter(username=username).exists():
                        messages.warning(request, 'Username is already taken.')
                        return redirect('/')
                    else:
                        usr = User.objects.create_user(first_name=first_last_name[0], last_name=first_last_name[1] , username=username, email=email, password=password)
                        usr.save();
                        messages.success(request, 'Successfully Account created.')
                        return redirect('/')
            else:
                messages.warning(request, 'Password do not match.')
                return redirect('/')
        else:
            return render(request, 'index.html')
    
def userLogin(request):
    if request.method == 'POST':
        userEmail = request.POST['UserEmail']
        password = request.POST['loginPass']

        email_exist = User.objects.filter(email=userEmail).exists()
        username_exist = User.objects.filter(username=userEmail).exists()
        if email_exist:
            user = authenticate(email=userEmail, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Successfully Loggedin.')
                return redirect('/')
            else:
                messages.warning(request, 'Password is wrong.')
                return redirect('/')
        elif username_exist:
            user = authenticate(username=userEmail, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Successfully Loggedin.')
                return redirect('/')
            else:
                messages.warning(request, 'Password is wrong.')
                return redirect('/')
        else:
            messages.warning(request, 'Account not found.')
            return redirect('/')

def userLogout(request):
    logout(request)
    messages.success(request, 'Successfully LoggedOut.')
    return redirect('/')

def add_to_cart(request, user_id, product_id):
    # get_user = User.objects.filter(id=user_id)
    get_product = product.objects.filter(product_id=product_id).values('product_id')
    if get_product:
        carts = cart(product_id=product_id, user_id=user_id)
        carts.save()
        messages.success(request, 'Successfully Added in your cart.')
        return redirect('/')
    else:
        messages.warning(request, 'Sorry Product is out of Stock.')
        return redirect('/')