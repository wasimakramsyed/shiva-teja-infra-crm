from django.shortcuts import render, redirect, get_object_or_404
from .models import Lead
from .forms import LeadForm
from accounts.decorators import role_required
from customers.models import Customer
from notifications.models import Notification


@role_required(['admin', 'manager', 'sales'])
def lead_list(request):
    leads = Lead.objects.all()

    return render(
        request,
        'leads/lead_list.html',
        {'leads': leads}
    )


@role_required(['sales'])
def create_lead(request):
    form = LeadForm(request.POST or None)

    if form.is_valid():
        form.save()

        # Create Notification
        Notification.objects.create(
            message="New lead created"
        )

        return redirect('/leads/')

    return render(
        request,
        'leads/create_lead.html',
        {'form': form}
    )


@role_required(['admin', 'sales'])
def convert_lead(request, lead_id):
    lead = get_object_or_404(
        Lead,
        id=lead_id
    )

    # Prevent duplicate conversion
    if hasattr(lead, 'customer'):
        return redirect('/leads/')

    Customer.objects.create(
        lead=lead,
        customer_name=lead.lead_name,
        mobile_number=lead.mobile_number,
        email=lead.email,
        address=lead.address,
        assigned_to=lead.assigned_to
    )

    lead.status = 'converted'
    lead.save()

    # Create Notification
    Notification.objects.create(
        message=f"Lead {lead.lead_name} converted to customer"
    )

    return redirect('/leads/')