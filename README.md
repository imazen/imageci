# imageci

# Booting under docker

This will build the Postgres and Web (nginx/uwsgi/flask) images and boot them together

`docker-compose up -d --build`

Open http://localhost:8080/ to view

#Test runners

All things under test (and all reference apps) must have a docker image or have a git repo and Dockerfile within

#Authentication

We don't want to store passwords or secrets

OAuth 2 - delegate to github like travis does

Anonymous users can upload files and create test cases, but not edit anything

This permission should be configurable, I.e, allow Anonymous (everyone), or any authenticated member, or only those with write access to this repository (I believe this info is sent by OAuth 2 from GitHub)

OAuth 2 


# Database and Initial Data Loading

Data is defined in `models/initial_data.py` in a list of dictionaries.  The key values
are the names of the ORM classes.  The value is a 0 to many list of dictionaries of data.

The `populate_database` method will read this file and load up the session it is given.

## Initializing DB for use

    from models import (
        engine,
        Session,
        init_engine,
        initialize_database,    
    )
    
    # Creates engine and Session objects
    init_engine('development')
    
    # If you need to create db_structure and load intial data
    initialize_database()
    
    # Get ORM session for operation
    session = Session()
    

