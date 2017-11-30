"""
The Philadelphia-Reflections website

> rewritten in Python Flask
> to run as an AWS Lambda function
> connecting to an RDS MySql database
> with images on S3
> distributed using the Zappa package
"""
from flask import Flask
app = Flask(__name__)

from .version import __version__

import philad_lambda.philad_lambda
