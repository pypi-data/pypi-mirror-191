from x_mock.m_random import m_name
from x_mock.test_case.common_utils import execute


class TestName:
    def test_name(self):
        execute("""@clast()""")
        execute("""@cfirst()""")
        execute("""@cname()""")
        execute("""@cname(3)""")
        print(m_name.cfirst())
        print(m_name.clast())
        print(m_name.cname())
