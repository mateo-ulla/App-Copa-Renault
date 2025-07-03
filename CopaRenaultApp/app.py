from flask import Flask, request, redirect
from config import Config
from models import db
from routes import main_bp
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config.from_object(Config)

# Forzar HTTPS si está en producción
@app.before_request
def before_request():
    if not app.debug and not request.is_secure:
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)


# Inicializar extensiones
db.init_app(app)
jwt = JWTManager(app)


# Registrar blueprint
app.register_blueprint(main_bp)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
