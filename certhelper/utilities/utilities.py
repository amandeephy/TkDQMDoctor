import datetime

from django.utils import timezone


def is_valid_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except:
        return False


def get_date_string(year, month, day):
    """"
    returns empty string if date is invalid
    returns YYYY-MM-DD if date is valid
    """

    datestring = None

    if year and month and day:  # if attributes exist
        if int(year) in range(1900, 3000) and int(month) in range(1, 13) and int(day) in range(1, 32):
            if len(month) == 1: month = "0" + month
            if len(day) == 1: day = "0" + day
            datestring = year + "-" + month + "-" + day

    if is_valid_date(datestring):
        return datestring
    return ""


def get_filters_from_request_GET(request):
    filter_candidates = [
        'category',
        'subcategory',
        'subsubcategory',
        'date_range_0',
        'date_range_1',
        'runs_0',
        'runs_1',
        'type',
    ]
    applied_filters = {}
    for candidate in filter_candidates:
        tmp = request.GET.get(candidate, '')
        if tmp != '' and tmp != 0:
            if not candidate.startswith('date_range') or candidate.startswith('date_range') and is_valid_date(tmp):
                applied_filters[candidate] = tmp

    year = request.GET.get('date_year', '')
    month = request.GET.get('date_month', '')
    day = request.GET.get('date_day', '')

    the_date = get_date_string(year, month, day)

    # TODO solve conflict between two dates set
    if request.GET.get('date', ''):
        the_date = request.GET.get('date', '')

    if the_date:
        applied_filters['date'] = the_date

    return applied_filters


def is_valid_id(primary_key, Classname):
    try:
        if Classname.objects.filter(pk=primary_key):
            return True
    except:
        return False
    return False


def request_contains_filter_parameter(request):
    for candidate in ["options", "category", "runs", "type", "date", "userid"]:
        for word in request.GET:
            if candidate in word:
                return True
    return False


def get_this_week_filter_parameter():
    start_of_week = timezone.now() - timezone.timedelta(timezone.now().weekday())
    end_of_week = start_of_week + timezone.timedelta(6)

    date_gte = str(start_of_week.year) + "-" + str(start_of_week.month) + "-" + str(start_of_week.day)
    date_lte = str(end_of_week.year) + "-" + str(end_of_week.month) + "-" + str(end_of_week.day)

    get_parameters = "?date__gte=" + str(date_gte)
    get_parameters += "&date__lte=" + str(date_lte)

    return get_parameters


def get_today_filter_parameter():
    return "?date={}".format(timezone.now().strftime('%Y-%m-%d'))


def get_from_summary(summary, runtype=None, reco=None, date=None):
    filtered = summary
    if runtype:
        filtered = [item for item in filtered if item['type__runtype'] == runtype]
    if reco:
        filtered = [item for item in filtered if item['type__reco'] == reco]
    if date:
        filtered = [item for item in filtered if item['date'] == to_date(date)]
    return filtered


def to_date(date, formatstring="%Y-%m-%d"):
    if isinstance(date, datetime.datetime):
        return date.date()
    if isinstance(date, datetime.date):
        return date
    return datetime.datetime.strptime(date, formatstring).date()


def to_weekdayname(date, formatstring="%Y-%m-%d"):
    return to_date(date, formatstring).strftime("%A")


def get_full_name(user):
    name = ""
    if user.first_name:
        name += str(user.first_name) + " "
    if user.last_name:
        name += str(user.last_name) + " "

    if name:
        name += "(" + str(user.username) + ")"
    else:
        name += str(user.username)

    return name
