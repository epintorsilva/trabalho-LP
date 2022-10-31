from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

''' Iniciallização da conexão do SQLAlchemy com o banco de dados'''
db = SQLAlchemy()

'''Esta função instancia a aplicação e registra nela configurações de banco de dados,
    gerenciamento de sessão e rotas.
'''
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    '''Configuração do gerenciamento de seção'''
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça o login para acessar essa página.'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id ):
        return User.query.get(int(user_id))

    '''Registro de rotas'''
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    '''Criação do arquivo do banco de dados'''
    with app.app_context():
        db.create_all()

    return app