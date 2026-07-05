from django.shortcuts import render, redirect, get_object_or_404
from .models import Commission
from .forms import CommissionForm
from accounts.decorators import role_required
from notifications.models import Notification


@role_required(['admin', 'accounts', 'manager'])
def commission_list(request):
    query = request.GET.get('q')
    status_filter = request.GET.get('status')

    commissions = Commission.objects.all()

    if query:
        commissions = commissions.filter(
            commission_id__icontains=query
        )

    if status_filter:
        commissions = commissions.filter(
            status=status_filter
        )

    return render(
        request,
        'commissions/commission_list.html',
        {
            'commissions': commissions,
            'query': query,
            'status_filter': status_filter
        }
    )


@role_required(['admin', 'accounts'])
def create_commission(request):
    form = CommissionForm(
        request.POST or None
    )

    if form.is_valid():
        commission = form.save()

        Notification.objects.create(
            message=(
                f"Commission created: "
                f"{commission.commission_id}"
            )
        )

        return redirect('/commissions/')

    return render(
        request,
        'commissions/create_commission.html',
        {
            'form': form
        }
    )


@role_required(['admin', 'accounts', 'manager'])
def commission_profile(request, commission_id):
    commission = get_object_or_404(
        Commission,
        id=commission_id
    )

    return render(
        request,
        'commissions/commission_profile.html',
        {
            'commission': commission
        }
    )


@role_required(['admin', 'accounts'])
def edit_commission(request, commission_id):
    commission = get_object_or_404(
        Commission,
        id=commission_id
    )

    form = CommissionForm(
        request.POST or None,
        instance=commission
    )

    if form.is_valid():
        form.save()
        return redirect('/commissions/')

    return render(
        request,
        'commissions/create_commission.html',
        {
            'form': form
        }
    )