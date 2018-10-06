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
    __table_name__ = 'copyright_status'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    is_usable = Column(Boolean, nullable=False)
    requires_attribution = Column(Boolean, nullable=False)


class FileContainer(Base):
    """
    Points to system and root folder for file references
    """
    __table_name__ = 'file_container'

    id = Column(Integer, primary_key=False)
    name = Column(String)
    container_type = Column(String)
    path = Column(String)


class FileReference(Base):
    """

    """
    __table_name__ = 'file_reference'

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
    __table_name__ = 'test_suite'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


class TestSuiteEntry(Base):
    __table_name__ = 'test_run'

    id = Column(Integer, primary_key=True)
    test_suite_id = ForeignKey('test_suite.id')
    test_case_job_hash = Column(String(16))
    test_case_item_id = Column(Integer)


class TestCaseVersion(Base):
    __table_name__ = 'test_case_version'

    id = Column(Integer, primary_key=True)

    # This does not change with versioning of test case
    item_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    created = Column(DateTime, default=datetime.utcnow)

    job = Column(JSON)

    # Programmatically generate this with data.
    job_hash = Column(String(16), nullable=False)


class Application(Base):
    __table_name__ = 'application'

    id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)


class InvocationTargetVersion(Base):
    __table_name__ = 'invocation_target'

    id = Column(Integer, primary_key=True)
    hash = Column(String(16))
    application_id = ForeignKey('application.id')
    translator_function = Column(String)
    invocation_command = Column(String)
    docker_tag = Column(String)
    docker_registry = Column(String)
    version_description = Column(String)
    version = Column(Integer, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)


class CachedResult(Base):
    __table_name__ = 'cached_result'

    id = Column(Integer, primary_key=True)
    task_hash = Column(String(16))
    file_id = ForeignKey('file_reference.id')
    invocation_target_id = ForeignKey('invocation_target.id')
    item_job_id = ForeignKey('test_case_version.job_id')
