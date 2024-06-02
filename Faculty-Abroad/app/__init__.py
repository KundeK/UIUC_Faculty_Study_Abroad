"""Setup at app startup"""
import os
import sys
import sqlalchemy
from flask import Flask
import logging
from yaml import load, Loader



def init_connection_engine():
    """ initialize database setup
    Takes in os variables from environment if on GCP
    Reads in local variables that will be ignored in public repository.
    Returns:
        pool -- a connection to GCP MySQL
    """


    # detect env local or gcp
    if os.environ.get('GAE_ENV') != 'standard':
        try:
            variables = load(open("app/templates/app.yaml"), Loader=Loader)
        except OSError:
            print("Make sure you have the app.yaml file setup")
            sys.exit()

        env_variables = variables['env_variables']
        for var in env_variables:
            os.environ[var] = env_variables[var]

    # pool = sqlalchemy.create_engine(
    #     sqlalchemy.engine.url.URL(
    #         drivername="mysql+pymysql",
    #         username=os.environ.get('MYSQL_USER'),
    #         password=os.environ.get('MYSQL_PASSWORD'),
    #         database=os.environ.get('MYSQL_DB'),
    #         host=os.environ.get('MYSQL_HOST'),
    #         port=os.environ.get('MYSQL_PORT')
    #     )
    # )

    pool = sqlalchemy.create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            os.environ.get('MYSQL_USER'), os.environ.get('MYSQL_PASSWORD'), os.environ.get('MYSQL_HOST'), os.environ.get('MYSQL_PORT'), os.environ.get('MYSQL_DB')
        )
    )

    return pool




app = Flask(__name__)
db = init_connection_engine()

app.logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

# To prevent from using a blueprint, we use a cyclic import
# This also means that we need to place this import here
# pylint: disable=cyclic-import, wrong-import-position
from app import routes
