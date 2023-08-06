from x_mock import m_random
from x_mock.test_case.common_utils import execute


class TestDate:
    def test_date(self):
        execute("@date('%Y-%m-%d %H:%M:%S', '+1d')")
        execute("@date('%Y-%m-%d %H:%M:%S', '+24h')")
        print(m_random.m_date.date('%y-%m-%d', '-20d'))
        print(m_random.m_date.date())

    def test_time(self):
        print(m_random.m_date.time('', '+2sec'))
        print(m_random.m_date.time('', '+4sec'))
        execute("@time('', '+4sec')")
        execute("@time")


