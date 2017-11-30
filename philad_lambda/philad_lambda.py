"""
This package runs the Philadelphia Reflections website as an AWS Lambda function

This file provides a connection to the MySQL database running on AWS RDS and
calls the main views of the system via Blueprint
"""
from flask import g, redirect, url_for

import sqlalchemy
import logging

# larger Flask apps utilize __init__.py for app setup
from philad_lambda import app

# ============= CONFIGURATION =============

# load config from this file
app.config.from_object(__name__)

# load default configs and include database info
MYSQL_USER = 'george'
MYSQL_PSWD = 'zareason'  # TODO: use KMS to encrypt/decrypt the password
MYSQL_ENDPOINT = 'philad.c2e2iknsgq7e.us-east-1.rds.amazonaws.com'
MYSQL_PORT_I = 3306
MYSQL_PORT_S = str(MYSQL_PORT_I)
MYSQL_DBNAME = 'philad'

app.config.update(dict(
    DATABASE='mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.
        format(MYSQL_USER, MYSQL_PSWD, MYSQL_ENDPOINT, MYSQL_PORT_S, MYSQL_DBNAME),
    SECRET_KEY='7H9YAl3exX8K^VlC!5E4h$vX5',  # created by LastPass # TODO: what is this?
    USERNAME=MYSQL_USER,
    PASSWORD=MYSQL_PSWD
    ))

# load additional settings from a file pointed to by an environment variable
# silent=True ignores errors if this variable is not set
app.config.from_envvar('PHILAD_SETTINGS', silent=True)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_db():
    """
    Connect to the the MySQL database on AWS RDS
    :return: the database connection
    """
    try:
        if not hasattr(g, 'mysql_db'):
            engine = sqlalchemy.create_engine(app.config['DATABASE'])
            g.mysql_db = engine.connect()
            logger.info("SUCCESS: connection to RDS successful")
        return g.mysql_db
    except Exception as e:
        logger.exception("Database Connection Error {}".format(str(e)))


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request"""
    if hasattr(g, 'mysql_db'):
        g.mysql_db.close()

# ============= VIEWS =============


@app.route('/')
def index():
    """no path specified redirects to the home page index.html"""
    return redirect(url_for('index_page_code.index_page'))


# home pages
from philad_lambda.Index_Page import index_page_code
app.register_blueprint(index_page_code)


if __name__ == '__main__':
    app.run()
