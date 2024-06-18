import os
import logging
from logging.config import dictConfig

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}

dictConfig(logging_config)

logger = logging.getLogger(__name__)

API_URL = os.getenv('API_URL', 'http://narrative-api:3000')
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
