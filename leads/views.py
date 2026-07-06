from django.shortcuts import render, redirect, get_object_or_404
from .models import Lead
from .forms import LeadForm
from customers.models import Customer
from accounts.decorators import role_required


@role_required(['admin', 'manager', 'sales'])
def lead_list(request):
    query = request.GET.get('q')
    status_filter = request.GET.get('status')

    leads = Lead.objects.all()

    if query:
        leads = leads.filter(
            lead_name__icontains=query
        )

    if status_filter:
        leads = leads.filter(
            status=status_filter
        )

    return render(
        request,
        'leads/lead_list.html',
        {
            'leads': leads,
            'query': query,
            'status_filter': status_filter
        }
    )


@role_required(['sales', 'admin'])
def create_lead(request):
    form = LeadForm(
        request.POST or None
    )

    if form.is_valid():
        form.save()
        return redirect('/leads/')

    return render(
        request,
        'leads/create_lead.html',
        {
            'form': form
        }
    )


@role_required(['admin', 'manager', 'sales'])
def lead_profile(request, lead_id):
    lead = get_object_or_404(
        Lead,
        id=lead_id
    )

    return render(
        request,
        'leads/lead_profile.html',
        {
            'lead': lead
        }
    )


@role_required(['admin', 'sales'])
def edit_lead(request, lead_id):
    lead = get_object_or_404(
        Lead,
        id=lead_id
    )

    form = LeadForm(
        request.POST or None,
        instance=lead
    )

    if form.is_valid():
        form.save()
        return redirect('/leads/')

    return render(
        request,
        'leads/create_lead.html',
        {
            'form': form
        }
    )


from django.contrib import messages
from bookings.models import Booking


@role_required(['admin', 'sales'])
def convert_lead(request, lead_id):
    lead = get_object_or_404(
        Lead,
        id=lead_id
    )

    # Only mark as converted
    lead.status = 'converted'
    lead.save()

    messages.success(
        request,
        "Lead converted successfully. Create booking now."
    )

    return redirect(f'/bookings/create/?lead={lead.id}')