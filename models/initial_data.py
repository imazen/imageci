#
# This hold data to populate the db with start data.
#
# Root object is a dictionary with the key being the ORM object name.
# The value is a list of dictionaries with each representing a row.
#
# The extra work at keeping key/name pairs will allow nullable fields to be
# added with no extra work at input and helps self describe.
#
# In a situation where a parent child relationship is represented in the data,
# a special record dictionary field 'kw_objects' is used to allow creating the
# child object with a reference to the parent.
#
# 'parent_field_name' is the name that you assign the parent object to in the child object creations.
# 'object_class_name' is the class name to be created for the child object.
# 'objects': is a list of dictionaries for the child, the same as the root dictionaries in format.
#
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
         'name': 'Initial Test',
         'kw_objects': {
             'parent_field_name': 'test_suite',
             'object_class_name': 'TestCaseVersion',
             'objects': [
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
            }
         }
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
