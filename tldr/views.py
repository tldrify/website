import requests
import os
import urllib
import re
from flask import render_template, request, abort, Response, redirect, url_for, send_from_directory, jsonify
from requests.exceptions import ConnectionError
from tldr import app
from tldr.model import db, Citation, User, MailTask
from tldr import utils
from flask_login import login_user, logout_user, current_user, login_required
from wtforms import form, fields, validators


def send_mail(mailto, subject, body):
    mailTask = MailTask(mailto, subject, body)
    db.session.add(mailTask)
    db.session.commit()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.errorhandler(500)
def page_500(e):
    return render_template('errors/500.html')


@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route('/tldrify.safariextz')
def safari_extension():
    return send_from_directory(
        app.static_folder,
        request.path[1:],
        mimetype="application/octet-stream")


@app.route('/tldrify.plist')
def safari_extension_manifest():
    return send_from_directory(
        app.static_folder, request.path[1:], mimetype="text/xml")


@app.route('/terms', methods=['GET'])
def terms():
    return render_template('terms.html')


@app.route('/privacy', methods=['GET'])
def privacy():
    return render_template('privacy.html')


@app.route('/help', methods=['GET'])
def help():
    return render_template('help.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        login_user(form.user, remember=True)
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("login.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = SignupForm(request.form)
    if request.method == "POST" and form.validate():
        user = User(form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for("index"))
    return render_template("signup.html", form=form)


@app.route("/resetpass", methods=["GET", "POST"])
def resetpass():
    form = ResetPasswordForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        body = render_template(
            'emails/reset_link.html', token=user.get_token())
        send_mail(user.email, 'Password reset on TLDRify', body)
        return render_template("reset_pass.html", form=form, sent=True)
    else:
        return render_template("reset_pass.html", form=form)


@app.route("/changepass", methods=["GET", "POST"])
def changepass():
    token = request.args.get('token', None)
    user = None
    if token is not None:
        user = User.verify_token(token)
    if token is None or user is None:
        return redirect(url_for("resetpass"))

    form = ChangePasswordForm(request.form)
    if request.method == "POST" and form.validate():
        user.password = form.password.data
        db.session.commit()
        return redirect(url_for("login"))
    else:
        return render_template("change_pass.html", form=form)


@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/manage", methods=["GET"])
@login_required
def manage():
    return render_template("manage.html", form=form)


@app.route('/sharebox', methods=['GET'])
def sharebox():
    return render_template(
        'sharebox.html',
        url=request.args.get('url', ''),
        title=request.args.get('title', ''))


@app.route('/ajaxproxy', methods=['GET', 'HEAD', 'POST', 'OPTIONS'])
def ajaxproxy():
    headers = {}
    for h in ['User-Agent', 'Cache-Control', 'Accept', 'Accept-Language']:
        headers[h] = request.headers.get(h)
    r = requests.request(
        request.method,
        request.args.get('url', ''),
        headers=headers,
        data=request.form,
        verify=False)
    response = Response(r.content)
    for h in ['Content-Type']:
        response.headers[h] = r.headers.get(h)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response


@app.route('/<id>', methods=['GET'])
def open(id):
    citation = Citation.by_short_id(id)
    if citation is None:
        abort(404)

    # Check that protocols match:
    cur_proto = request.url[0:request.url.index(':')]
    orig_proto = citation.url[0:citation.url.index(':')]
    if cur_proto != orig_proto:
        return redirect(
            request.url.replace(cur_proto, orig_proto, 1), code=301)

    try:
        headers = {}
        for h in ['User-Agent', 'Cache-Control', 'Accept', 'Accept-Language']:
            headers[h] = request.headers.get(h)
        response = requests.get(citation.url, headers=headers, verify=False)
    except ConnectionError:
        return render_template('errors/broken.html', url=citation.url)

    html, encoding, meta_encoding = utils.decode_response(response)
    html = utils.fix_base_url(html, citation.url)
    html = utils.inject_scripts(html, citation)

    content = html.encode(encoding, 'ignore')
    content_type = 'text/html; charset=%s' % (meta_encoding
                                              if meta_encoding else encoding)

    return Response(content, content_type=content_type)


@app.route("/feedback", methods=["POST"])
def feedback():
    body = render_template(
        'emails/feedback.html',
        email=request.form['email'],
        text=request.form['body'])
    send_mail('webmaster@tldrify.com', 'New Feedback on TLDRify', body)
    return Response(status=202)


class LoginForm(form.Form):
    email = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate(self):
        if not form.Form.validate(self):
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user is None or user.password != self.password.data:
            self.password.errors.append('Wrong e-mail or password')
            return False
        self.user = user
        return True


class SignupForm(form.Form):
    email = fields.TextField(
        validators=[validators.required(),
                    validators.Length(min=6, max=256)])
    password = fields.PasswordField(
        validators=[validators.required(),
                    validators.Length(min=1, max=256)])

    def validate(self):
        if not form.Form.validate(self):
            return False
        if User.query.filter_by(email=self.email.data).count() > 0:
            self.email.errors.append(
                'This e-mail address is already registered')
            return False
        return True


class ResetPasswordForm(form.Form):
    email = fields.TextField(
        validators=[validators.Required(),
                    validators.Email()])

    def validate(self):
        if not form.Form.validate(self):
            return False
        if User.query.filter_by(email=self.email.data).count() == 0:
            self.email.errors.append('The e-mail address is not found')
            return False
        return True


class ChangePasswordForm(form.Form):
    password = fields.PasswordField(
        validators=[validators.required(),
                    validators.Length(min=1, max=256)])
    confirm = fields.PasswordField()

    def validate(self):
        if not form.Form.validate(self):
            return False
        if self.password.data != self.confirm.data:
            self.confirm.errors.append('Passwords do not match')
            return False
        return True
