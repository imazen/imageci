import models


def test_db_creation_and_init():
    models.init_engine('development')
    models.initialize_database()


