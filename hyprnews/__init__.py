# python -m flask --app hyprnews init-db
# python -m flask --app hyprnews run

from flask import Flask
from .models import db, migrate
import os
import click

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///hyprnews.v2.sqlite.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO= True # Set to True to log all SQL
    )

    db.init_app(app)
    migrate.init_app(app, db)

    if test_config is None:
        # load the instance config
        app.config.from_pyfile('config.py', silent=True)
    else:
        # test config
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # db.init_app(app)
    @app.cli.command('init-db')
    @click.option('--empty', is_flag=True, help="Create schema only, no mock data")
    def init_db_command(empty):
        """Clear the existing data and create new tables."""
        #init_db(app, schema_only=empty)
        with app.app_context():
            db.create_all()
            if not empty:
                seed_db(db)
        click.echo('Initialized the database' + ('' if empty else ' with mock data.'))

    #
    # BLUEPRINTS
    #
    from . import news
    app.register_blueprint(news.bp)
    app.add_url_rule('/', endpoint='index')

    return app

#
# TODO - decide where this should live 
#
def seed_db(db):
    from .models import Article

    mock_articles = [
        Article(
            title="OrangePi 5 Ultra Review",
            body="Following our review of their recent RV2 RISC-V board, "
                    "OrangePi has offered us to review one of their latest ARM64 "
                    "based hardware, the OrangePi 5 Ultra. This is currently "
                    "their highest specs ARM64 SBC.",
            url="https://boilingsteam.com/orange-pi-5-ultra-review/"
        ),
        Article(
            title="PHP 8.4 Installation and Upgrade guide for Ubuntu and Debian",
            body="A guide for Debian and Ubuntu on how to install PHP 8.4 on a new "
                    "server or how to upgrade an existing PHP setup to PHP 8.4.",
            url="https://php.watch/articles/php-84-install-upgrade-guide-debian-ubuntu"
        ),
        Article(
            title="How to fix PHP Curl HTTPS Certificate Authority issues on Windows",
            body="A successful HTTPS request involves the HTTP client validating the "
                    "server-provided TLS certificate against a list of known and trusted "
                    "root certificates. The PHP Curl extension is not different; the Curl "
                    "extension uses libcurl to make the HTTPS request, and libcurl, which "
                    "in turn uses a TLS library such as OpenSSL to validate the request.",
            url="https://php.watch/articles/php-curl-windows-cainfo-fix"
        )
    ]

    db.session.add_all(mock_articles)
    db.session.commit()
