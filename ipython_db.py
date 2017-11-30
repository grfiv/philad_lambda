"""
when testing with IPython, %run ipython_db.py will setup a connection 'conn' to the RDS 'philad' database
"""
import sqlalchemy
import pymysql
import pandas as pd

MYSQL_USER = 'george'
MYSQL_PSWD = 'zareason'  # TODO: use KMS to encrypt/decrypt the password
MYSQL_ENDPOINT = 'philad.c2e2iknsgq7e.us-east-1.rds.amazonaws.com'
MYSQL_PORT_I = 3306
MYSQL_PORT_S = str(MYSQL_PORT_I)
MYSQL_DBNAME = 'philad'
DATABASE = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.\
           format(MYSQL_USER, MYSQL_PSWD, MYSQL_ENDPOINT, MYSQL_PORT_S, MYSQL_DBNAME)
SECRET_KEY = '7H9YAl3exX8K^VlC!5E4h$vX5'
USERNAME = 'george'
PASSWORD = 'zareason'

engine = sqlalchemy.create_engine(DATABASE)
conn = engine.connect()
