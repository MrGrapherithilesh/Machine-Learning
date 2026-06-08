from app import create_app
from config import APP_PORT


if __name__ == "__main__":
    app = create_app()
    app.run(debug=False, port=APP_PORT, use_reloader=False)
