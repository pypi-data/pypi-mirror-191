import unittest

from unicode_linebreak import linebreaks

class TestPyUnicodeLinebreak(unittest.TestCase):
    def test_simple(self):
        string = 'a b\nc\r\nd e\rf end'
        expected_result = [
            (2, False), (4, True), (7, True), (9, False),
            (11, True), (13, False), (16, True)
        ]
        self.assertListEqual(linebreaks(string), expected_result)

    def test_scriptio_continua_linebreaks(self):
        string = (
            '支持常见的温度传感器（例如，常见的热敏电阻、'
            'AD595、AD597、AD849x、PT100、PT1000、'
            'MAX6675、MAX31855、MAX31856、MAX31865、'
            'BME280、HTU21D和LM75）。'
            '还可以配置自定义热敏电阻和自定义模拟温度传感器。'
        )
        expected_result = [
            (3, False), (6, False), (9, False), (12, False),
            (15, False), (18, False), (21, False), (24, False),
            (27, False), (30, False), (36, False), (42, False),
            (45, False), (48, False), (51, False), (54, False),
            (57, False), (60, False), (66, False), (74, False),
            (82, False), (91, False), (99, False), (108, False),
            (118, False), (129, False), (140, False), (151, False),
            (160, False), (166, False), (169, False), (179, False),
            (182, False), (185, False), (188, False), (191, False),
            (194, False), (197, False), (200, False), (203, False),
            (206, False), (209, False), (212, False), (215, False),
            (218, False), (221, False), (224, False), (227, False),
            (230, False), (233, False), (236, False), (239, False),
            (242, False), (245, False), (251, True)
        ]

        self.assertListEqual(linebreaks(string), expected_result)
