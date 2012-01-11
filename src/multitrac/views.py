from pyramid.view import view_config
from pyramid.renderers import get_renderer
from pyramid.response import Response

from multitrac.models import DBSession
from multitrac.models import MyModel

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
    return { "master":master}

@view_config(route_name="tickets", renderer='templates/tickets.pt')
def tickets_view(request):
    """docstring for tickets_view"""
    master = get_renderer('templates/master.pt').implementation()
    return { "master": master}

@view_config(route_name="settings", renderer='templates/settings.pt')
def settings_view(request):
    """docstring for settings_view"""
    master = get_renderer('templates/master.pt').implementation()
    return { "master":master}

#@view_config(route_name='tickets')
#def myview(request):
        #return Response('OK')
