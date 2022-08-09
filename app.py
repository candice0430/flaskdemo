from flask import Flask
import config
from ext import db,mail
from blueprints import user_bp,qa_bp
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(config)
# app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
mail.init_app(app)

app.register_blueprint(user_bp)
app.register_blueprint(qa_bp)

migrate = Migrate(app,db)


@app.route('/')
def hello_world():  # put application's code here
    engine = db.get_engine()
    with engine.connect() as conn:
        res = conn.execute("select 1")
        print(res)
        return "hhhh"


if __name__ == '__main__':
    app.run()
