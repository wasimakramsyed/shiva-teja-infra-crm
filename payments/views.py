from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .models import Payment
from .forms import PaymentForm
from accounts.decorators import role_required
from notifications.models import Notification


@role_required(['admin', 'accounts'])
def payment_list(request):
    query = request.GET.get('q')
    status_filter = request.GET.get('status')

    payments = Payment.objects.all()

    # Search by payment ID
    if query:
        payments = payments.filter(
            payment_id__icontains=query
        )

    # Filter by payment status
    if status_filter:
        payments = payments.filter(
            status=status_filter
        )

    return render(
        request,
        'payments/payment_list.html',
        {
            'payments': payments,
            'query': query,
            'status_filter': status_filter
        }
    )


@role_required(['accounts'])
def create_payment(request):
    form = PaymentForm(request.POST or None)

    if form.is_valid():
        try:
            payment = form.save(commit=False)
            payment.full_clean()
            payment.save()

            Notification.objects.create(
                message="Payment received"
            )

            return redirect('/payments/')

        except ValidationError as e:
            form.add_error(None, e)

    return render(
        request,
        'payments/create_payment.html',
        {'form': form}
    )