import pytest
from models import FileContainer, FileReference


@pytest.fixture()
def fc_fr():
    fc = FileContainer(id=1, name='Local', container_type='Local', path='file://c:/dir/')
    fr = FileReference(id=1, name='File', file_size_bytes=12, copyright_url='',
                       file_container=fc, relative_path='FileOne/FileOne.jpg',
                       file_contents_hash='bad_hash', mime_type='image/jpeg',
                       json_metadata='{}')
    return fc, fr


def test_file_reference_full_path(fc_fr):
    fc, fr = fc_fr
    assert fr.full_path == 'file://c:/dir/FileOne/FileOne.jpg'
