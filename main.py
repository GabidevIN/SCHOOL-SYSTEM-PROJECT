from flask import Flask
from views import web


sys = Flask(__name__)
sys.register_blueprint(web, url_prefix="/")


if __name__ == '__main__':
    sys.run(debug=True, port=8000)