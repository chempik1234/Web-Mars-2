from data import db_session
from data.__all_models import *
from flask import jsonify
from flask_restful import Resource, abort, reqparse
from werkzeug.security import generate_password_hash
parser = reqparse.RequestParser()
parser.add_argument('team_leader', required=True, type=int)
parser.add_argument('job', required=True)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('collaborators', required=True)
parser.add_argument('start_date', required=True)
parser.add_argument('end_date', required=True)
parser.add_argument('address', required=True)
parser.add_argument('is_finished', required=True, type=bool)
parser.add_argument('category', required=True, type=int)


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(job_id)
    if not jobs:
        abort(404, message=f"Job {job_id} not found")


def set_password(password):
    return generate_password_hash(password)


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(User).get(job_id)
        return jsonify({'job': job.to_dict(
            only=('team_leader', 'job', 'work_size', 'collaborators',
                  'start_date', 'end_date', 'address', 'is_finished',
                  'category'))})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        job = session.query(Jobs).all()
        return jsonify({'job': [item.to_dict(
            only=('team_leader', 'job', 'work_size', 'collaborators',
                  'start_date', 'end_date', 'address', 'is_finished',
                  'category')) for item in job]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        job = Jobs(
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            start_date=args['start_date'],
            end_date=args['end_date'],
            address=args['address'],
            is_finished=args['is_finished'],
            category=args['category']
        )
        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})
