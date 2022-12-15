from django.contrib import admin
from django.urls import path
from apps.barred_patron.views import (first, self_restrict, save_data, view_table, update_self_restrict, delete_self_restrict,
                                      barred_patron_form, notice_of_reinstate, request_for_reinstate,
                                      )
from apps.accounts.views import user_login, user_logout


urlpatterns = [

    path('', user_login, name="user_login"),
    path('logout', user_logout, name="user_logout"),
    path('home', first, name="home"),
    path('self-restrict', self_restrict, name="self-restrict"),
    path('barred-patron-form', barred_patron_form, name="barred_patron_form"),
    path('notice-of-reinstate', notice_of_reinstate, name="notice_of_reinstate"),
    path('request-for-reinstate', request_for_reinstate, name="request_for_reinstate"),
    path('save', save_data, name="save-data"),
    path('tables-view', view_table, name="view_table"),
    path('self-restrict/edit/<int:pk>', update_self_restrict, name="update_self_restrict"),
    path('self-restrict/delete/<int:pk>', delete_self_restrict, name="delete_self_restrict"),

    # admin
    path('admin/', admin.site.urls),

]
