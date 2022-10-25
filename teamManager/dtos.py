class TeamDTO(object):

    def __init__(self, team_id, name, location):
        self.team_id = team_id
        self.name = name
        self.location = location


class EmployeeDTO(object):

    def __init__(self, employee_id, name, surname, tenure, salary):
        self.employee_id = employee_id
        self.name = name
        self.surname = surname
        self.tenure = tenure
        self.salary = salary
