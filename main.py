from flask import Flask

from db import db
from routers import app as router


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "1234"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    db.init_app(app)
    app.register_blueprint(router)

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
