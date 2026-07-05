from django.shortcuts import render, redirect
from .models import CRMSettings
from .forms import CRMSettingsForm
from accounts.decorators import role_required


@role_required(['admin'])
def crm_settings(request):
    settings = CRMSettings.objects.first()

    form = CRMSettingsForm(
        request.POST or None,
        instance=settings
    )

    if form.is_valid():
        form.save()
        return redirect('/settings/')

    return render(
        request,
        'settings_config/crm_settings.html',
        {
            'form': form
        }
    )