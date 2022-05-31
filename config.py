import os


class Config(object):
    RATELIMIT_HEADERS_ENABLED = True
    RATELIMIT_STORAGE_URL = os.environ.get("REDIS_URL") or "memory://"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "ELHa$YW3rK@Weu9qJaa4b*ryz3Uek%zM"
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL").replace("postgres://", "postgresql://")
        if os.environ.get("DATABASE_URL")
        else "postgresql://mash:mash@localhost:5433/thing"
    )
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_size": 20}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
