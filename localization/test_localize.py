import unittest
from localize import get_equivalent_locale, use_localize


class LocalizationTest(unittest.TestCase):
    def test_equivalent_locale(self):
        cases = [
            ["zh", "zh-Hans"],
            ["zh_CN", "zh-Hans"],
            ["zh_TW", "zh-Hant"],
            ["zh_HK", "zh-Hans"],
            ["zh_MO", "zh-Hans"],
            ["zh-CN", "zh-Hans"],
            ["zh-TW", "zh-Hant"],
            ["zh-HK", "zh-Hans"],
            ["zh-MO", "zh-Hans"],
            ["zh-Hans", "zh-Hans"],
            ["zh_Hans", "zh-Hans"],
            ["zh-Hant", "zh-Hant"],
            ["zh_Hant", "zh-Hant"],
            ["zh-Hans-CN", "zh-Hans"],
            ["zh-Hans-HK", "zh-Hans"],
            ["zh-Hans-TW", "zh-Hans"],
            ["zh-Hant-TW", "zh-Hant"],
            ["zh-Hans_CN", "zh-Hans"],
            ["zh-Hans_HK", "zh-Hans"],
            ["zh-Hans_TW", "zh-Hans"],
            ["zh-Hant_TW", "zh-Hant"],
            ["zh-Hant_CN", "zh-Hant"],
        ]
        for case in cases:
            self.assertEqual(get_equivalent_locale(case[0]), case[1])

    def test_localize(self):
        key = "Error.ConnectionTimedOut.Title"
        cases = [
            [None, "Connection Timed Out"],
            ["", "Connection Timed Out"],
            ["fr", "Connection Timed Out"],
            ["en", "Connection Timed Out"],
            ["en_US", "Connection Timed Out"],
            ["en_UK", "Connection Timed Out"],
            ["zh-Hans", "连接超时"],
            ["zh-Hant", "連接超時"],
            ["zh_CN", "连接超时"],
            ["zh_TW", "連接超時"],
            ["ja", "接続がタイムアウトしました"],
            ["ja_JP", "接続がタイムアウトしました"],
        ]
        for case in cases:
            self.assertEqual(use_localize(case[0])(key), case[1])


if __name__ == '__main__':
    unittest.main()
