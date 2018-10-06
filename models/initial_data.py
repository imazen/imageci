INITIAL_DATA = {
    'CopyrightLicense': [],
    'FileContainer': [
        {'id': 1,
         'name': 'Local',
         'container_type': '???',
         'path': 'file:/C:/local_data'},
    ],
    'FileReference': [
        {'id': 1,
         'name': 'FileOne',
         'file_size_bytes': 1230,
         'copyright_url': '',
         'copyright_status_string': '',
         'file_container_id': 1,
         'relative_path': 'FileOne/FileOne.jpg',
         'file_contents_hash': 'QAZWSX',
         'mime_type': 'image/jpeg',
         'json_metadata': '{}'},
    ],
    'TestSuite': [
        {'id': 1,
         'name': 'Initial Test'}
    ],
    'TestSuiteEntry': [
        {'id': 1,
         'test_suite_id': 1,
         'test_case_job_hash': 'ABCD',
         'test_case_item_id': 1}
    ],
    'TestCaseVersion': [
        {'id': 1,
         'item_id': 1,
         'title': 'Test item 1',
         'job_hash': 'ABCD',
         'job': '{}'},
        {'id': 2,
         'item_id': 1,
         'title': 'Test item 1',
         'job_hash': 'EFGH',
         'job': '{}'},
    ],
    'Application': [
        {'id': 1,
         'name': 'ImageFlow'},
        {'id': 2,
         'name': 'ImageMagick'},
    ],
    'InvocationTargetVersion': [
        {'id': 1,
         'hash': 'EDCRFV',
         'application_id': 1,
         'translator_function': None,
         'invocation_command': '/bin/true',
         'docker_repo': '',
         'dockerfile': '',
         'git_repo': '??.git',
         'commit': 'GUID',
         'override_docker_tag': None,
         'version_description': 'Initial ImageFlow Invocation Version',
         'version': 1}
    ],
    'CachedResult': [],
}
