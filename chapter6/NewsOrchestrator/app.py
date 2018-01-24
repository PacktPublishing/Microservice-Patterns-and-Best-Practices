import os
from flask import Flask

from views import news

app = Flask(__name__)

app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

app.register_blueprint(news)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
