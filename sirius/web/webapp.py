"""Main server entry. Run like:

$ bin/gunicorn -k flask_sockets.worker sirius.server:app -b 0.0.0.0:5002 -w 1
"""
import gevent
import logging
import flask
import flask_sockets
from flask_bootstrap import Bootstrap
from flask_cors import CORS

from sirius.protocol import protocol_loop
from sirius import stats
from sirius import config

# Import models so they get picked up for migrations. Do not remove.
from sirius.models import db
from sirius.models import user
from sirius.models import hardware
from sirius.models import messages

from sirius.web import landing
from sirius.web import twitter
from sirius.web import login
from sirius.web import admin
from sirius.web import printer_print
from sirius.web import printer_overview
from sirius.web import external_api
from sirius.web import print_key_api


logger = logging.getLogger(__name__)
sockets = flask_sockets.Sockets()


def create_app(config_name):
    app = flask.Flask(__name__)
    app.config.from_object(config.config[config_name])
    config.config[config_name].init_app(app)

    # Allow the printkey API to be browser accessible
    CORS(app, resources={r"/printkey/*": {"origins": "*"}})

    # Configure various plugins and logging
    bootstrap = Bootstrap(app)
    db.db.init_app(app)
    sockets.init_app(app)
    login.manager.init_app(app)
    logging.basicConfig(level=logging.DEBUG if app.debug else logging.INFO)

    # Register blueprints
    app.register_blueprint(stats.blueprint)
    app.register_blueprint(landing.blueprint)
    app.register_blueprint(twitter.blueprint, url_prefix="/login")
    app.register_blueprint(printer_overview.blueprint)
    app.register_blueprint(printer_print.blueprint)
    app.register_blueprint(external_api.blueprint)
    app.register_blueprint(admin.blueprint)
    app.register_blueprint(print_key_api.blueprint)

    # Live interactions.
    gevent.spawn(protocol_loop.mark_dead_loop)
    @sockets.route('/api/v1/connection')
    def api_v1_connection(ws):
        with app.app_context():
            protocol_loop.accept(ws)

    logger.debug('Creating app.')
    return app
