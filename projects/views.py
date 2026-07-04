from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Plot
from .forms import ProjectForm, PlotForm
from bookings.models import Booking
from payments.models import Payment
from accounts.decorators import role_required


@role_required(['admin', 'manager'])
def project_list(request):
    query = request.GET.get('q')

    projects = Project.objects.all()

    if query:
        projects = projects.filter(
            project_name__icontains=query
        )

    return render(
        request,
        'projects/project_list.html',
        {
            'projects': projects,
            'query': query
        }
    )


@role_required(['admin'])
def create_project(request):
    form = ProjectForm(
        request.POST or None
    )

    if form.is_valid():
        form.save()
        return redirect('/projects/')

    return render(
        request,
        'projects/create_project.html',
        {
            'form': form
        }
    )


@role_required(['admin'])
def create_plot(request):
    form = PlotForm(
        request.POST or None
    )

    if form.is_valid():
        form.save()
        return redirect('/projects/')

    return render(
        request,
        'projects/create_plot.html',
        {
            'form': form
        }
    )


@role_required(['admin', 'manager'])
def project_dashboard(request, project_id):
    project = get_object_or_404(
        Project,
        id=project_id
    )

    available_plots = project.plots.filter(
        status='available'
    ).count()

    booked_plots = project.plots.filter(
        status='booked'
    ).count()

    registered_plots = project.plots.filter(
        status='registered'
    ).count()

    bookings = Booking.objects.filter(
        project=project
    )

    revenue = sum(
        payment.amount
        for payment in Payment.objects.filter(
            booking__project=project
        )
    )

    outstanding = sum(
        booking.booking_amount
        for booking in bookings
    ) - revenue

    context = {
        'project': project,
        'available_plots': available_plots,
        'booked_plots': booked_plots,
        'registered_plots': registered_plots,
        'revenue': revenue,
        'outstanding': outstanding,
        'plots': project.plots.all(),
        'bookings': bookings,
    }

    return render(
        request,
        'projects/project_dashboard.html',
        context
    )


@role_required(['admin'])
def edit_project(request, project_id):
    project = get_object_or_404(
        Project,
        id=project_id
    )

    form = ProjectForm(
        request.POST or None,
        instance=project
    )

    if form.is_valid():
        form.save()
        return redirect('/projects/')

    return render(
        request,
        'projects/create_project.html',
        {
            'form': form
        }
    )