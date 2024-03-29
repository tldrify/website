from flask import Response, request, jsonify
from tldr import app
from tldr.model import db, Citation, CitationView, User
from tldr import utils
from flask_login import current_user, login_required
from sqlalchemy import text

import time, datetime


@app.route("/api/links", methods=["GET"])
@login_required
def links():
    per_page = int(request.args.get('perPage', 10))
    cur_page = int(request.args.get('currentPage', 1))

    order_by = ['created', 'desc']
    filter = []
    total = current_user.citations.filter_by(deleted=None).count()
    start = per_page * (cur_page - 1)
    end = start + per_page
    data = []

    sortargs = request.args.getlist('sort[0][]')
    if len(sortargs) == 2:
        if sortargs[1] != 'desc':
            sortargs[1] = 'asc'
        order_by = sortargs

    query = db.session.query(Citation, db.func.count(CitationView.id).label('views'))\
     .outerjoin(CitationView)\
     .group_by(Citation.id)\
     .filter(Citation.user_id==current_user.id)\
     .filter(Citation.deleted==None)\
     .order_by(text('{} {}'.format(*order_by)))

    for c, v in query[start:end]:
        data.append({
            'id': c.id,
            'short_url': c.short_url(),
            'url': c.url,
            'created': time.mktime(c.created.timetuple()),
            'views': v
        })

    return jsonify({
        'totalRows': total,
        'perPage': per_page,
        'currentPage': cur_page,
        'data': data,
        'sort': [order_by],
        'filter': filter
    })


@app.route('/api/links/<ids>', methods=['DELETE'])
def delete(ids):
    for c in Citation.query.filter(Citation.id.in_(ids.split('+'))):
        c.deleted = datetime.datetime.now()
    db.session.commit()
    return Response(status=202)


@app.route('/api/links/restore/<ids>', methods=['GET'])
def restore(ids):
    for c in Citation.query.filter(Citation.id.in_(ids.split('+'))):
        c.deleted = None
    db.session.commit()
    return Response(status=202)


@app.route('/api/create.js', methods=['GET'])
def create_js():
    url = request.args.get('url', '')
    data = request.args.get('data', '')

    citation = Citation(url, data, request.user_agent.string)
    citation.user_id = current_user.get_id()
    db.session.add(citation)
    db.session.commit()

    js = 'TLDR.restore("%s", "%s", %d, %s, true);' % (citation.url,
                                                      citation.short_url(),
                                                      citation.id, data)
    return Response(js, mimetype='application/javascript; charset=utf-8')

@app.route('/api/create', methods=['POST'])
def create():
    url = request.json['url'];
    data = request.json['data'];

    citation = Citation(url, data, request.user_agent.string)
    citation.user_id = current_user.get_id()
    db.session.add(citation)
    db.session.commit()

    return jsonify({
        'id': citation.id,
        'short_url': citation.short_url()
    })

@app.route('/api/citation/<id>/view', methods=['POST'])
def create_citation_view(id):
    view = CitationView(id, request.user_agent.string)
    view.xpath_failure = request.json['xpath_failure']
    db.session.add(view)
    db.session.commit()

    return Response(status=202)
