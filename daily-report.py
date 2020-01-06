#!/usr/bin/env python3

from tldr import mail
from tldr.model import db, Citation, CitationView, User
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader


if __name__ == '__main__':
    now = datetime.now()
    day_ago = now - timedelta(days=1)

    # Find new users
    new_users = []
    for u in User.query.filter(User.created >= day_ago):
        new_users.append(u)

    # Find new citations
    new_citations = []
    for c in Citation.query.filter(Citation.created >= day_ago):
        new_citations.append(c)

    # Find new broken links
    broken_links = []
    for c in db.session.query(Citation).join(CitationView).filter(
            CitationView.xpath_failure == True).filter(
                Citation.created >= day_ago):
        broken_links.append(c)

    jinja_env = Environment(loader=FileSystemLoader('tldr/templates'))
    template = jinja_env.get_template('emails/daily_report.html')
    html = template.render(
        since=day_ago.strftime('%d %B, %Y'),
        new_users=new_users,
        new_citations=new_citations,
        broken_links=broken_links)

    mail.send(
        '"TLDRify" <webmaster@tldrify.com>', ['webmaster@tldrify.com'],
        'tldrify.com - Daily Report',
        html=html)
