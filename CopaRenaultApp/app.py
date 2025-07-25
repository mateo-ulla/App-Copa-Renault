from flask import Flask, request, redirect
from config import Config
from models import db
from routes import main_bp
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

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
migrate = Migrate(app, db)

# Registrar blueprint
app.register_blueprint(main_bp)

# Imports necesarios para el manejador de error
from flask import flash, session, url_for


from jwt.exceptions import ExpiredSignatureError
@app.errorhandler(ExpiredSignatureError)
def handle_expired_token(e):
    flash('Tu sesión ha expirado. Por favor, inicia sesión nuevamente.')
    session.clear()
    resp = redirect(url_for('main.login'))
    resp.delete_cookie('access_token_cookie')
    return resp

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)