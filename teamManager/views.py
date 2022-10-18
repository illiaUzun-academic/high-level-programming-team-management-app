from django.shortcuts import render, redirect

from teamManager.dtos import TeamDTO
from teamManager.forms import TeamForm
from teamManager.models import Team


# Create your views here.


# Return all teams data
def team_list(request):
    teams = list()
    for team in Team.objects():
        teams.append(TeamDTO(team.id.__str__(), team.name, team.office_location).__dict__)
    return render(request, "team-list.html", {'teams': teams})


def team_create(request):
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            form_data = form.data
            team = Team()
            team.name = form_data.get("name")
            team.office_location = form_data.get("location")
            team.save()
            return redirect('team-list')
    else:
        form = TeamForm()
    return render(request, 'team-create.html', {'form': form})


def team_update(request, team_id):
    team = Team.objects.get(id=team_id)
    form = TeamForm(initial={'name': team.name, 'location': team.office_location})
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            form_data = form.data
            team.name = form_data.get("name")
            team.office_location = form_data.get("location")
            team.save()
            return redirect('/team-list')
    return render(request, 'team-update.html', {'form': form})


def team_delete(request, team_id):
    team = Team.objects.get(id=team_id)
    try:
        team.delete()
    except:
        pass
    return redirect('team-list')
