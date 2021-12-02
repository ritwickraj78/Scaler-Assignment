from flask import Flask, request
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from hashids import Hashids

from api.config import configure_app

app = Flask(__name__)
print(app)
configure_app(app)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

user_hash_manager = Hashids(salt="9713yIJbsjuwgeEY2UQIHIuguei2E33E8Ooue@$", min_length=16)

app.config['JWT_SECRET_KEY'] = 'iu@$Efhffiuwefu7243@$2ey98je732ou&&e872e9bnf982kmfvcw83$@&(*#Ndfkfjfbj'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 60 * 60 * 3  # 3 hours
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = False
app.config['JWT_BLACKLIST_ENABLED'] = False

jwt = JWTManager(app)


@app.after_request
def after_every_response(response):
    whitelist_origins = ['http://localhost:3000']
    try:
        if request.referrer:
            r = request.referrer[:-1]
            if r in whitelist_origins:
                response.headers.add('Access-Control-Allow-Origin', r)
                response.headers.add('Access-Control-Allow-Credentials', 'true')
                response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
                response.headers.add('Access-Control-Allow-Headers', 'sentry-trace')
                response.headers.add('Access-Control-Allow-Headers', 'Cache-Control')
                response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
                response.headers.add('Access-Control-Allow-Headers', 'Authorization')
                response.headers.add('Access-Control-Allow-Headers', 'Secret')
                response.headers.add('Access-Control-Allow-Headers', 'secret')
                response.headers.add('Access-Control-Allow-Headers', 'Access-Control-Allow-Origin')
                response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
    except Exception as e:
        print(e)
    return response