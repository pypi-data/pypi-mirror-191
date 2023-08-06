from x_mock import m_random
from x_mock.test_case.common_utils import execute


class TestBasic:
    def test_basic_character(self):
        print(m_random.m_character.character())
        execute("@character()")
        execute("@character('lower')")
        execute("@character('upper')")
        execute("@character('number')")
        execute("@character('symbol')")
        execute("@character('aeiou')")

    def test_basic_integer(self):
        print(m_random.m_integer.integer())
        execute("@integer(2,4)")
        execute("@integer(3)")
        execute("@integer()")
        execute("@integer(2,2)")

    def test_basic_boolean(self):
        print(m_random.m_boolean.boolean())
        execute("@boolean(2,4)")
        execute("@boolean(3)")
        execute("@boolean()")
        execute("@boolean(2,2)")

    def test_basic_float(self):
        print(m_random.m_float.float())
        execute("@float(2,4)")
        execute("@float(3)")
        execute("@float()")
        execute("@float(2,2)")

    def test_basic_string(self):
        print(m_random.m_string.string())
        print(m_random.m_string.string(7))
        print(m_random.m_string.string(7, 10))
        execute("@string(2)")
        execute('@string("lower", 3)')
        execute('@string("upper", 3)')
        execute('@string("number", 3)')
        execute('@string("symbol", 3)')
        execute('@string("aeiou", 3)')
        execute('@string("lower", 1, 3)')
        execute('@string("upper", 1, 3)')
        execute('@string("number", 1, 3)')
        execute('@string("symbol", 1, 3)')
        execute('@string("aeiou", 1, 3)')
        execute('@string("chinese", 1, 3)')
        execute('@string("cn_symbol", 1, 3)')
        execute('@string("cn_string", 3, 9)')
        execute('@string("cn_string", 1)')
