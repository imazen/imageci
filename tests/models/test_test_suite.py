from models import (
    TestSuite,
    TestCaseVersion,
)


def test_relationships():
    ts = TestSuite(id=1, name='TS1')
    tcv1 = TestCaseVersion(id=1, item_id=100, title='Item 100', job_hash='ABCD', job='{}', test_suite=[ts])
    tcv2 = TestCaseVersion(id=2, item_id=101, title='Item 101', job_hash='ABCD', job='{}', test_suite=[ts])
    assert ts.test_cases[0] is tcv1
    assert ts.test_cases[1] is tcv2
