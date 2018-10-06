import models
from models import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# This is slightly different to allow sharing objects both in normal apps
# and Flask apps.  We are not using flask-sqlalchemy for this reason.
engine_uri = models.get_engine_uri('development')
engine = create_engine(engine_uri)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    Base.metadata.create_all(bind=engine)
