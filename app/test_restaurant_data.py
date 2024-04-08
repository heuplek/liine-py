import unittest
import dataParse

class TestRestaurantDataParsing(unittest.TestCase):

    def test_mapHours(self):
        # Test cases for mapHours single day
        print("Testing mapHours single day")
        self.assertEqual(dataParse.mapHours("Mon 11:00 am - 10 pm"), [{'open_ts': 11100, 'close_ts': 12200}])
        print("Testing mapHours day range")
        # Test cases for mapHours day range
        self.assertEqual(dataParse.mapHours("Mon-Tue 11:00 am - 10 pm"), [{'open_ts': 11100, 'close_ts': 12200}, {'open_ts': 21100, 'close_ts': 22200}])


    def test_to24(self):
        print("Testing to24")
        self.assertEqual(dataParse.to24("10:00 am"), "1000")
        self.assertEqual(dataParse.to24("10:00 pm"), "2200")
        self.assertEqual(dataParse.to24("1 am"), "0100")
        self.assertEqual(dataParse.to24("12 pm"), "1200")
        self.assertEqual(dataParse.to24("12:30 am"), "0030")

    def test_normalize_hours(self):
        print("Testing normalize_hours")
        self.assertEqual(dataParse.normalize_hours("10:00"), "1000")
        self.assertEqual(dataParse.normalize_hours("1"), "0100")
        self.assertEqual(dataParse.normalize_hours("12"), "1200")
        self.assertEqual(dataParse.normalize_hours("12:30"), "1230")

    def test_handle_close_after_midnight(self):
        print("Testing handle_close_after_midnight")
        self.assertEqual(dataParse.handle_close_after_midnight("1230", "0130", 1), [{'open_ts': 20000, 'close_ts': 21230}])

    def test_full_parse(self):
        print("Testing full_parse")
        test_data = dataParse.parseData("test.csv")
        self.assertIn({'open_ts': 11100, 'close_ts': 12200, 'restaurant': 'Test'}, test_data)
        self.assertIn({'open_ts': 21100, 'close_ts': 22200, 'restaurant': 'Test'}, test_data)
        self.assertIn({'open_ts': 41700, 'close_ts': 42400, 'restaurant': 'Test 2'}, test_data)
        self.assertIn({'open_ts': 50000, 'close_ts': 50130, 'restaurant': 'Test 2'}, test_data)
        self.assertIn({'open_ts': 51700, 'close_ts': 52400, 'restaurant': 'Test 2'}, test_data)
        self.assertIn({'open_ts': 60000, 'close_ts': 60130, 'restaurant': 'Test 2'}, test_data)
        self.assertIn({'open_ts': 61500, 'close_ts': 62400, 'restaurant': 'Test 2'}, test_data)
        self.assertIn({'open_ts': 70000, 'close_ts': 70130, 'restaurant': 'Test 2'}, test_data)
        self.assertIn({'open_ts': 71500, 'close_ts': 72330, 'restaurant': 'Test 2'}, test_data)
        self.assertEqual(len(test_data), 9)

if __name__ == '__main__':
    unittest.main()