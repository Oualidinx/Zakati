import os

from app_racine import create_app

from dotenv import load_dotenv
load_dotenv('.flaskenv')
app = create_app(os.environ.get('FLASK_ENV'))

if __name__ == "__main__":
    app.run(host="0.0.0.0")  # host="0.0.0.0", port="5050"