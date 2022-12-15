from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import json
from orders.models import Order
from easyaudit.models import CRUDEvent


@login_required(login_url="/")
def audit_view(request, pk):
    if request.user.user_type == 'agent':
        changed_fields = []
        order = Order.objects.get(uuid=pk)
        audit_objects = CRUDEvent.objects.filter(object_id=pk)
        for audit_object in audit_objects:
            if not ((audit_object.changed_fields is None) or (audit_object.changed_fields == 'null')):
                changed_fields.append(audit_object)
        context = {
            'changed_fields': changed_fields,
            'order': order,
        }
        return render(request, 'audit-view.html', context=context)
    else:
        return redirect('orders')


@login_required(login_url="/")
def audit_detailed_view(request, pk):
    if request.user.user_type == 'agent':
        audit = []
        audit_object = CRUDEvent.objects.get(id=pk)
        str_data = audit_object.changed_fields
        dict_data = json.loads(str_data)
        for key, value in dict_data.items():
            audit.append(
                {
                    "field": key,
                    "old_value": value[0],
                    "new_value": value[1]
                }
            )
        context = {
            'audit_objects': audit,
        }
        return render(request, 'audit_detailed_view.html', context=context)
    else:
        return redirect('orders')
