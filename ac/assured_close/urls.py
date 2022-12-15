"""Assured Close URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from audit.views import audit_view, audit_detailed_view
from orders.views import orders_view, order_edit, order_edited, customer_order_view, order_delete, \
    pay_order, order_create
from core.views import customer_registration, customer_agent_login, customer_profile, customer_profile_edit, \
    customer_or_agent_list, \
    agent_profile, agent_profile_edit, customer_agent_logout, \
    customer_profile_edited, agent_profile_edited
from payment_integration.stripe_payment.views import ProductDetailView, \
    PaymentSuccessView, PaymentFailedView, PaymentHistoryListView, create_checkout_session

auth_pages = [
    # Customer and Agent Pages
    path('', customer_agent_login, name='customer_agent_login'),
    path('register', customer_registration, name='customer_registration'),
    path('logout', customer_agent_logout, name='customer_agent_logout'),
    path('customer/profile/', customer_profile, name='customer_profile'),
    path('customer/profile/edit', customer_profile_edit, name='customer_profile_edit'),
    path('customer/profile/edit/<uuid:pk>', customer_profile_edited, name='customer_profile_edited'),
    path('customer/or/agent/list', customer_or_agent_list, name='customer_or_agent_list'),
    path('agent/profile', agent_profile, name='agent_profile'),
    path('agent/profile/edit', agent_profile_edit, name='agent_profile_edit'),
    path('agent/profile/edit/<uuid:pk>', agent_profile_edited, name='agent_profile_edited'),

    # Audit URLs
    path('order/audit/<uuid:pk>', audit_view, name='order_audit'),
    path('order/audit/detailed/<int:pk>', audit_detailed_view, name='audit_detailed_view'),
]

login_required_pages = [
    path('orders', orders_view, name='orders'),
    path('orders/edit/<uuid:pk>', order_edit, name='order_edit'),
    path('orders/edited/<uuid:pk>', order_edited, name='order_edited'),
    path('customer/order/view/<uuid:pk>', customer_order_view, name='customer_order_view'),
    path('orders/create', order_create, name='order_create'),
    path('orders/delete/<uuid:pk>', order_delete, name='order_delete'),
    path('orders/pay', login_required(TemplateView.as_view(template_name='make_payment.html'))),
    path('temp', TemplateView.as_view(template_name='temp.html')),
    path('pay/<str:pk>', pay_order, name='pay_order'),

    # payment
    path('detail/<id>/', ProductDetailView.as_view(), name='detail'),
    path('success/', PaymentSuccessView.as_view(), name='success'),
    path('failed/', PaymentFailedView.as_view(), name='failed'),
    path('history/', PaymentHistoryListView.as_view(), name='history'),
    path('api/checkout-session/<id>/', create_checkout_session, name='api_checkout_session'),
]

testing_pages = [
    # path('register_customer_temp', test_customer_register, name="test_customer_register"),
    # path('register_agent_temp', test_agent_register, name="test_agent_register"),
    # url(r'^halt_clusters/(?P<order_id>\d+)/$', OrdersEditView, name='edit_order')
]

misc_pages = [
    # Django Admin
    path('admin/', admin.site.urls),
]

urlpatterns = auth_pages + login_required_pages + misc_pages + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Uncomment for development
urlpatterns += testing_pages
