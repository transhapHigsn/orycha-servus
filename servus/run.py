from flask import Flask
from servus.views import servus

app = Flask(__name__)
app.register_blueprint(servus)

if __name__ == '__main__':
    app.run(port=5000, debug=True)

