from datetime import datetime
import urllib
from .initial_data import INITIAL_DATA

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
    ForeignKeyConstraint,
    UniqueConstraint,
    Table,
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
    created = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<CopyrightLicense(id={self.id}, name='{self.name}', is_usable={self.is_usable})>"


class FileContainer(Base):
    """
    Points to system and root folder for file references
    """
    __tablename__ = 'file_container'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    container_type = Column(String)
    path = Column(String)
    read_through_cache_container_id = Column(Integer, nullable=True)
    file_references = relationship('FileReference', back_populates='file_container')
    created = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<FileContainer(id={self.id}, name='{self.name}', path='{self.path}', " \
               f"container_type='{self.container_type}'>"


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
    file_container_id = Column(Integer, ForeignKey('file_container.id'))
    file_container = relationship('FileContainer', back_populates='file_references')
    relative_path = Column(String, nullable=False)
    file_contents_hash = Column(String(16), nullable=False)
    mime_type = Column(String(255), nullable=False)
    json_metadata = Column(String)  # Might want JSON in Postgres, not supported in SQLite
    created = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<FileReference(id={self.id}, name='{self.name}', file_container_id={self.file_container_id}," \
               f"relative_path='{self.relative_path}, file_contents_hash='{self.file_contents_hash}, " \
               f"mime_type={self.mime_type}'>"

    @property
    def full_path(self):
        return urllib.parse.urljoin(self.file_container.path, self.relative_path)


test_suite_entry = Table(
    'test_suite_entry',
    Base.metadata,
    Column('test_suite_id', Integer, ForeignKey('test_suite.id'), primary_key=True),
    Column('test_case_job_hash', String(16), primary_key=True),
    Column('test_case_item_id', Integer, primary_key=True),
    ForeignKeyConstraint(('test_case_job_hash', 'test_case_item_id'),
                         ('test_case_version.job_hash', 'test_case_version.item_id'))
)


class TestSuite(Base):
    """
    This defines a complete test run.
    """
    __tablename__ = 'test_suite'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    test_cases = relationship('TestCaseVersion', secondary='test_suite_entry')

    def __repr__(self):
        return f"<TestSuite(id={self.id}, name='{self.name}>"


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
    job_hash = Column(String(16), nullable=False)
    job = Column(String)  # Might want JSON in Postgres, not supported in SQLite
    created = Column(DateTime, default=datetime.utcnow)
    test_suite = relationship('TestSuite', back_populates='test_cases',
                              secondary='test_suite_entry')

    UniqueConstraint('item_id', 'job_hash')

    def __repr__(self):
        return f"<TestCaseVersion(id={self.id}, item_id={self.item_id}, " \
               f"title='{self.title}', job_hash='{self.job_hash}'>"


class TestCaseRun(Base):
    __tablename__ = 'test_case_run'

    id = Column(Integer, primary_key=True)
    test_suite_id = Column(Integer, ForeignKey='test_suite.id')
    test_case_version_id = Column(Integer, ForeignKey='test_case_version.id')
    invocation_target_id = Column(Integer, nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(Integer)


class Application(Base):
    """
    Application for use in a test case job.  This gives a group for InvocationTargetVersions
    """
    __tablename__ = 'application'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    invocation_targets = relationship('InvocationTargetVersion', back_populates='application')

    def __repr__(self):
        return f"<Application(id={self.id}, name='{self.name}'>"


class InvocationTargetVersion(Base):
    """
    Unique version of process to run in a docker build.  Called as part of a TestCaseVersion job.
    """
    __tablename__ = 'invocation_target'

    id = Column(Integer, primary_key=True)
    hash = Column(String(16))
    application_id = Column(Integer, ForeignKey('application.id'))
    application = relationship('Application')
    translator_function = Column(String)
    invocation_command = Column(String)
    docker_repo = Column(String)
    dockerfile = Column(String)
    git_repo = Column(String)   #requires .git suffix
    commit = Column(String)
    # commit is used for docker_tag unless explicitly overridden.
    # When we build, commit will be the docker tag.
    override_docker_tag = Column(String, nullable=True)
    cached_result = relationship('CachedResult')
    version_description = Column(String)
    version = Column(Integer, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<InvocationTargetVersion(id={self.id}, hash='{self.hash}, application_id={self.application_id}>"


class CachedResult(Base):
    """
    Results created from a job process.

    task_hash: Provides a unique hash of what was used to create this result.  Used for not executing
    previously computed result files.

    invocation_target_id and item_job_id: are used to allow clean up of cached results if a test case or
    application version is not longer part of the test suite.
    """
    __tablename__ = 'cached_result'

    task_hash = Column(String(16), primary_key=True)
    file_id = ForeignKey('file_reference.id')
    invocation_target_id = Column(Integer, ForeignKey('invocation_target.id'))
    item_job_id = Column(Integer, ForeignKey('test_case_version.id'))
    item_job = relationship('InvocationTargetVersion', back_populates='cached_result')
    created = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<CachedResult(id={self.id}, task_hash='{self.task_hash}, file_id={self.file_id}, " \
               f"invocation_target_id={self.invocation_target_id}, item_job_id={self.item_job_id}>"


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


def populate_database(session):
    for class_name, records in INITIAL_DATA.items():
        if not records:
            continue
        inserts = []
        class_obj = globals()[class_name]
        for record_fields in records:
            inserts.append(class_obj(**record_fields))
        session.bulk_save_objects(inserts)
        session.commit()


def initialize_database():
    global engine
    global Session
    Base.metadata.create_all(engine)
    session = Session()
    populate_database(session)
