import csv
from datetime import date
from django.http import HttpResponse
from unidecode import unidecode

def calculate_age(born, today = date.today()):
    try:
        birthday = born.replace(year=today.year)
    except ValueError:
        birthday = born.replace(year=today.year, day=born.day-1)
    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year

def parseInt(integer):
    try:
        value = int(integer)
    except ValueError:
        value = None
    return value

def parseFloat(integer):
    try:
        return float(integer)
    except ValueError:
        return None

class DateException(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)

def csvDump(model, name = "excelfile"):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename='+name+'.csv'
    writer = csv.writer(response, delimiter=';')
    row = []
    for mo in model:
        row.append(unidecode(mo))
    writer.writerow(row)
    return response

def median(mylist):
    sorts = sorted(mylist)
    length = len(sorts)
    if not length % 2:
        return (sorts[length / 2] + sorts[length / 2 - 1]) / 2.0
    return sorts[length / 2]