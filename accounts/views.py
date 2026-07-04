from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def login_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            if user.role == 'admin':
                return redirect('/')

            elif user.role == 'manager':
                return redirect('/')

            elif user.role == 'sales':
                return redirect('/sales-dashboard/')

            elif user.role == 'accounts':
                return redirect('/accounts-dashboard/')

        else:
            error = "Invalid username or password"

    return render(
        request,
        'accounts/login.html',
        {
            'error': error
        }
    )


def logout_view(request):
    logout(request)
    return redirect('/login/')