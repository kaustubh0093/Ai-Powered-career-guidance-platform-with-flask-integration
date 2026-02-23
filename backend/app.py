from flask import Flask, render_template
from flask_cors import CORS
from flasgger import Swagger
from backend.config import Config
from backend.routes.api import api_bp

def create_app():
    app = Flask(__name__, 
                static_folder='../frontend/static',
                template_folder='../frontend/templates')
    
    app.config.from_object(Config)
    
    # Enable CORS for all routes
    CORS(app)
    
    # Register API blueprint
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Initialize Swagger
    app.config['SWAGGER'] = {
        'title': 'Career AI Platform API',
        'uiversion': 3
    }
    Swagger(app)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    


    return app



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
