from __future__ import print_function
from xmlrpclib import ServerProxy
from collections import namedtuple

from multitrac.date import *

class TrackUtil(object):
    """docstring for TrackUtil"""
    def __init__(self):
        super(TrackUtil, self).__init__()

    def connect(self):
        """Connect to the xmlrpc server"""
        if not self.url:
            raise
        self.server = ServerProxy(self.url)

    # Url parsing may differ for your repository
    def get_repository_name(self, url):
        """docstring for get_repository_name"""
        url = url.split("/")
        return url[2]

    def get_ticket_name(self, id):
        name = self.server.ticket.get(id)[3]["summary"]
        return name

    def get_ticket_url(self, id):
        """docstring for get_ticket_url"""
        temp = self.rawurl.split("/")
        temp[5] = "ticket"
        temp[6] = str(id)
        url = "/".join(temp)
        return url

    def get_recent_tickets(self):
        """docstring for get_recent_tickets"""
        tickets = self.server.ticket.getRecentChanges(self.firstday)
        #tickets  = self.server.ticket.query("owner=ielectric")
        return list(tickets)

    def get_active_tickets(self, user):
        """docstring for get_active_tickets"""
        active = self.server.ticket.query("status!=closed")
        byuser = self.server.ticket.query("owner=" + user)
        set_ = set(active).intersection(set(byuser))
        return list(set_)

    def set_server_url(self, username, password, url):
        """docstring for set_server_url"""
        self.rawurl = "http://" + url
        self.url = "http://" + username + ":" + password + "@" + url

    def get_billable(self, ticket):
        """docstring for get_billable"""
        billable = self.server.ticket.get(ticket)[3]["billable"]
        return int(billable)

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

    def calculate_hours(self, tickets, user):
        """docstring for calculate_hours"""
        self.hours = [0, 0]
        for ticket in tickets:
            billable = self.get_billable(ticket)

            comments = self.get_comments([ticket])
            for comment in comments:
                #c = self._pretify_c(comment)

                Comment = namedtuple('Comment', 'date user tag hours')
                c = Comment(comment[0], comment[1], comment[2], comment[4])

                if self.firstday < c.date <= self.lastday \
                    and c.tag == "hours" \
                    and c.user == user:
                        if not c.hours:
                            pass
                        else:
                            if billable:
                                self.hours[0] += float(c.hours)
                            else:
                                self.hours[1] += float(c.hours)
        return self.hours
