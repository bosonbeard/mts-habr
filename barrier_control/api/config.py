DB_NAME = 'data.sqlite'
ACCESS_TABLE = 'users_access'
BARIERS_TABLE = 'barriers'
USER_TABLE = 'users'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': './app.log',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'myapp': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False
        },
    }
}


__all__ = ["DB_NAME", "ACCESS_TABLE", "BARIERS_TABLE", "USER_TABLE", "LOGGING"]
