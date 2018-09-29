from datetime import datetime

from sqlalchemy import (
    Boolean,
    create_engine,
    Column,
    DateTime,
    Integer,
    String,
    ForeignKey,
    func,
    types,
    JSON,
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    sessionmaker,
    relationship,
)

Base = declarative_base()
engine = None
Session = None


# TODO: Add to FileReference instead of text based copyright.
class CopyrightLicense(Base):
    """
    USed to map "closest license" for a given copyright to programatically
    determine usability and requirements
    """
    __tablename__ = 'copyright_license'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    is_usable = Column(Boolean, nullable=False)
    requires_attribution = Column(Boolean, nullable=False)


class FileContainer(Base):
    """
    Points to system and root folder for file references
    """
    __tablename__ = 'file_container'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    container_type = Column(String)
    path = Column(String)


class FileReference(Base):
    """
    Represents a file in storage.  This is used for source files for testing and will
    be created for generated files as results of testing steps.
    """
    __tablename__ = 'file_reference'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    copyright_url = Column(String(2048))
    copyright_status_string = Column(String(255), nullable=False)
    file_container = ForeignKey('file_container.id')
    relative_path = Column(String, nullable=False)
    file_contents_hash = Column(String(16), nullable=False)
    mime_type = Column(String(255), nullable=False)
    json_metadata = Column(JSON)
    created = Column(DateTime, default=datetime.utcnow)


class TestSuite(Base):
    """
    This defines a complete test run.
    """
    __tablename__ = 'test_suite'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


class TestSuiteEntry(Base):
    """
    xref table to join test
    """
    __tablename__ = 'test_run'

    id = Column(Integer, primary_key=True)
    test_suite_id = ForeignKey('test_suite.id')
    test_case_job_hash = Column(String(16))
    test_case_item_id = Column(Integer)


class TestCaseVersion(Base):
    """
    Holds a full test case.  This may include multiple processes to generate resulting files and multiple
    comparison actions.  The job field defines all custom operations, including expected results.

    item_id: a representation of the test case operation.  It does not change for a new record that modifies
    the operational parameters, as it is still the same test case.

    job_hash: hashes the relevant fields that impact test case uniqueness

    job: This will be a complex JSON structure that will define source files, invocation targets, result files,
    comparisons and results evaluation.  This is tightly coupled to the code that will be executed in the runner.
    """
    __tablename__ = 'test_case_version'

    id = Column(Integer, primary_key=True)

    # This does not change with versioning of test case
    item_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    created = Column(DateTime, default=datetime.utcnow)
    job_hash = Column(String(16), nullable=False)
    job = Column(JSON)


class Application(Base):
    """
    Application for use in a test case job.  This gives a group for InvocationTargetVersions
    """
    __tablename__ = 'application'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class InvocationTargetVersion(Base):
    """
    Unique version of process to run in a docker build.  Called as part of a TestCaseVersion job.
    """
    __tablename__ = 'invocation_target'

    id = Column(Integer, primary_key=True)
    hash = Column(String(16))
    application_id = ForeignKey('application.id')
    translator_function = Column(String)
    invocation_command = Column(String)
    docker_repo = Column(String)
    dockerfile = Column(String)
    git_repo = Column(String)   #requires .git suffix
    commit = Column(String)
    # commit is used for docker_tag unless explicitly overridden.
    # When we build, commit will be the docker tag.
    override_docker_tag = Column(String, nullable=True)
    version_description = Column(String)
    version = Column(Integer, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)


class CachedResult(Base):
    """
    Results created from a job process.

    task_hash: Provides a unique hash of what was used to create this result.  Used for not executing
    previously computed result files.

    invocation_target_id and item_job_id: are used to allow clean up of cached results if a test case or
    application version is not longer part of the test suite.
    """
    __tablename__ = 'cached_result'

    id = Column(Integer, primary_key=True)
    task_hash = Column(String(16))
    file_id = ForeignKey('file_reference.id')
    invocation_target_id = ForeignKey('invocation_target.id')
    item_job_id = ForeignKey('test_case_version.job_id')


def get_engine_uri(engine_name):
    return 'sqlite://'


def init_engine(engine_name):
    global engine
    global Session

    uri = get_engine_uri(engine_name)
    engine = create_engine(uri)
    Session = sessionmaker(bind=engine)


def clean_database():
    global engine
    global Session
    Base.metadata.drop_all(engine)


def initialize_database():
    global engine
    global Session
    Base.metadata.create_all(engine)