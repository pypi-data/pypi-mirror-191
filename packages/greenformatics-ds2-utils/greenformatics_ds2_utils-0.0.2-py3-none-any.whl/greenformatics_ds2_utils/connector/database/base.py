# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from greenformatics_ds2_utils import Singleton


Base = declarative_base()


class SingleSession(metaclass=Singleton):
    """ This singleton class ensures that one database session is active one time during the program run. """

    def __init__(self, url):
        # Create a new connection pool
        db_engine = create_engine(url,
                                  pool_size=100, # Set connection pool size
                                  max_overflow=0,
                                  pool_pre_ping=True,
                                  connect_args={
                                      "keepalives": 1,
                                      "keepalives_idle": 60,
                                      "keepalives_interval": 5,
                                      "keepalives_count": 5
                                  })
        # Create a new session
        self._target_session = sessionmaker(bind=db_engine, autoflush=False, expire_on_commit=False)
        self._session = self._target_session()

    def get_session(self):
        return self._session

    def close(self):
        # Close existing session..
        self._session.close()
        # And create a new one for the singleton class
        self._session = self._target_session()

    def shutdown(self):
        # Close existing session..
        self._session.close()
