from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def user_login(request):
    data = {}
    if request.method == 'POST':
        # user_type = "security"
        user_type = request.POST['user_type']
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            if user_type == 'security' and user.user_type == 'security':
                login(request, user)
                request.session['username'] = username
                return redirect('home')
            elif user_type == 'security_supervisor' and user.user_type == 'security_supervisor':
                login(request, user)
                request.session['username'] = username
                return redirect('home')
            else:
                data['error'] = "Please select valid option!"
                return render(request, 'login.html', data)
        else:
            data['error'] = "Username or Password is incorrect"
            return render(request, 'login.html', data)
    else:
        return render(request, 'login.html', )


@login_required(login_url="/")
def user_logout(request):
    logout(request)
    return redirect('user_login')
