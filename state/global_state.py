from redis.asyncio import Redis

from adapters.database import Database
from adapters.classifier import Classifier

from utils import settings

database = Database(settings.DB_URL)
classifier = Classifier()

redis = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASS,
    db=settings.REDIS_DB
)
