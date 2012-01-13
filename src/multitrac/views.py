import pickle
import types

from pyramid.view import view_config
from pyramid.renderers import get_renderer
from pyramid.response import Response
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer
import tracer.core
from dateutil.relativedelta import relativedelta

from multitrac.models import DBSession
from multitrac.models import User

class Formdata(object):
    """docstring for Formdata"""

    def __init__(self):
        self.name = []
        self.options = []

    def get_months(self):
        """docstring for calc_months"""
        pass

    def form_parser(self, data):
        """docstring for users_parser"""
        data = data.split("\r\n")
        data[:] =  [item for item in data if item]
        if not data:
            data = None
            return data
        if "|" not in data[0]:
            return data
        data[:] = [item.split("|") for item in data]
        return data

    def get_users(self):
        """docstring for get_users"""
        pass

    def create_text(self, list):
        """docstring for create_tracs_text"""
        if not list:
            string = ""
            return string

        if type(list[0]) == types.ListType:
            list[:] = ["|".join(item) for item in list if item]

        string = "\r\n".join(list)
        return string

    def get_tracs(self):
        """docstring for get_tracs"""
        pass

    def get_weeks(self):
        """docstring for get_weeks"""
        pass


def my_view(request):
    dbsession = DBSession()
    root = dbsession.query(MyModel).filter(MyModel.name==u'root').first()
    return { 'project':'multitrac'}

@view_config(route_name="root", renderer='templates/root.pt')
def root_view(request):
    """docstring for root_view"""
    master = get_renderer('templates/master.pt').implementation()
    return { "master":master}

@view_config(route_name="hours", renderer='templates/hours.pt')
def hours_view(request):
    """docstring for hours_view"""
    master = get_renderer('templates/master.pt').implementation()

    t = tracer.core.TrackUtil()
    formdata = Formdata()
    with open("sql/users") as file:
        users = pickle.load(file)

    formdata.values = range(0, -9, -1)

    formdata.name.append("Users")
    formdata.options.append(users)

    formdata.name.append("Month")
    none = [(0, "None")]
    months = none[:]
    weeks = none[:]
    for month in range(-1, -9, -1):
        firstday, lastday = t.get_edge_days_month(month)
        months.append((month,
            firstday.strftime("%Y-%m-%d ") +
            "=>" +
            lastday.strftime(" %Y-%m-%d")
            ))
    formdata.options.append(months)

    formdata.name.append("Week")
    for week in range(-1, -9, -1):
        firstday, lastday = t.get_edge_days_week(week)
        lastday = lastday + relativedelta(days=-1)
        weeks.append((week,
            firstday.strftime("%Y-%m-%d ") +
            "=>" +
            lastday.strftime(" %Y-%m-%d")
            ))
    formdata.options.append(weeks)

    form = Form(request)

    formdata.error = False


    return dict(master=master, renderer=FormRenderer(form), formdata=formdata)

@view_config(route_name="tickets", renderer='templates/tickets.pt')
def tickets_view(request):
    """docstring for tickets_view"""
    master = get_renderer('templates/master.pt').implementation()

    formdata = Formdata()

    with open("sql/users") as file:
        users = pickle.load(file)

    formdata.name.append("Users")
    formdata.options.append(users)

    form = Form(request)

    return dict(master=master, renderer=FormRenderer(form), formdata=formdata)

@view_config(route_name="settings", renderer='templates/settings.pt')
def settings_view(request):
    """docstring for settings_view"""
    master = get_renderer('templates/master.pt').implementation()

    tracs = None
    users = None

    formdata = Formdata()

    if request.params:
        tracs = request.params.getall("tracs")[0]
        users = request.params.getall("users")[0]
        formdata.tracs = formdata.form_parser(tracs)
        formdata.users = formdata.form_parser(users)
        with open("sql/tracs", "w") as file:
            pickle.dump(formdata.tracs, file)
        with open("sql/users", "w") as file:
            pickle.dump(formdata.users, file)

    with open("sql/tracs") as file:
        tracs = pickle.load(file)
    with open("sql/users") as file:
        users = pickle.load(file)

    tracs = formdata.create_text(tracs)
    users = formdata.create_text(users)



    formdata.tracs = tracs or None
    formdata.users = users or None

    form = Form(request)

    return dict(master=master, renderer=FormRenderer(form), formdata=formdata)
