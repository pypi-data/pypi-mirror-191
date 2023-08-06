import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# instagram
INSTAGRAM_USERNAME = os.getenv("BYB_INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("BYB_INSTAGRAM_PASSWORD")

# s3 assets

S3_ASSET_URL = os.getenv("BYB_S3_ASSET_URL")
S3_ASSET_BUCKET = os.getenv("BYB_S3_ASSET_BUCKET")
S3_ASSET_PATH = os.getenv("BYB_S3_ASSET_PATH")
S3_ASSET_CLOUDFRONT_DIST = os.getenv("BYB_S3_ASSET_CLOUDFRONT_DIST")
AWS_ACCESS_KEY_ID = os.getenv("BYB_AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("BYB_AWS_SECRET_ACCESS_KEY")
