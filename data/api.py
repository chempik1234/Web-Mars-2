import flask
from data.__all_models import *
from flask import request
from data import db_session


blueprint = flask.Blueprint('jobs_api', __name__, template_folder='templates')
print(blueprint)


@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    print([i.id for i in jobs])
    return flask.jsonify({'jobs': [item.to_dict(
        only=('id', 'job', 'team_leader', 'work_size', 'collaborators',
              'start_date', 'end_date', 'is_finished', 'category')
    )
        for item in jobs]})


@blueprint.route('/api/jobs_add', methods=['POST'])
def add_job():
    db_sess = db_session.create_session()
    if not request.json:
        return flask.jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'job', 'team_leader', 'work_size', 'collaborators',
                  'start_date', 'end_date', 'is_finished', 'category']):
        return flask.jsonify({'error': 'Bad request'})
    elif db_sess.query(Jobs).filter(Jobs.id == request.json['id']).first():
        return flask.jsonify({'error': 'Id already exists'})
    jobs = Jobs(
        id=request.json['id'],
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        collaborators=request.json['collaborators'],
        start_date=request.json['start_date'],
        end_date=request.json['end_date'],
        address=request.json['address'],
        is_finished=request.json['is_finished'],
        category=request.json['category']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/jobs_get/<int:job_id>', methods=['GET'])
def get_job(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    print(jobs)
    if not jobs:
        return flask.jsonify({'error': 'Not found'})
    return flask.jsonify(
        {
            'jobs': jobs.to_dict(only=(
                'id', 'job', 'team_leader', 'work_size', 'collaborators',
                'start_date', 'end_date', 'is_finished', 'category')
            )
        }
    )


@blueprint.route('/api/jobs_delete/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(job_id)
    if not jobs:
        return flask.jsonify({'error': 'Not found'})
    db_sess.delete(jobs)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/jobs_edit/', methods=['PUT'])
def edit_job():
    db_sess = db_session.create_session()
    keyss = ['id', 'job', 'team_leader', 'work_size', 'collaborators',
             'start_date', 'end_date', 'is_finished', 'category']
    if not request.json:
        return flask.jsonify({'error': 'Empty request'})
    elif 'id' not in request.json or not all(key in keyss for key in request.json):
        return flask.jsonify({'error': 'Bad request'})
    elif not db_sess.query(Jobs).filter(Jobs.id == request.json['id']).first():
        return flask.jsonify({'error': 'Id does not exist'})
    jobs = Jobs(
        id=request.json['id'],
        team_leader=request.json.get('team_leader'),
        job=request.json.get('job'),
        collaborators=request.json.get('collaborators'),
        start_date=request.json.get('start_date'),
        end_date=request.json.get('end_date'),
        address=request.json.get('address'),
        is_finished=request.json.get('is_finished'),
        category=request.json.get('category')
    )
    if jobs.team_leader:
        db_sess.query(Jobs).filter(Jobs.id == jobs.id).update(values={Jobs.team_leader: jobs.team_leader})
    if jobs.job:
        db_sess.query(Jobs).filter(Jobs.id == jobs.id).update(values={Jobs.job: jobs.job})
    if jobs.collaborators:
        db_sess.query(Jobs).filter(Jobs.id == jobs.id).update(values={Jobs.collaborators: jobs.collaborators})
    if jobs.start_date:
        db_sess.query(Jobs).filter(Jobs.id == jobs.id).update(values={Jobs.start_date: jobs.start_date})
    if jobs.end_date:
        db_sess.query(Jobs).filter(Jobs.id == jobs.id).update(values={Jobs.end_date: jobs.end_date})
    if jobs.address:
        db_sess.query(Jobs).filter(Jobs.id == jobs.id).update(values={Jobs.address: jobs.address})
    if jobs.is_finished:
        db_sess.query(Jobs).filter(Jobs.id == jobs.id).update(values={Jobs.is_finished: jobs.is_finished})
    if jobs.category:
        db_sess.query(Jobs).filter(Jobs.id == jobs.id).update(values={Jobs.category: jobs.category})
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})