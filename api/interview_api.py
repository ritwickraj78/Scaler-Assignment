from datetime import datetime, timedelta

from flask import jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from sqlalchemy import or_, and_

from api.models import Admin, InterviewDetails, Interviewer, InterviewCandidate
from api.server import app, user_hash_manager, db
from api.utils import __authenticate_request


@app.route('/api/admin/login/', methods=['POST'])
def admin_login_api():
    if not __authenticate_request(request.headers['Secret']):
        return jsonify(error="Forbidden"), 403
    if not request.json:
        return jsonify(error="Invalid Request Body"), 500

    if 'email' not in request.json or 'password' not in request.json:
        return jsonify(error="Invalid Request Body"), 500

    admin_email = request.json['email'].lower().strip()
    admin = Admin.query.filter_by(email=admin_email).first()
    if not admin:
        return jsonify({"success": False, "error": "No account with this email id"})

    is_password_verified = admin.check_password(request.json['password'])
    if not is_password_verified:
        return jsonify({"error": 'Incorrect Password', "success": False})
    hashed_user_id = user_hash_manager.encode(admin.id)
    access_token = create_access_token(identity=hashed_user_id)
    refresh_token = create_refresh_token(identity=hashed_user_id)
    return jsonify({'access_token': access_token, 'refresh_token': refresh_token})


@app.route('/api/admin/interview/', methods=['POST'])
@jwt_required
def update_interview_details():
    if not __authenticate_request(request.headers['Secret']):
        return jsonify(error="Forbidden"), 403
    admin_id = user_hash_manager.decode(get_jwt_identity())[0]
    if not request.json:
        return jsonify("Missing Request Body")
    if 'interview_id' not in request.json or \
            'start_time' not in request.json or 'duration' not in request.json:
        return jsonify("Invalid Request Body")
    start_time = datetime.strptime(request.json['start_time'], '%d-%m-%Y %H:%M').time()
    duration = int(request.json['duration'])

    interview_details = InterviewDetails.query.get(int(request.json['interview_id']))
    if not interview_details:
        return jsonify({"success": False, "error": "No interview with this id"})
    interviewer = Interviewer.query.filter_by(email=request.json['interviewer_email']).first()
    interviewee = InterviewCandidate.query.filter_by(email=request.json['interviewee_email']).first()
    if not interviewer or not interviewee:
        return jsonify({"error": "Person not found", "success": False})
    interviewer_schedule = InterviewDetails.query.filter_by(interviewer_id=interviewer.id, is_cancelled=False). \
        filter(or_((and_(InterviewDetails.start_time <= start_time,
                         start_time < (InterviewDetails.start_time + timedelta(minutes=duration)))),
                   (and_(InterviewDetails.start_time < (start_time + timedelta(minutes=duration)),
                         (start_time + timedelta(minutes=duration)) <=
                         (InterviewDetails.start_time + timedelta(minutes=duration)))))).all()
    interviewee_schedule = InterviewDetails.query.filter_by(interviewee_id=interviewee.id, is_cancelled=False). \
        filter(or_((and_(InterviewDetails.start_time <= start_time,
                         start_time < (InterviewDetails.start_time + timedelta(minutes=InterviewDetails.duration)))),
                   (and_(InterviewDetails.start_time < (start_time + timedelta(minutes=duration)),
                         (start_time + timedelta(minutes=duration)) <=
                         (InterviewDetails.start_time + timedelta(minutes=InterviewDetails.duration)))))).all()
    if interviewer_schedule:
        return jsonify({"error": True, "message": "Interviewer is Busy"})
    if interviewee_schedule:
        return jsonify({"error": True, "message": "Interviewee is Busy"})
    interview_details.start_time = start_time
    interview_details.duration = duration
    db.session.add(interview_details)
    db.session.commit()
    return jsonify({'success': True, 'interview_id': interview_details.id})


@app.route('/api/admin/interview/', methods=['DELETE'])
@jwt_required
def delete_interview():
    if not __authenticate_request(request.headers['Secret']):
        return jsonify(error="Forbidden"), 403
    admin_id = user_hash_manager.decode(get_jwt_identity())[0]
    if not request.json:
        return jsonify("Missing Request Body")
    if 'interview_id' not in request.json:
        return jsonify("Invalid Request Body")
    interview_details = InterviewDetails.query.get(int(request.json['interview_id']))
    if not interview_details:
        return jsonify({"success": False, "error": "No interview with this id"})

    interview_details.is_cancelled = True
    db.session.add(interview_details)
    db.session.commit()
    return jsonify({'success': True, 'interview_id': interview_details.id})


@app.route('/api/admin/interview/create/', methods=['POST'])
@jwt_required
def create_interview():
    if not __authenticate_request(request.headers['Secret']):
        return jsonify(error="Forbidden"), 403
    admin_id = user_hash_manager.decode(get_jwt_identity())[0]
    if not request.json:
        return jsonify("Missing Request Body")
    if 'interviewer_email' not in request.json or 'interviewee_email' not in request.json or \
            'start_time' not in request.json or 'duration' not in request.json:
        return jsonify("Invalid Request Body")
    start_time = datetime.strptime(request.json['start_time'], '%d-%m-%Y %H:%M').time()
    duration = int(request.json['duration'])
    interviewer = Interviewer.query.filter_by(email=request.json['interviewer_email']).first()
    interviewee = InterviewCandidate.query.filter_by(email=request.json['interviewee_email']).first()
    if not interviewer or not interviewee:
        return jsonify({"error": "Person not found", "success": False})
    interviewer_schedule = InterviewDetails.query.filter_by(interviewer_id=interviewer.id, is_cancelled=False). \
        filter(or_((and_(InterviewDetails.start_time <= start_time,
                         start_time < (InterviewDetails.start_time + timedelta(minutes=duration)))),
                   (and_(InterviewDetails.start_time < (start_time + timedelta(minutes=duration)),
                         (start_time + timedelta(minutes=duration)) <=
                         (InterviewDetails.start_time + timedelta(minutes=duration)))))).all()
    interviewee_schedule = InterviewDetails.query.filter_by(interviewee_id=interviewee.id, is_cancelled=False). \
        filter(or_((and_(InterviewDetails.start_time <= start_time,
                         start_time < (InterviewDetails.start_time + timedelta(minutes=duration)))),
                   (and_(InterviewDetails.start_time < (start_time + timedelta(minutes=duration)),
                         (start_time + timedelta(minutes=duration)) <=
                         (InterviewDetails.start_time + timedelta(minutes=duration)))))).all()
    if interviewer_schedule:
        return jsonify({"error": True, "message": "Interviewer is Busy"})
    if interviewee_schedule:
        return jsonify({"error": True, "message": "Interviewee is Busy"})
    interview_details = InterviewDetails(
        start_time=start_time,
        duration=duration,
        interviewer_id=interviewer.id,
        interviewee_id=interviewee.id,
        created_by=admin_id
    )
    db.session.add(interview_details)
    db.session.commit()
    return jsonify({'success': True, 'interview_id': interview_details.id})


@app.route('/api/admin/interview/', methods=['GET'])
@jwt_required
def get_interview_details():
    if not __authenticate_request(request.headers['Secret']):
        return jsonify(error="Forbidden"), 403
    admin_id = user_hash_manager.decode(get_jwt_identity())[0]
    if not request.json:
        return jsonify("Missing Request Body")
    if 'interview_id' not in request.json:
        return jsonify("Invalid Request Body")
    interview_details = InterviewDetails.query.get(int(request.json['interview_id']))
    if not interview_details:
        return jsonify({"success": False, "error": "No interview with this id"})
    interviewer = Interviewer.query.get(interview_details.interviewer_id)
    interviewee = InterviewCandidate.query.get(interview_details.interviewee_id)
    admin = Admin.query.get(admin_id)
    return jsonify({'success': True,
                    "data": {'interview_id': interview_details.id,
                             'interview_start': str(interview_details.start_time),
                             'interview_duration': interview_details.duration,
                             'interviewer': interviewer.email,
                             'interviewee': interviewee.email,
                             'created_by': admin.email}})


@app.route('/api/admin/interviews/', methods=['GET'])
@jwt_required
def get_interviews_list():
    if not __authenticate_request(request.headers['Secret']):
        return jsonify(error="Forbidden"), 403
    now = datetime.utcnow()
    interviews = InterviewDetails.query.filter_by(is_cancelled=False).order_by(InterviewDetails.start_time).all()
    past_interview_data = []
    upcoming_interview_data = []
    for interview in interviews:
        interviewer = Interviewer.query.get(interview.interviewer_id)
        interviewee = InterviewCandidate.query.get(interview.interviewee_id)
        if interview.start_time < now:
            past_interview_data.append({
                'start_time': str(interview.start_time),
                'interviewer': interviewer.email,
                'interviewee': interviewee.email,
                'duration': interview.duration,
            })
        else:
            upcoming_interview_data.append({
                'start_time': str(interview.start_time),
                'interviewer': interviewer.email,
                'interviewee': interviewee.email,
                'duration': interview.duration,
            })
    return jsonify({'success': True,
                    'upcoming_interviews': upcoming_interview_data,
                    'past_interviews': past_interview_data})


@app.route('/api/admin/people/', methods=['GET'])
@jwt_required
def get_people_list():
    if not __authenticate_request(request.headers['Secret']):
        return jsonify(error="Forbidden"), 403
    interviewers = Interviewer.query.all()
    interviewees = InterviewCandidate.query.all()
    interviewers_data = []
    interviewees_data = []
    for interviewer in interviewers:
        interviewers_data.append({
            "email": interviewer.email,
            'name': interviewer.name
        })
    for interviewee in interviewees:
        interviewees_data.append({
            "email": interviewee.email,
            'name': interviewee.name
        })
    return jsonify({'success': True, 'interviewees': interviewees_data, 'interviewers': interviewers_data})
