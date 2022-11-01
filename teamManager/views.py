import base64
import io

import matplotlib.pyplot as plt
import openpyxl
from django.shortcuts import render, redirect

from teamManager.dtos import TeamDTO, EmployeeDTO
from teamManager.forms import TeamForm, EmployeeForm
from teamManager.models import Team, Employee


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
            return redirect('team-list')
    return render(request, 'team-update.html', {'form': form})


def team_delete(request, team_id):
    Team.objects.get(id=team_id).delete()
    Employee.objects.get(team_id=team_id).delete()
    return redirect('team-list')


SALARY_BORDERS = [1500, 4000]
TENURE_BORDERS = [2, 5]


def team_view(request, team_id):
    team = Team.objects.get(id=team_id)

    quality = 1
    cost = 1
    speed = 1

    employees = list()
    for employee in Employee.objects(team_id=team_id):
        employees.append(EmployeeDTO(
            employee.id.__str__(),
            employee.name,
            employee.surname,
            employee.tenure,
            employee.salary,
        ).__dict__)

        employee_cost = 0
        if employee.salary <= SALARY_BORDERS[0]:
            employee_cost = 1
        elif SALARY_BORDERS[0] < employee.salary < SALARY_BORDERS[1]:
            employee_cost = 2
        elif employee.salary >= SALARY_BORDERS[1]:
            employee_cost = 3

        employee_quality = 0
        if employee.tenure <= TENURE_BORDERS[0]:
            employee_quality = 1
        elif TENURE_BORDERS[0] < employee.tenure < TENURE_BORDERS[1]:
            employee_quality = 2
        elif employee.tenure >= TENURE_BORDERS[1]:
            employee_quality = 3

        cost += employee_cost
        quality += employee_quality

    speed += employees.__len__()
    image = io.BytesIO()
    labels = 'Speed', 'Cost', 'Quality'
    sizes = [speed, cost, quality]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, shadow=True, startangle=90)
    ax1.axis('equal')
    plt.savefig(image, format='png')
    image.seek(0)
    chart_base64 = base64.b64encode(image.read()).decode("utf-8")

    return render(request, "team-view.html",
                  {
                      'employees': employees,
                      'team_id': team_id,
                      'team_name': team.name,
                      'chart_base64': chart_base64
                  })


def employee_create(request, team_id):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form_data = form.data
            employee = Employee()
            employee.team_id = team_id
            employee.name = form_data.get("name")
            employee.surname = form_data.get("surname")
            employee.tenure = form_data.get("tenure")
            employee.salary = form_data.get("salary")
            employee.save()
            return redirect('/team-view/' + team_id)
    else:
        form = EmployeeForm()
    return render(request, 'employee-create.html', {'form': form, 'team_id': team_id})


def employee_upload(request, team_id):
    if request.method == "POST":
        employee_list = request.FILES.get("employee_list")
        workbook = openpyxl.load_workbook(employee_list)
        worksheet = workbook["Employees"]

        for row in worksheet.iter_rows(min_row=2, values_only=True):
            employee = Employee()
            employee.team_id = team_id
            employee.name = row[0]
            employee.surname = row[1]
            employee.tenure = row[2]
            employee.salary = row[3]
            employee.save()

    return redirect('/team-view/' + team_id)


def employee_update(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    form = EmployeeForm(initial={'name': employee.name,
                                 'surname': employee.surname,
                                 'tenure': employee.tenure,
                                 'salary': employee.salary})
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form_data = form.data
            employee.name = form_data.get("name")
            employee.surname = form_data.get("surname")
            employee.save()
            return redirect('/team-view/' + employee.team_id)
    return render(request, 'employee-update.html', {'form': form, 'team_id': employee.team_id})


def employee_delete(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    employee.delete()
    return redirect('/team-view/' + employee.team_id)
