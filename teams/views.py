from django.shortcuts import render, redirect, get_object_or_404
from .models import Team
from .forms import TeamForm
from accounts.decorators import role_required
from django.db.models import Q
from employees.models import Employee

@role_required(['admin', 'manager'])
def team_list(request):

    query = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "").strip()

    teams = Team.objects.select_related(
        "team_head"
    ).prefetch_related(
        "members"
    )

    if query:

        teams = teams.filter(

            Q(team_id__icontains=query) |

            Q(team_name__icontains=query) |

            Q(team_head__first_name__icontains=query) |

            Q(team_head__surname__icontains=query) |

            Q(members__first_name__icontains=query) |

            Q(members__surname__icontains=query)

        ).distinct()

    if status_filter:

        teams = teams.filter(
            status=status_filter
        )

    context = {

        "teams": teams.order_by("team_name"),

        "query": query,

        "status_filter": status_filter,

        "total_teams": Team.objects.count(),

        "active_teams": Team.objects.filter(
            status="active"
        ).count(),

        "inactive_teams": Team.objects.filter(
            status="inactive"
        ).count(),

        "employee_count": Employee.objects.filter(
            status="active"
        ).count(),

    }

    return render(
        request,
        "teams/team_list.html",
        context
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