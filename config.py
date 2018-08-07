import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Secret key for session management. You can generate random strings here:
# https://randomkeygen.com/
SECRET_KEY = 'my precious'

# AWS config
S3_BUCKET                 = os.environ.get("S3_BUCKET_NAME")
S3_KEY                    = os.environ.get("S3_ACCESS_KEY")
S3_SECRET                 = os.environ.get("S3_SECRET_ACCESS_KEY")
S3_LOCATION               = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

SECRET_KEY                = os.urandom(32)
DEBUG                     = True
