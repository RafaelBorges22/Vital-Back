from flask import Flask
from database.db import db
from models.ClientModel import ClientModel
from routers.ClientRouters import client_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vital.db'
db.init_app(app)

# Register the blueprint
app.register_blueprint(client_blueprint)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)