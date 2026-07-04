from django.shortcuts import render, redirect
from .models import Registration
from .forms import RegistrationForm
from accounts.decorators import role_required
from notifications.models import Notification


@role_required(['admin', 'manager'])
def registration_list(request):
    registrations = Registration.objects.all()

    return render(
        request,
        'registrations/registration_list.html',
        {'registrations': registrations}
    )


@role_required(['admin', 'manager', 'sales'])
def create_registration(request):
    form = RegistrationForm(request.POST or None)

    if form.is_valid():
        form.save()

        Notification.objects.create(
            message="Registration completed"
        )
        return redirect('/registrations/')

    return render(
        request,
        'registrations/create_registration.html',
        {'form': form}
    )