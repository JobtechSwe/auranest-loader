import os
import sys
import pytest

@pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.integration
def test_postgres__convert_to_timestamp():
    print('============================', sys._getframe().f_code.co_name, '============================ ')
    from datetime import datetime
    from loader.postgresql import convert_to_timestamp
    expires_at = '2019-03-25 23:59:58'
    timestamp = convert_to_timestamp(expires_at)
    print(timestamp)
    dt = datetime.fromtimestamp(int(timestamp/1000))

    assert dt.year == 2019
    assert dt.month == 3
    assert dt.day == 25
    assert dt.hour == 23
    assert dt.minute == 59
    assert dt.second == 58


@pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.integration
def test_str_to_date_time():
    print('============================', sys._getframe().f_code.co_name, '============================ ')
    from loader.postgresql import convert_to_timestamp
    from datetime import datetime
    millis = convert_to_timestamp('2019-02-03')
    # print(millis)
    dt = datetime.fromtimestamp(int(millis/1000))
    print('dt: %s' % dt)

    assert dt.year == 2019
    assert dt.month == 2
    assert dt.day == 3

@pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.integration
def test_unix_time_millis():
    from loader.postgresql import convert_to_timestamp
    millis = convert_to_timestamp('2019-02-28')
    assert millis == 1551308400000

if __name__ == '__main__':
    pytest.main([os.path.realpath(__file__), '-svv', '-ra', '-m integration'])