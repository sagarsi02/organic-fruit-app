from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import product, cart
from django.db.models import F
from django.http import JsonResponse
from .connection import my_custom_sql
from django.contrib.auth.decorators import login_required

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
                        usr.save()
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
    final_product_id = product_id.replace('-', '')
    get_product = product.objects.filter(product_id=final_product_id).values('product_id')
    if get_product:
        already_exist = cart.objects.filter(product_id=final_product_id).filter(user_id=user_id)
        if already_exist:
            cart.objects.filter(product_id=final_product_id).filter(user_id=user_id).update(product_quentity=F('product_quentity') + 1)
            messages.success(request, 'Successfully Added in your cart.')
            return redirect('/')
        else:
            carts = cart(product_id=final_product_id, user_id=user_id)
            carts.save()
            messages.success(request, 'Successfully Added in your cart.')
            return redirect('/')
    else:
        messages.warning(request, 'Sorry Product is out of Stock.')
        return redirect('/')

@login_required
def basket_list(request):
    get_user_id = request.user.id
    cart_list = cart.objects.filter(user_id=get_user_id)
    product_id = []
    for i in cart_list.values():
        product_id.append(i['product_id'])
    product_details = product.objects.filter(product_id__in=product_id)
    query = """
    SELECT 
        app_cart.product_quentity, 
        app_cart.user_id,
        app_product.product_id, 
        app_product.title, 
        app_product.desc, 
        app_product.image, 
        app_product.price, 
        app_product.kg_or_ltr
    FROM 
        app_cart
    INNER JOIN 
        app_product 
    ON 
        app_product.product_id = app_cart.product_id
    where 
        app_cart.user_id = {0};
    """.format(get_user_id)
    datas = my_custom_sql(query)
    if not datas:
        return JsonResponse({"message": "Item Not Found"}, safe=False, status=404)
    return JsonResponse(datas, safe=False)

def basket(request):
    return render(request, 'cart.html')