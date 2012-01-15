from __future__ import print_function
from ConfigParser import ConfigParser
from datetime import datetime, timedelta, date, time
from xmlrpclib import ServerProxy
from collections import namedtuple

from dateutil.relativedelta import relativedelta

class TrackUtil(object):
    """docstring for TrackUtil"""
    def __init__(self):
        super(TrackUtil, self).__init__()

    def insert_auth(self, url, username, password):
        """Simple function that inserts the username and password before the @"""
        if "{username}" in url and "{password}" in url:
            # look at a better function
            self.url_template = url.format(username=username, password=password, repository="{repository}")
        else:
            self.url = url

    def set_url(self, url):
        """Set url"""
        # do properties  like in c#
        self.url = url

    def connect(self):
        """Connect to the xmlrpc server"""
        self.server = ServerProxy(self.url)

    def insert_repo(self, repo):
        if "{repository}" in self.url_template:
            self.url = self.url_template.format(repository=repo)
        else:
            return self.url

    def get_edge_days_month(self, rel_month=-1):
        """get the first day of month and first of next month """

        today = date.today()
        midnight = time.min

        reldate = today + relativedelta(months=rel_month)

        last_day = reldate + relativedelta(day=1, months=+1)
        first_day = reldate + relativedelta(day=1)

        lastday, firstday = datetime.combine(last_day, midnight), datetime.combine(first_day, midnight)

        return firstday, lastday

    def get_edge_days_week(self, rel_week=-1):
        """get first day of week and first day of nexy week"""

        today = date.today()
        midnight = time.min

        reldate = today + relativedelta(weeks=rel_week)

        last_day = reldate + relativedelta(weekday=0)
        first_day = reldate + relativedelta(weeks=-1, weekday=0)

        lastday, firstday = datetime.combine(last_day, midnight), datetime.combine(first_day, midnight)

        return firstday, lastday

    def set_abs_month(self, abs_month, abs_year=None):
        """docstring for set_abs_month"""
        if not abs_year:
            abs_year = date.now().year

        midnight = time.min

        firstday = date(abs_year, abs_month)
        self.firstday = datetime.combine(firstday, midnight)

        lastday = date(abs_year, abs_month + 1)
        self.lastday = datetime.combine(lastday, midnight)

    def get_recent_tickets(self):
        """docstring for get_recent_tickets"""
        tickets = self.server.ticket.getRecentChanges(self.firstday)
        return tickets

    def get_active_tickets(self, user):
        """docstring for get_active_tickets"""
        active = self.server.ticket.query("status!=closed")
        byuser = self.server.ticket.query("owner="+user)
        return set(active).intersection(set(byuser))

    def get_comments(self, tickets):
        """docstring for get_comments"""
        tcomments = []
        for ticket in tickets:
            tcomments.extend(self.server.ticket.changeLog(ticket))

        return tcomments

    def _pretify_c(self, comment):
        """docstring for pretify_comment"""
        # no pretify just the two lines below
        # see namedtuple
        date, user, tag = comment[:3]
        hours = comment[4]
        dict = {
            "date": date,
            "user": user,
            "tag": tag,
            "hours": hours
        }

        return dict

# do it as a decorator
class HourCalculator(TrackUtil):
    """docstring for HourCalculator"""
    def __init__(self):
        super(HourCalculator, self).__init__()
        self.users = {}

    def calculate_hours(self, comments):
        """docstring for calculate_hours"""
        self.users = {}
        for comment in comments:
            #c = self._pretify_c(comment)

            Comment = namedtuple('Comment', 'date user tag hours')
            c = Comment(comment[0], comment[1], comment[2], comment[4])

            if self.firstday < c.date <= self.lastday and c.tag == "hours":
                if c.user not in self.users:
                    self.users[c.user] = 0
                if not c.hours:
                    pass
                else:
                    self.users[c.user] += float(c.hours)
        return self.users


def get_hours(username=None, password=None, repos=None, url=None):
    """function that is called by get_hours script"""

    # Url is missing
    if not (username and password and repos):
        print("This function takes 3 arguments: username, password, repos and url")

    # TODO: billable
    repositories = repos

    h = HourCalculator()
    h.firstday, h.lastday = h.get_edge_days_month()
    print(h.firstday, h.lastday,)
    h.insert_auth(url, username, password)
    for repo in repositories:
        h.insert_repo(repo)
        h.connect()
        tickets = h.get_recent_tickets()
        print(h.get_active_tickets("zupo"))
        if not tickets:
            continue
        comments = h.get_comments(tickets)
        print(repo)
        print(h.calculate_hours(comments))

if __name__ == "__main__":

    get_hours()
