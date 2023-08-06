import re
import unittest

from uhslc_station_tools.extractor import extract_rate


class TestExtractor(unittest.TestCase):

    def test_extracting_sensor_frequencies(self):
        """
        Sensor frequency or sensor rate is the sampling rate of the sensor.
        This information is stored in the header of the data file for each sensor. It is
        not consistently stored in the same place in the header. We are making sure the function
        can handle header extraction properly for all cases
        """

        hourly_header  = "181DurHOU     LAT=29 53.8S LONG=031 00. E TMZONE=GMT    REF=00000 60 NOV 22 M 30"
        regular_header = "105RodPRD    PLAT=19 40  S LONG=063 25  E TMZONE=GMT    REF=1810 15 FEB 22   28 "
        re_rate_hourly = extract_rate(hourly_header)
        re_rate_regular = extract_rate(regular_header)

        self.assertEqual(re_rate_hourly, '60')
        self.assertEqual(re_rate_regular, '15')


if __name__ == '__main__':
    unittest.main()
