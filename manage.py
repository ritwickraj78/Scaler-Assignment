from flask_migrate import MigrateCommand
from flask_script import Manager, Server

from api.models import Admin
from api.server import app, db

manager = Manager(app)
manager.add_command("runserver", Server(host="0.0.0.0", port="5000"))

manager.add_command('db', MigrateCommand)
app.config['DEBUG'] = True


@manager.command
def create_admin():
    admin = Admin(email="ritwick@admin.com", password="password")
    db.session.add(admin)
    db.session.commit()

if __name__ == '__main__':  # pragma: no cover
    manager.run()


