#!/usr/bin/env python3

from tldr import mail
from tldr.model import db, MailTask
from datetime import datetime

if __name__ == '__main__':
    for m in MailTask.query.filter_by(sent=None):
        try:
            mail.send(
                '"TLDR" <webmaster@tldrify.com>', [m.recipient],
                m.subject,
                html=m.body)
            m.sent = datetime.now()
            db.session.commit()
        except:
            pass
