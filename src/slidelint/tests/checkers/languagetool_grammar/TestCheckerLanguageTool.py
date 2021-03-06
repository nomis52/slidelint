"""
The languagetool_grammar.pdf file contain slides with grammar issues.

The tests check:
  1. whether help messages are provided
  2. whether languagetool finds grammar issues
"""
import os.path
import unittest
from testfixtures import compare, Replacer, tempdir, ShouldRaise

from slidelint.checkers import language_tool_checker

here = os.path.dirname(os.path.abspath(__file__))


def subprocess_helper(temp_dir, cmd):
    config_file = os.path.join(temp_dir.path, 'tmp_file')
    import subprocess
    origing_popen = subprocess.Popen
    with Replacer() as r:
        def not_existing_program(*args, **kwargs):
            return origing_popen(cmd, *args[1:], **kwargs)
        r.replace('subprocess.Popen', not_existing_program)
        language_tool_checker.start_languagetool_server(
            temp_dir.path, config_file)


class Test_Languagetool_Checker(unittest.TestCase):

    @tempdir()
    def test_languagetool_server_fails(self, temp_dir):
        # Program doesn't exist
        with ShouldRaise(OSError):
            subprocess_helper(
                temp_dir,
                ['not_existing_program', '/tmp'])
        # Program fails to work
        with ShouldRaise(IOError):
            subprocess_helper(temp_dir, ['python', '-c', '5/0'])
        # Program segfaults
        with ShouldRaise(IOError):
            subprocess_helper(
                temp_dir,
                ['python', '-c',
                 'import signal; import sys; sys.exit(signal.SIGSEGV)'])
        # Server started message don't appeared
        with ShouldRaise(IOError):
            subprocess_helper(
                temp_dir,
                ['python', '-c', 'print "Something goes wrong"'])
        subprocess_helper(
            temp_dir,
            ['python', '-c', 'print "Server started"'])

    def test_language_tool_checker(self):
        target_file = os.path.join(
            here, 'languagetool_grammar.pdf')
        rez = language_tool_checker.main(target_file=target_file)
        compare(rez,
                [{'help': 'It would be a honour.',
                  'id': 'C2000',
                  'msg': 'misspelling - Use \'an\' instead of \'a\' if '
                         'the following word starts with a vowel sound,'
                         ' e.g. \'an article\', \'an hour\'',
                  'msg_name': 'EN_A_VS_AN',
                  'page': 'Slide 1'},
                 {'help': 'It would be a honour.',
                  'id': 'C2005',
                  'msg': 'misspelling - Possible spelling mistake found',
                  'msg_name': 'MORFOLOGIK_RULE_EN_US',
                  'page': 'Slide 1'},
                 {'help': 'It was only shown on ITV and '
                          'not B.B.C.',
                  'id': 'C2005',
                  'msg': 'misspelling - Possible spelling mistake found',
                  'msg_name': 'MORFOLOGIK_RULE_EN_US',
                  'page': 'Slide 1'},
                 {'help': '... they\'re coats in the cloakroom. '
                          'I know alot about precious stones. Have '
                          'you seen th...',
                  'id': 'C2005',
                  'msg': 'misspelling - Possible spelling mistake found',
                  'msg_name': 'MORFOLOGIK_RULE_EN_US',
                  'page': 'Slide 3'}])

    def test_checker_helpers(self):
        compare(language_tool_checker.main(msg_info='All'),
                [{'help': 'Language tool found error',
                  'id': 'C2000',
                  'msg': 'Language tool found error',
                  'msg_name': 'language-tool',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2001',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'COMMA_PARENTHESIS_WHITESPACE',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2002',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'UPPERCASE_SENTENCE_START',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2003',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'WHITESPACE_PUNCTUATION',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2004',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'WHITESPACE_RULE',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2005',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'MORFOLOGIK_RULE_EN_US',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2006',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'BRITISH_SIMPLE_REPLACE_RULE',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2007',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'MORFOLOGIK_RULE_EN_AU',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2008',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'MORFOLOGIK_RULE_EN_CA',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2009',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'MORFOLOGIK_RULE_EN_NZ',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2010',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'A_WAS',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2011',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'CONFUSION_OF_OUR_OUT',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2012',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'YOUR_SHOULD',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2013',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'THE_SOME_DAY',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2014',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'MAKE_US_OF',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2015',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'ON_OF_THE',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2016',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'ASK_WETHER',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2017',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'UP_TO_DATA',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2018',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'FEEL_TREE_TO',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2019',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'EASIEST_WAS_TO',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2020',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'ARE_STILL_THE_SOME',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2021',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'IS_EVEN_WORST',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2022',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'DE_JURO',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2023',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'MASSAGE_MESSAGE',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2024',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'I_THIN',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2025',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'SUPPOSE_TO',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2026',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'ALL_BE_IT',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2027',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'ALL_FOR_NOT',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2028',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'ALL_OVER_THE_WORD',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2029',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'ANOTHER_WORDS',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2030',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'BACK_AND_FOURTH',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2031',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'BACK_IN_FORTH',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2032',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'BOB_WIRE',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2033',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'BYE_THE_WAY',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2034',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'CHALK_FULL',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2035',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'EGG_YOKE',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2036',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'ET_ALL',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2037',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'EYE_BROW',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2038',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'FOR_SELL',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2039',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'THERE_EXITS',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2040',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'HE_THE',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2041',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'INSURE_THAT',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2042',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'IN_MASSE',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2043',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'IN_PARENTHESIS',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2044',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'IN_STEAD_OF',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2045',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'IN_TACT',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2046',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'IN_VEIN',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2047',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'IT_SELF',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2048',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'VE_GO_TO',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2049',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'FOR_ALONG_TIME',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2050',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'FOR_ALL_INTENSIVE_PURPOSES',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2051',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'AWAY_FRO',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2052',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'ONE_IN_THE_SAME',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2053',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'PER_SE',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2054',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'SNEAK_PEAK',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2055',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'SOME_WHAT_JJ',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2056',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'STAND_ALONE_NN',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2057',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'TEEM_TEAM',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2058',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'UNDER_WEAR',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2059',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'WHERE_AS',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2060',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'WITCH_HAUNT',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2061',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'YOUR_S',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2062',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'YOURS_APOSTROPHE',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2063',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'HEAR_HERE',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2064',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'TOT_HE',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2065',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'WITH_OUT',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2066',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'ALLOT_OF',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2067',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'I_HERD',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2068',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'ADVICE_ADVISE',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2069',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'ALL_MOST',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2070',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'ANALYSIS_IF',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2071',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'BED_ENGLISH',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2072',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'PIGEON_ENGLISH',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2073',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'TELEPHONE_POLL',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2074',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'OPINION_POLE',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2075',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'BOTTLE_NECK',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2076',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'FIRE_ARM',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2077',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'NEWS_PAPER',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2078',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'AN_OTHER',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2079',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'IN_THE_PASSED',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2080',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'SENT_START_THEM',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2081',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'TOO_TO',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2082',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'THINK_YOU_A',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2083',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'IS_WERE',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2084',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'ONE_ORE',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2085',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'THE_ONLY_ON',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2086',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'THEIR_IS',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2087',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'I_A',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2088',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'I_NEW',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2089',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'PLEASE_NOT_THAT',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2090',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'NUT_NOT',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2091',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'AND_SO_ONE',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2092',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'THROUGH_AWAY',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2093',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'OR_WAY_IT',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2094',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'DT_RESPONDS',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2095',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'THINK_OFF',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2096',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'YOU_THING',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2097',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'VBZ_VBD',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2098',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'FORE_DPS',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2099',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'LESS_MORE_THEN',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2100',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'COMMA_THAN',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2101',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'FROM_THAN_ON',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2102',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'AND_THAN',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2103',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'THAN_INTERJ',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2104',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'WHO_THAN',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2105',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'OF_CAUSE',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2106',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'LOOK_ATE',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2107',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'A_KNOW_BUG',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2108',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'MY_BE',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2109',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'IS_SHOULD',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2110',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'THE_FLEW',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2111',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'CAN_NOT',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2112',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'CAN_BEEN',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2113',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'CANT',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2114',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'TURNED_OFF',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2115',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'FEMALE_ACTOR',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2116',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'FEMALE_WAITER',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2117',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'FIRST_WOMAN_NOUN',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2118',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'FIRST_MAN_NOUN',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2119',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'LITTLE_BIT',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2120',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'MANGER_MANAGER',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2121',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'HAD_OF',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2122',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'ONES',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2123',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'SPARKING_WINE',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2124',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'VERY_MATCH',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2125',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'VARY_MUCH',
                  'page': ''},
                 {'help': 'http://wiki.languagetool.org/',
                  'id': 'C2126',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'ZERO-SUM_GAIN',
                  'page': ''}])
        compare(language_tool_checker.main(msg_info=['C2112']),
                [{'help': 'http://wiki.languagetool.org/',
                  'id': 'C2112',
                  'msg': 'http://wiki.languagetool.org/',
                  'msg_name': 'CAN_BEEN',
                  'page': ''}])
        compare(language_tool_checker.main(msg_info=['W8001']),
                [])

if __name__ == '__main__':
    unittest.main()
