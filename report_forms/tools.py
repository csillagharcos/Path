from datetime import date

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