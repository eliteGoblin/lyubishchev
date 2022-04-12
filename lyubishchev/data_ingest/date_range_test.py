import unittest
from dataclasses import dataclass
import logging

from data_ingest import timeRangeFromStartEnd, timeRangeFromWeek, timeRangeFromOffsetDays


class TestRange(unittest.TestCase):
    def test_start_end(self):
        @dataclass
        class TestCase:
            desc: str
            startDate: str
            endDate: str
            error: bool
            startUnixSec: int = 0
            endUnixSec: int = 0

        """
        # week 00 按date来算
        AEST FRI 2021-01-01 SUN 2021-01-03
        # week 01
        AEST SUN 01-03 SUN 01-10
        # week 23 按date来算; week 22 按datetime来算
        # AEST SUN 2021-05-30:00:00:00 1622296800 2021-05-29T14:00:00Z
        # AEST SUN 2021-06-06:00:00:00 1622901600 2021-06-05T14:00:00Z
        """
        # 自己的datetime模块支持, 转换; week number, 转date range.
        testcases = [
            TestCase(desc="empty input", startDate=None, endDate=None, error=True,),
            TestCase(desc="start date after end date", startDate='12-1', endDate='9-23', error=True,),
            TestCase(desc="valid start and end", startDate='09-23', endDate='12-1', error=False,),
        ]

        for case in testcases:
            try:
                startUnixSec, endUnixSec = timeRangeFromStartEnd(case.startDate, case.endDate)
            except Exception as e:
                logging.error(e)
                self.assertTrue(case.error)
            else:
                self.assertFalse(case.error)
                self.assertEqual(startUnixSec, case.startUnixSec)
                self.assertEqual(endUnixSec, case.endUnixSec)
        

    def test_week_number(self):
        """
        期望输入:  与linux date +'%U' 一致
        2021-23, 返回AEST: SUN 2021-5-30T00:00 - SUN 2021-6-6T00:00
        """
        ...


if __name__ == '__main__':
    unittest.main()
