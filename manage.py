from flask_migrate import MigrateCommand
from flask_script import Manager, Server

from api.models import Admin, InterviewCandidate, Interviewer
from api.server import app, db

manager = Manager(app)
manager.add_command("runserver", Server(host="0.0.0.0", port="5000"))

manager.add_command('db', MigrateCommand)
app.config['DEBUG'] = True

@manager.command
def add_people():
    candidate = InterviewCandidate(name='Ritwick', email='ritwickraj78@gmail.com')
    db.session.add(candidate)
    InterviewCandidate(name='Rishab', email='rishabraj06@gmail.com')
    db.session.add(candidate)
    db.session.commit()
    interviewer = Interviewer(name='Interviewer 1', email='i1@scaler.com')
    db.session.add(interviewer)
    interviewer = Interviewer(name='Interviewer 2', email='i2@scaler.com')
    db.session.add(interviewer)
    db.session.commit()


@manager.command
def create_admin():
    admin = Admin(email="ritwick@admin.com", password="password")
    db.session.add(admin)
    db.session.commit()

if __name__ == '__main__':  # pragma: no cover
    manager.run()


