import os
from flask import Flask

from views import news

# instantiate the app
app = Flask(__name__)

# set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

# register blueprints
app.register_blueprint(news)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
