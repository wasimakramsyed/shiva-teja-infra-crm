from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from .forms import EmployeeForm
from accounts.decorators import role_required


@role_required(['admin', 'manager'])
def employee_list(request):
    query = request.GET.get('q')

    employees = Employee.objects.all()

    if query:
        employees = employees.filter(
            first_name__icontains=query
        )

    return render(
        request,
        'employees/employee_list.html',
        {
            'employees': employees,
            'query': query
        }
    )


@role_required(['admin'])
def create_employee(request):
    form = EmployeeForm(
        request.POST or None,
        request.FILES or None
    )

    if form.is_valid():
        form.save()
        return redirect('/employees/')

    return render(
        request,
        'employees/create_employee.html',
        {
            'form': form
        }
    )


@role_required(['admin', 'manager'])
def employee_profile(request, employee_id):
    employee = get_object_or_404(
        Employee,
        id=employee_id
    )

    return render(
        request,
        'employees/employee_profile.html',
        {
            'employee': employee
        }
    )


@role_required(['admin'])
def edit_employee(request, employee_id):
    employee = get_object_or_404(
        Employee,
        id=employee_id
    )

    form = EmployeeForm(
        request.POST or None,
        request.FILES or None,
        instance=employee
    )

    if form.is_valid():
        form.save()
        return redirect('/employees/')

    return render(
        request,
        'employees/create_employee.html',
        {
            'form': form
        }
    )