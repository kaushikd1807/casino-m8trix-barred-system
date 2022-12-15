from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import AgentRegisterForm, CustomerRegisterForm
from orders.models import Order
from .models import User, Country


def customer_registration(request):
    data = {}
    if request.method == 'POST':
        requested_data = request.POST.copy()
        try:
            check = requested_data['agree_terms']
            requested_data['user_type'] = 'customer'
            form_object = CustomerRegisterForm(requested_data)
            if form_object.is_valid():
                form_object.save()
                return redirect('customer_agent_login')
            else:
                data['error'] = "Email or Password is not valid"
                res = render(request, 'register_customer.html', data)
                return res

        except:
            data['error'] = "Please accept the terms & conditions"
            res = render(request, 'register_customer.html', data)
            return res
    else:
        return render(request, 'register_customer.html', data)


def customer_agent_login(request):
    data = {}
    if request.method == 'POST':
        customer_or_agent = request.POST['customer_or_agent']
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            if customer_or_agent == 'customer' and user.user_type == 'customer':
                login(request, user)
                request.session['username'] = username
                if not user.first_name:
                    return redirect('customer_profile_edit')
                return redirect('orders')
            elif customer_or_agent == 'agent' and user.user_type == 'agent':
                login(request, user)
                request.session['username'] = username
                if not user.first_name:
                    return redirect('agent_profile_edit')
                return redirect('orders')
            else:
                data['error'] = "Please select valid option!"
                res = render(request, 'login_customer.html', data)
                return res
        else:
            data['error'] = "Username or Password is incorrect"
            res = render(request, 'login_customer.html', data)
            return res
    else:
        return render(request, 'login_customer.html', data)


@login_required(login_url="/")
def customer_profile(request):
    if request.user.user_type == 'customer':
        user = request.user
        context = {
            'user': user,
        }
        return render(request, 'profile_customer.html', context=context)
    else:
        return redirect('orders')


@login_required(login_url="/")
def customer_profile_edit(request):
    if request.user.user_type == 'customer':
        user = request.user
        countries = Country.objects.all()
        context = {
            'user': user,
            'countries': countries,
        }
        return render(request, 'profile_customer_edit.html', context=context)
    else:
        return redirect('orders')


@login_required(login_url="/")
def customer_profile_edited(request, pk):
    if request.user.user_type == 'customer':
        if request.method == 'POST':
            request_data = request.POST
            user = User.objects.get(uuid=pk)
            user.first_name = request_data['first_name']
            user.last_name = request_data['last_name']
            user.email = request_data['email']
            user.address1 = request_data['address1']
            user.address2 = request_data['address2']
            user.city = request_data['city']
            user.country = request_data['country']
            user.zip_code = request_data['zip_code']
            user.phone = request_data['phone']
            user.bio = request_data['bio']
            try:
                user.profile_photo = request.FILES['profile_photo']
            except:
                pass
            user.save()
            messages.success(request, 'Your Profile has been updated successfully!!')
            return redirect('customer_profile')
    return redirect('customer_profile')


@login_required(login_url="/")
def customer_or_agent_list(request):
    customer_or_agent = set()
    if request.user.user_type == 'agent':
        orders = Order.objects.filter(agent=request.user)
        for order in orders:
            customer_or_agent.add(order.customer)
    else:
        context = {'error': 'User is not valid!'}
        return render(request, 'customer_list.html', context=context)
    context = {'customer_or_agent': customer_or_agent, }
    return render(request, 'customer_list.html', context=context)


@login_required(login_url="/")
def agent_profile(request):
    if request.user.user_type == 'agent':
        user = request.user
        context = {
            'user': user,
        }
        return render(request, 'profile_agent.html', context=context)
    else:
        return redirect('orders')


@login_required(login_url="/")
def agent_profile_edit(request):
    if request.user.user_type == 'agent':
        user = request.user
        countries = Country.objects.all()
        context = {
            'user': user,
            'countries': countries,
        }
        return render(request, 'profile_agent_edit.html', context=context)
    else:
        return redirect('orders')


@login_required(login_url="/")
def agent_profile_edited(request, pk):
    if request.user.user_type == 'agent':
        if request.method == 'POST':
            request_data = request.POST
            user = User.objects.get(uuid=pk)
            # user.company = request_data['company']
            user.first_name = request_data['first_name']
            user.last_name = request_data['last_name']
            user.email = request_data['email']
            user.country = request_data['country']
            # user.relator_id = request_data['realtor_id']
            # user.brokerage.name = request_data['brokerage']
            # user.certifications = request_data['certifications']
            user.phone = request_data['phone']
            # user.brokerage.address1 = request_data['address1']
            # user.profile_photo = request_data['profile_photo']
            user.bio = request_data['bio']
            try:
                user.profile_photo = request.FILES['profile_photo']
                user.brokerage.save()
            except:
                pass
            user.save()
            messages.success(request, 'Your Profile has been updated successfully!!')
            return redirect('agent_profile')
    return redirect('agent_profile')


@login_required(login_url="/")
def customer_agent_logout(request):
    logout(request)
    return redirect('customer_agent_login')

# def test_customer_register(request):
#     if request.method == 'POST':
#         f = CustomerRegisterForm(request.POST)
#         if f.is_valid():
#             user = f.save()
#             group = Group.objects.get(name='customers')
#             user.groups.add(group)
#             return redirect('/login')
#         return redirect('/login')
#
#     else:
#         f = CustomerRegisterForm()
#         return render(request, 'test/register_customer_temp.html', {'form': f})
#
#
# def test_agent_register(request):
#     if request.method == 'POST':
#         f = AgentRegisterForm(request.POST)
#         if f.is_valid():
#             user = f.save()
#             group = Group.objects.get(name='agents')
#             user.groups.add(group)
#             return redirect('/agent_login')
#         return redirect('/agent_login')
#
#     else:
#         f = AgentRegisterForm()
#         return render(request, 'test/register_agent_temp.html', {'form': f})
