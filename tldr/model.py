import datetime
import hashlib

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from tldr import app
from urllib.parse import urlparse
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

db = SQLAlchemy(app)


def baseN(num, b, numerals='0123456789abcdefghijklmnopqrstuvwxyz'):
    return ((num == 0) and numerals[0]) or (
        baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])


def hash_password(password):
    h = hashlib.sha256()
    h.update(password.encode("utf-8"))
    return h.hexdigest()


class Citation(db.Model):
    __table_args__ = {'mysql_engine': 'MyISAM', 'mysql_charset': 'utf8'}
    OFFSET = 1000

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Unicode(length=2048), nullable=False)
    data = db.Column(db.UnicodeText, nullable=False)
    created = db.Column(
        db.DateTime, default=datetime.datetime.now, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    deleted = db.Column(db.DateTime)
    user_agent = db.Column(db.String(length=4094))
    views = db.relationship(
        'CitationView', order_by='desc(CitationView.time)', lazy='dynamic')

    def __init__(self, url, data, user_agent):
        self.url = url
        self.data = data
        self.user_agent = user_agent

    def short_id(self):
        return baseN(self.id + self.OFFSET, 36)

    def short_url(self):
        parsed_url = urlparse(self.url)
        return "%s://tldrify.com/%s" % (parsed_url.scheme, self.short_id())

    @staticmethod
    def short_id_to_id(id):
        return int(id, 36) - Citation.OFFSET

    @staticmethod
    def by_short_id(id):
        try:
            return Citation.query.filter_by(id=Citation.short_id_to_id(
                id)).filter_by(deleted=None).first()
        except ValueError:
            return None


class CitationView(db.Model):
    __table_args__ = {'mysql_engine': 'MyISAM', 'mysql_charset': 'utf8'}

    id = db.Column(db.Integer, primary_key=True)
    citation_id = db.Column(db.Integer, db.ForeignKey('citation.id'))
    time = db.Column(
        db.DateTime, default=datetime.datetime.now, nullable=False)
    user_agent = db.Column(db.String(length=4094))
    xpath_failure = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, citation_id, user_agent):
        self.citation_id = citation_id
        self.user_agent = user_agent


class User(db.Model, UserMixin):
    __table_args__ = {'mysql_engine': 'MyISAM', 'mysql_charset': 'utf8'}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Unicode(length=255), unique=True, nullable=False)
    password = db.Column(db.Unicode(length=255), nullable=False)
    created = db.Column(
        db.DateTime, default=datetime.datetime.now, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    citations = db.relationship(
        'Citation', order_by='desc(Citation.created)', lazy='dynamic')

    def __init__(self, email, password, active=True):
        self.email = email
        self.password = password
        self.active = active

    def is_active(self):
        return self.active

    def get_token(self, expiration=1800):
        s = Serializer(app.config['SECRET_KEY'], expiration)
        return s.dumps({'user': self.id}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        id = data.get('user')
        if id:
            return User.query.get(id)
        return None


class MailTask(db.Model):
    __table_args__ = {'mysql_engine': 'MyISAM', 'mysql_charset': 'utf8'}

    id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.Unicode(length=255), nullable=False)
    subject = db.Column(db.Unicode(length=255), nullable=False)
    body = db.Column(db.UnicodeText, nullable=False)
    submitted = db.Column(
        db.DateTime, default=datetime.datetime.now, nullable=False)
    sent = db.Column(db.DateTime)

    def __init__(self, recipient, subject, body):
        self.recipient = recipient
        self.subject = subject
        self.body = body
