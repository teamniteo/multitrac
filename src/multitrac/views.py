import pickle
import types

from pyramid.view import view_config
from pyramid.renderers import get_renderer
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer
from dateutil.relativedelta import relativedelta

import multitrac.trac
import multitrac.date as date


class Formdata(object):
    """docstring for Formdata"""

    def __init__(self):
        self.name = []
        self.options = []

    def form_parser(self, data):
        """docstring for users_parser"""
        data = data.split("\r\n")
        data[:] = [item for item in data if item]
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

@view_config(route_name="root", renderer='templates/root.pt')
def root_view(request):
    """docstring for root_view"""
    master = get_renderer('templates/master.pt').implementation()
    return {"master": master}

@view_config(route_name="hours", renderer='templates/hours.pt')
def hours_view(request):
    """docstring for hours_view"""
    master = get_renderer('templates/master.pt').implementation()

    with open("sql/tracs") as file:
        tracs = pickle.load(file)
    with open("sql/users") as file:
        users = pickle.load(file)

    formdata = Formdata()
    formdata.error = False
    repositories = []
    all_hours = []
    hours = []

    if request.params:
        user = request.params.getall("Users")[0]
        month = int(request.params.getall("Month")[0])
        week = int(request.params.getall("Week")[0])
        if not (month == 0 or week == 0):
            formdata.error = True
        else:
            for trac in tracs:
                h = multitrac.trac.HourCalculator()
                h.set_server_url(*trac)
                h.connect()
                if month == 0:
                    h.firstday, h.lastday = date.get_edge_days_week(week)
                    tickets = h.get_recent_tickets()
                    hours = h.calculate_hours(tickets, user)
                if week == 0:
                    h.firstday, h.lastday = date.get_edge_days_month(month)
                    tickets = h.get_recent_tickets()
                    hours = h.calculate_hours(tickets, user)
                all_hours.append(hours)
                repositories.append(h.get_repository_name(trac[2]))

    formdata.values = range(0, -9, -1)

    formdata.name.append("Users")
    formdata.options.append(users)

    formdata.name.append("Month")
    none = [(0, "None")]
    months = none[:]
    weeks = none[:]
    for month in range(-1, -9, -1):
        # foo
        firstday, lastday = date.get_edge_days_month(month)
        months.append((month,
            firstday.strftime("%Y-%m-%d ") +
            "=>" +
            lastday.strftime(" %Y-%m-%d")
            ))
    formdata.options.append(months)

    formdata.name.append("Week")
    for week in range(-1, -9, -1):
        firstday, lastday = date.get_edge_days_week(week)
        lastday = lastday + relativedelta(days=-1)
        weeks.append((week,
            firstday.strftime("%Y-%m-%d ") +
            "=>" +
            lastday.strftime(" %Y-%m-%d")
            ))
    formdata.options.append(weeks)

    form = Form(request)

    return dict(master=master,
            renderer=FormRenderer(form),
            formdata=formdata,
            repositories=repositories,
            hours=all_hours)


@view_config(route_name="tickets", renderer='templates/tickets.pt')
def tickets_view(request):
    """docstring for tickets_view"""
    master = get_renderer('templates/master.pt').implementation()

    with open("sql/tracs") as file:
        tracs = pickle.load(file)
    with open("sql/users") as file:
        users = pickle.load(file)

    formdata = Formdata()
    all_tickets = []
    rep_tickets = []
    repositories = []

    h = multitrac.trac.TrackUtil()

    if request.params:
        user = request.params.getall("Users")[0]
        for trac in tracs:
            #h = TrackUtil()
            h.set_server_url(*trac)
            h.connect()
            active_tickets = h.get_active_tickets(user)
            if active_tickets:
                for id in active_tickets:
                    name = h.get_ticket_name(id)
                    url = h.get_ticket_url(id)
                    ticket = [id, name, url]
                    rep_tickets.append(ticket)

                # trac[2] url
                all_tickets.append(rep_tickets)
                rep_tickets = []
                repositories.append(h.get_repository_name(trac[2]))

    formdata.name.append("Users")
    formdata.options.append(users)

    form = Form(request)

    return dict(master=master,
            renderer=FormRenderer(form),
            formdata=formdata,
            tickets=all_tickets,
            repositories=repositories
            )


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
