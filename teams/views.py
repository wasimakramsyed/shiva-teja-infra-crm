from django.shortcuts import render, redirect, get_object_or_404
from .models import Team
from .forms import TeamForm
from accounts.decorators import role_required


@role_required(['admin', 'manager'])
def team_list(request):
    query = request.GET.get('q')

    teams = Team.objects.all()

    if query:
        teams = teams.filter(
            team_name__icontains=query
        )

    return render(
        request,
        'teams/team_list.html',
        {
            'teams': teams,
            'query': query
        }
    )


@role_required(['admin'])
def create_team(request):
    form = TeamForm(
        request.POST or None
    )

    if form.is_valid():
        form.save()
        return redirect('/teams/')

    return render(
        request,
        'teams/create_team.html',
        {
            'form': form
        }
    )


@role_required(['admin', 'manager'])
def team_dashboard(request, team_id):
    team = get_object_or_404(
        Team,
        id=team_id
    )

    members_count = team.members.count()

    context = {
        'team': team,
        'members_count': members_count,
    }

    return render(
        request,
        'teams/team_dashboard.html',
        context
    )


@role_required(['admin'])
def edit_team(request, team_id):
    team = get_object_or_404(
        Team,
        id=team_id
    )

    form = TeamForm(
        request.POST or None,
        instance=team
    )

    if form.is_valid():
        form.save()
        return redirect('/teams/')

    return render(
        request,
        'teams/create_team.html',
        {
            'form': form
        }
    )