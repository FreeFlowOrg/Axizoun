import boto3, botocore
from config import S3_KEY, S3_SECRET, S3_BUCKET
from flask import session

s3 = boto3.client(
   "s3",
   aws_access_key_id=S3_KEY,
   aws_secret_access_key=S3_SECRET
)

def download_f(filename):
	return redirect('https://s3.amazonaws.com/'+'axizoun-resumes'+'/'+filename)
