from django.shortcuts import render
from apps.barred_patron.models import PersonalInfo
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@login_required(login_url="/")
def first(request):
    return render(request, 'index.html', )


@login_required(login_url="/")
def barred_patron_form(request):
    return render(request, 'barred_patron_form.html', )


@login_required(login_url="/")
def notice_of_reinstate(request):
    return render(request, 'notice_of_reinstate.html', )


@login_required(login_url="/")
def request_for_reinstate(request):
    return render(request, 'request_for_reinstate.html', )


@login_required(login_url="/")
def self_restrict(request):
    return render(request, 'self_restrict.html')


@login_required(login_url="/")
def save_data(request):
    if request.method == "POST":
        print("data...", request.POST)
        first_name = request.POST['first_name']
        middle_name = request.POST['middle_name']
        last_name = request.POST['last_name']
        other_name = request.POST['other_name']
        date = request.POST['date']
        home_address = request.POST['home_address']
        home_street = request.POST['home_street']
        home_city = request.POST['home_city']
        home_state = request.POST['home_state']
        home_zipcode = request.POST['home_zipcode']

        personal_info = PersonalInfo.objects.create(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            other_name=other_name,
            date=date,
            home_address=home_address,
            home_street=home_street,
            home_city=home_city,
            home_state=home_state,
            home_zipcode=home_zipcode
        )
        personal_info.save()
    return redirect('view_table')


@login_required(login_url="/")
def view_table(request):
    tables = PersonalInfo.objects.all()
    context = {
        'tables': tables
    }
    return render(request, 'tables.html', context=context)


@login_required(login_url="/")
def update_self_restrict(request, pk):
    self_restrict = PersonalInfo.objects.get(id=pk)
    if request.method == "POST":
        first_name = request.POST['first_name']
        middle_name = request.POST['middle_name']
        last_name = request.POST['last_name']
        other_name = request.POST['other_name']
        date = request.POST['date']
        home_address = request.POST['home_address']
        home_street = request.POST['home_street']
        home_city = request.POST['home_city']
        home_state = request.POST['home_state']
        home_zipcode = request.POST['home_zipcode']

        self_restrict.first_name = first_name
        self_restrict.middle_name = middle_name
        self_restrict.last_name = last_name
        self_restrict.other_name = other_name
        # self_restrict.date = date
        self_restrict.home_address = home_address
        self_restrict.home_street = home_street
        self_restrict.home_city = home_city
        self_restrict.home_state = home_state
        self_restrict.home_zipcode = home_zipcode

        self_restrict.save()
        messages.success(request, 'Form submission successful')

        return HttpResponseRedirect(request.path_info)

    context = {
        'self_restrict': self_restrict
    }
    return render(request, 'self_restrict.html', context=context)


@login_required(login_url="/")
def delete_self_restrict(request, pk):
    self_restrict = PersonalInfo.objects.get(id=pk)
    self_restrict.delete()
    return redirect('view_table')


