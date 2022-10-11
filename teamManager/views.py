import json

from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from teamManager.dtos import TeamDTO
from teamManager.models import Team


# Create your views here.

class TeamsView(APIView):

    # Return all teams data
    def get(self, request):
        teams = list()
        for team in Team.objects():
            teams.append(TeamDTO(team.name, team.id.__str__()).__dict__)
        return Response(teams, status=status.HTTP_200_OK)

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        Team(**json.loads(body_unicode)).save()
        return Response(status=status.HTTP_201_CREATED)


class TeamView(APIView):

    def get(self, request, team_id):
        team = Team.objects(id=team_id).get()
        return JsonResponse(TeamDTO(team.name, team.id.__str__()).__dict__, status=status.HTTP_200_OK)

    def put(self, request, team_id):
        body_unicode = request.body.decode('utf-8')
        new_team = Team(**json.loads(body_unicode))
        new_team.id = team_id
        new_team.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, team_id):
        Team.objects(id=team_id).get().delete()
        return Response(status=status.HTTP_200_OK)
