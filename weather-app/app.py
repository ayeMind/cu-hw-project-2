from flask import Flask
from routes import register_blueprints

def init_app():
    app = Flask(__name__)

    with app.app_context():
        from dashboard import init_dashboard
        app = init_dashboard(app)
        return app

app = init_app()
register_blueprints(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, load_dotenv=True)