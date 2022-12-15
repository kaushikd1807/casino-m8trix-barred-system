from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from core.models import Country
from .models import Order, Document
from .forms import OrderForm, DocumentForm

User = get_user_model()


@login_required(login_url='/')
def orders_view(request):
    if request.method == "POST":
        mls_id = request.POST['mls_id']
        if mls_id:
            orders = Order.objects.filter(mls_id=mls_id)
            context = {
                'mls_id': mls_id,
                'orders': orders,
            }
            return render(request, 'orders.html', context=context)

        customer_email = request.POST['customer_email']
        if customer_email:
            orders = Order.objects.filter(customer__username__icontains=customer_email)
            context = {
                'customer_email': customer_email,
                'orders': orders,
            }
            return render(request, 'orders.html', context=context)
        try:
            order_params = {
                'created_at__gte': request.POST['start_date'],
                'created_at__lte': request.POST['end_date'],
            }
            orders = Order.objects.filter(**order_params)
            context = {
                'start_date': request.POST['start_date'],
                'end_date': request.POST['end_date'],
                'orders': orders,
            }
            return render(request, 'orders.html', context=context)

        except:
            return redirect('orders')

    elif request.user.user_type == 'agent':
        orders = Order.objects.filter(agent=request.user)
        page = request.GET.get('page', 1)
        paginator = Paginator(orders, 50)
        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            orders = paginator.page(paginator.num_pages)
        context = {
            'orders': orders,
        }
        return render(request, 'orders.html', context=context)

    elif request.user.user_type == 'customer':
        orders = Order.objects.filter(customer=request.user)
        page = request.GET.get('page', 1)
        paginator = Paginator(orders, 50)
        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            orders = paginator.page(paginator.num_pages)
        context = {
            'orders': orders,
        }
        return render(request, 'orders.html', context=context)

    else:
        return redirect('customer_agent_login')


@login_required(login_url='/')
def order_edit(request, pk):
    shared = None
    if request.user.user_type == 'agent':
        order = Order.objects.get(uuid=pk)
        countries = Country.objects.all()
        documents = Document.objects.filter(order=order)
        for document in documents:
            shared = document.shared
        context = {
            'order': order,
            'documents': documents,
            'countries': countries,
            'shared': shared,
        }
        return render(request, 'edit_order.html', context=context)
    else:
        return redirect('orders')


@login_required(login_url='/')
def order_delete(request, pk):
    if request.user.user_type == 'agent':
        order = Order.objects.get(uuid=pk)
        order.delete()
        return redirect('orders')
    else:
        return redirect('orders')


@login_required(login_url='/')
def order_edited(request, pk):
    if request.user.user_type == 'agent':
        if request.method == 'POST':
            request_data = request.POST
            order = Order.objects.get(uuid=pk)
            # order.agent.brokerage.name = request_data['agent_brokerage_name']
            # order.agent.phone = request_data['agent_phone']
            # order.agent.relator_id = request_data['agent_realtor_id']
            # order.agent.email = request_data['agent_email']
            order.mls_id = request_data['mls_id']
            order.listing_url = request_data['listing_url']
            order.address1 = request_data['property_address1']
            order.address2 = request_data['property_address2']
            order.city = request_data['property_city']
            order.state = request_data['property_state']
            order.zip_code = request_data['property_zip_code']
            order.country = request_data['property_country']
            order.agent_notes = request_data['agent_notes']
            order.save()

            shared = False
            try:
                shared = request.POST['shared_status']
            except:
                pass
            documents = Document.objects.filter(order=order)
            for document in documents:
                document.shared = shared
                document.save()
            files = request.FILES.getlist('property_files')
            if files:
                for file in files:
                    document = Document.objects.create(
                        shared=shared,
                        document_file=file,
                        order=order
                    )
            messages.success(request, 'The order has been updated successfully!!')
            return redirect('order_edit', pk=pk)
    return redirect('order_edit', pk=pk)


@login_required(login_url='/')
def customer_order_view(request, pk):
    if request.user.user_type == 'customer':
        order = Order.objects.get(uuid=pk)
        documents = Document.objects.filter(order=order, shared=True)
        context = {
            'order': order,
            'documents': documents,
        }
        return render(request, 'detailed_order_view.html', context=context)
    return redirect('orders')


def pay_order(request, pk):
    order = Order.objects.get(magic_url_seed=pk)
    context = {
        'order': order,
    }
    return render(request, 'qrcode_edit_order.html', context=context)


@login_required(login_url='/')
def order_create(request):
    if request.user.user_type == 'agent':
        if request.method == 'POST':
            try:
                order_form = OrderForm(request.POST)
                if order_form.is_valid():
                    order_form.save()

                order = Order.objects.get(mls_id=request.POST['mls_id'])

                shared = False
                try:
                    shared = request.POST['shared_status']
                except:
                    pass
                files = request.FILES.getlist('property_files')
                if files:
                    for file in files:
                        document = Document.objects.create(
                            shared=shared,
                            document_file=file,
                            order=order
                        )
                return redirect('orders')
            except:
                return redirect('orders')
        else:
            agents_list = User.objects.filter(uuid=request.user.uuid)
            customers_list = User.objects.filter(user_type='customer')
            countries = Country.objects.all()
            context = {
                'agents_list': agents_list,
                'customers_list': customers_list,
                'countries': countries,
            }
            return render(request, 'create_order.html', context=context)
    else:
        return redirect('orders')
