import os
import sys
import pytest
import requests
from pprint import pprint

@pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.integration
def test_fetch_bootstrap_ads():
    print('============================', sys._getframe().f_code.co_name, '============================ ')
    from loader.loader_platsannonser import fetch_bootstrap_ads

    bootstrap_ads = fetch_bootstrap_ads()
    assert len(bootstrap_ads) > 0

@pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.integration
def test_is_ad_included():
    print('============================', sys._getframe().f_code.co_name, '============================ ')
    from loader.loader_platsannonser import is_ad_included

    last_ts = 123456789
    ad_item1_nok = { 'annonsId': 1,'uppdateradTid': last_ts}
    ad_item2_nok = { 'annonsId': 2,'uppdateradTid': last_ts}
    ad_item3_nok = { 'annonsId': 3,'uppdateradTid': last_ts}

    exclude_ids = ['1','2','3']

    ad_item1_ok = { 'annonsId': 1,'uppdateradTid': 123456790}
    ad_item4_ok = { 'annonsId': 4,'uppdateradTid': 123456800}

    assert not is_ad_included(ad_item1_nok, last_ts, exclude_ids)
    assert not is_ad_included(ad_item2_nok, last_ts, exclude_ids)
    assert not is_ad_included(ad_item3_nok, last_ts, exclude_ids)

    assert is_ad_included(ad_item1_ok, last_ts, exclude_ids)
    assert is_ad_included(ad_item4_ok, last_ts, exclude_ids)



@pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.integration
def test_fetch_updated_platsannonser():
    print('============================', sys._getframe().f_code.co_name, '============================ ')
    from loader import settings
    from loader.postgresql import convert_to_timestamp
    from loader.loader_platsannonser import fetch_updated_ads
    nextdate_millis = convert_to_timestamp('2019-02-28')

    # load(settings.LA_FEED_URL, settings.LA_DETAILS_URL, nextdate_millis, None)
    # start_platsannonser()
    updated_ads = fetch_updated_ads(settings.LA_FEED_URL, nextdate_millis)
    # print(len(updated_ads))

    assert len(updated_ads) > 0
    # print(updated_ads[0]['uppdateradTid'], nextdate_millis)
    assert updated_ads[0]['uppdateradTid'] >= nextdate_millis

@pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.integration
def test_fetch_platsannons_detail():
    print('============================', sys._getframe().f_code.co_name, '============================ ')
    from loader import settings
    from loader.loader_platsannonser import fetch_ad_details
    ad_id = 20157672
    ts = 1553499161598

    result_ad = fetch_ad_details(ad_id, ts, settings.LA_DETAILS_URL)
    print(result_ad)

    assert result_ad['annonsId'] == ad_id
    assert result_ad['annonsrubrik'].startswith('RegTest FM Annonsstatus')
    assert result_ad['updatedAt'] == ts

@pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.integration
def test_fetch_missing_platsannons_detail():
    print('============================', sys._getframe().f_code.co_name, '============================ ')
    from loader import settings
    from loader.loader_platsannonser import fetch_ad_details
    # missing_ad_id = 20154399
    missing_ad_id = 12345678
    ts = 1553499161598

    with pytest.raises(requests.exceptions.RequestException):
        fetch_ad_details(missing_ad_id, ts, settings.LA_DETAILS_URL)




@pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.integration
def test_start_platsannonser():
    print('============================', sys._getframe().f_code.co_name, '============================ ')
    from loader.main import start_platsannonser
    start_platsannonser()




if __name__ == '__main__':
    pytest.main([os.path.realpath(__file__), '-svv', '-ra', '-m integration'])