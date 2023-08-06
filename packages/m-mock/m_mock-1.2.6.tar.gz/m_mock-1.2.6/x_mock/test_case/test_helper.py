from x_mock import m_random
from x_mock.test_case.common_utils import execute


class TestHelper:
    def test_helper(self):
        m_random.m_helper.pick('(1,2,3)')
        execute("""@pick('("1",2,"3")')""")
