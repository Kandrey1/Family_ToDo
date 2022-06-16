from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import ListProducts, Products, TodoList


def index(request):
    return render(request, "todo/index.html")


def about(request):
    return render(request, "todo/about.html")


def list_products(request):
    lists = ListProducts.objects.filter(user_id=request.user.pk)
    if request.method == "POST":
        if "lists_create" in request.POST:
            new_list = request.POST.get('list')
            if new_list.strip() != "":
                list_e = ListProducts(name_list=new_list, user_id=request.user.pk)
                list_e.save()
                return redirect('lists_products')

        if "del_list" in request.POST:
            id_del_list = request.POST.get('del_list')
            ListProducts.objects.filter(pk=int(id_del_list)).delete()

    return render(request, "todo/lists_products.html", {"lists": lists})


def products(request, products_slug):
    products = Products.objects.filter(list_name=products_slug)
    if request.method == "POST":
        if "product_add" in request.POST:
            product = request.POST.get('product')
            if product.strip() != "":
                prod = Products(buy=product, list_name=products_slug, check=False)
                prod.save()
                return redirect(Products.get_path_redirect(products_slug))

        if "product_reset" in request.POST:
            products.update(check=False)
            return redirect(Products.get_path_redirect(products_slug))

        if "product_save" in request.POST:
            list_check = request.POST.getlist('checkedbox')
            Products.objects.filter(pk__in=list_check).update(check=True)
            Products.objects.exclude(pk__in=list_check).update(check=False)

        if "product_delete" in request.POST:
            list_del = request.POST.getlist('checkedbox')
            obj_del = Products.objects.filter(pk__in=[int(i) for i in list_del])
            obj_del.delete()

    return render(request, "todo/products.html", {"products": products, "title_list": products_slug})


def todo(request):
    todos = TodoList.objects.filter(user_id=request.user.pk)
    if request.method == "POST":
        if "todo_add" in request.POST:
            new_todo = request.POST.get('todo')
            if new_todo.strip() != "":
                todo = TodoList(title=new_todo, user_id=request.user.pk, check=False)
                todo.save()
                return redirect('todo')

        if "todo_reset" in request.POST:
            todos.update(check=False)

        if "todo_save" in request.POST:
            list_check = request.POST.getlist('checkedbox')
            TodoList.objects.filter(pk__in=list_check).update(check=True)
            TodoList.objects.exclude(pk__in=list_check).update(check=False)

        if "todo_delete" in request.POST:
            list_del = request.POST.getlist('checkedbox')
            obj_del = TodoList.objects.filter(pk__in=[int(i) for i in list_del])
            obj_del.delete()

    return render(request, "todo/todo_list.html", {"todos": todos})


def register_user(request):
    if request.method == "POST":
        reg_name = request.POST.get('reg_name')
        reg_email = request.POST.get('reg_email')
        reg_pass = request.POST.get('reg_pass')
        user_reg = User.objects.create_user(reg_name, reg_email, reg_pass)
        login(request, user_reg)
        return redirect('home')

    return render(request, "todo/register.html")


def login_user(request):
    auth_name = request.POST.get('auth_name')
    auth_pass = request.POST.get('auth_pass')

    user = authenticate(username=auth_name, password=auth_pass)
    if user is not None:
        login(request, user)
        return redirect('home')

    return render(request, "todo/login.html")


def logout_user(request):
    logout(request)
    return redirect('login')


def personal_account(request):
    return render(request, "todo/personal_account.html")
