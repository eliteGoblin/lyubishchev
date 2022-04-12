# import unittest
# from dataclasses import dataclass
# import logging
#
#
# class TestValidation(unittest.TestCase):
#     def test_start_end(self):
#         @dataclass
#         class TestCase:
#             desc: str
#             startDate: str
#             endDate: str
#             error: bool
#             startUnixSec: int = 0
#             endUnixSec: int = 0
#
#         testcases = [
#             TestCase(desc="empty input", startDate=None, endDate=None, error=True, ),
#             TestCase(desc="start date after end date", startDate='12-1', endDate='9-23', error=True, ),
#             TestCase(desc="valid start and end", startDate='09-23', endDate='12-1', error=False, ),
#         ]
#
#         for case in testcases:
#             try:
#                 startUnixSec, endUnixSec = timeRangeFromStartEnd(case.startDate, case.endDate)
#             except Exception as e:
#                 logging.error(e)
#                 self.assertTrue(case.error)
#             else:
#                 self.assertFalse(case.error)
#                 self.assertEqual(startUnixSec, case.startUnixSec)
#                 self.assertEqual(endUnixSec, case.endUnixSec)