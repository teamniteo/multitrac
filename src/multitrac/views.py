from pyramid.view import view_config
from pyramid.renderers import get_renderer
from pyramid.response import Response
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer

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

    def get_users(self):
        """docstring for get_users"""
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

    formdata = Formdata()
    formdata.name.append("Users")
    formdata.options.append([1, 2, 3])

    formdata.name.append("Month")
    formdata.options.append([1, 2, 3])

    formdata.name.append("Week")
    formdata.options.append([1, 2, 3])

    form = Form(request)

    formdata.error = False

    if request.method == "POST":
        print "lol"

    return dict(master=master, renderer=FormRenderer(form), formdata=formdata)

@view_config(route_name="tickets", renderer='templates/tickets.pt')
def tickets_view(request):
    """docstring for tickets_view"""
    master = get_renderer('templates/master.pt').implementation()

    formdata = Formdata()
    formdata.name.append("Users")
    formdata.options.append([1, 2, 3])

    form = Form(request)

    return dict(master=master, renderer=FormRenderer(form), formdata=formdata)

@view_config(route_name="settings", renderer='templates/settings.pt')
def settings_view(request):
    """docstring for settings_view"""
    master = get_renderer('templates/master.pt').implementation()
    return { "master":master}

