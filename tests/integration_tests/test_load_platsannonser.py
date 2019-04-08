import os
import sys
import pytest
import requests
import json
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
def test_save_dirty_ad():
    print('============================', sys._getframe().f_code.co_name, '============================ ')
    from loader.main import fetch_details_and_save

    # ad_data['annonsId']
    ad_item1 = { 'annonsId': 23075723,'uppdateradTid': 123456790}
    test_ad_ids = [ad_item1]
    fetch_details_and_save(test_ad_ids)


@pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.integration
def test_clean_dirty_ad():
    print('============================', sys._getframe().f_code.co_name, '============================ ')
    from loader.loader_platsannonser import clean_stringvalues
    dirty_ad = get_dirty_ad()
    # pprint(dirty_ad)

    assert '\\u0000' in json.dumps(dirty_ad)

    clean_ad = clean_stringvalues(dirty_ad)
    # pprint(clean_ad)
    assert '\\u0000' not in json.dumps(clean_ad)




@pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.integration
def test_start_platsannonser():
    print('============================', sys._getframe().f_code.co_name, '============================ ')
    from loader.main import start_platsannonser
    start_platsannonser()


def get_dirty_ad():
    return {'annonsId': 23075723,
          'annonsrubrik': 'Tandläkare sökes till Degerfors',
          'annonstext': 'Vi söker dig som är \x00exibel, tar egna initiativ och har en '
                        'god samarbetsförmåga. Ett stort intresse för att erbjuda '
                        'personlig service är nödvändigt. Din positiva attityd bidrar '
                        'till vår goda stämning på mottagningen. Du tycker att det är '
                        'roligt med service och att medverka i mottagningens '
                        'utvecklingsarbete.\n'
                        'Vi lägger stor vikt vid dina personliga egenskaper och söker '
                        'särskilt efter dig som kännetecknas av våra värderingar '
                        "'Ny\x00ken, Omtänksam och Tillgänglig'. Allmäntandvård, "
                        'meriterande om du är nischad i en eller \x00flera områden. Du '
                        'har goda kunskaper i det svenska språket i både tal och '
                        'skrift. Har du tidigare arbetat med Opus är detta '
                        'meriterande.\n'
                        ' Family Dental Care i Degerfors är en hemtrevlig och modern '
                        'tandläkarklinik i centrala Degerfors. Patienterna ska få en '
                        'omhändertagande känsla när de kliver in genom vår dörr. '
                        'Samtliga behandlingar utförs av välutbildad, trevlig och '
                        'kompetent personal som också har god erfarenhet av patienter '
                        'med tandläkarskräck.',
          'annonstextFormaterad': 'Vi söker dig som är \x00exibel, tar egna initiativ '
                                  'och har en god samarbetsförmåga. Ett stort intresse '
                                  'för att erbjuda personlig service är nödvändigt. Din '
                                  'positiva attityd bidrar till vår goda stämning på '
                                  'mottagningen. Du tycker att det är roligt med '
                                  'service och att medverka i mottagningens '
                                  'utvecklingsarbete.\n'
                                  'Vi lägger stor vikt vid dina personliga egenskaper '
                                  'och söker särskilt efter dig som kännetecknas av '
                                  "våra värderingar 'Ny\x00ken, Omtänksam och "
                                  "Tillgänglig'. Allmäntandvård, meriterande om du är "
                                  'nischad i en eller \x00flera områden. Du har goda '
                                  'kunskaper i det svenska språket i både tal och '
                                  'skrift. Har du tidigare arbetat med Opus är detta '
                                  'meriterande.\n'
                                  ' Family Dental Care i Degerfors är en hemtrevlig och '
                                  'modern tandläkarklinik i centrala Degerfors. '
                                  'Patienterna ska få en omhändertagande känsla när de '
                                  'kliver in genom vår dörr. Samtliga behandlingar '
                                  'utförs av välutbildad, trevlig och kompetent '
                                  'personal som också har god erfarenhet av patienter '
                                  'med tandläkarskräck.',
          'ansokningssattEpost': 'tarek@familydentalcare.se',
          'ansokningssattViaAF': False,
          'anstallningTyp': {'namn': 'Vanlig anställning', 'varde': '1'},
          'antalPlatser': 2,
          'arbetsgivareId': '21203447',
          'arbetsgivareNamn': 'Famili Cooperation AB',
          'arbetsplatsId': '86943592',
          'arbetsplatsNamn': 'Famili Cooperation AB',
          'arbetsplatsadress': {'gatuadress': 'Medborgargatan 17 A 0TR',
                                'kommun': {'namn': 'Degerfors', 'varde': '1862'},
                                'koordinatPrecision': None,
                                'lan': {'namn': 'Örebro län', 'varde': '18'},
                                'land': None,
                                'latitud': '59.2418452211078',
                                'longitud': '14.43296439995',
                                'postnr': '69330',
                                'postort': 'DEGERFORS'},
          'arbetstidTyp': {'namn': 'Heltid', 'varde': '1'},
          'avpublicerad': False,
          'avpubliceringsdatum': '2019-01-01 07:12:59',
          'besoksadress': {'gatuadress': 'Medborgargatan 17 A 0TR',
                           'land': 'SE',
                           'postnr': '69330',
                           'postort': 'Degerfors'},
          'epost': 'tarek@familydentalcare.se',
          'expiresAt': '2019-05-31 23:59:59',
          'id': '23075723',
          'informationAnsokningssatt': 'Ansökan sker med CV och personligt brev inkl. '
                                       'bild endast per mail. OBS! Vänligen endast per '
                                       'mail.\n'
                                       'Tjänsten är hel- eller deltid med tillträde '
                                       'enligt överenskommelse.',
          'ingenErfarenhetKravs': True,
          'kallaTyp': 'VIA_AF_FORMULAR',
          'kompetenser': [{'namn': 'Tandläkarexamen', 'varde': '608237', 'vikt': 10},
                          {'namn': 'Legitimation som tandläkare',
                           'varde': '3432',
                           'vikt': 10}],
          'lonTyp': {'namn': 'Fast månads- vecko- eller timlön', 'varde': '1'},
          'lonebeskrivning': 'Lön 75.000kr',
          'organisationsnummer': '5591273841',
          'postadress': {'gatuadress': 'Lotsgatan 155',
                         'land': 'SE',
                         'postnr': '21642',
                         'postort': 'Limhamn'},
          'publiceringsdatum': '2019-01-28 00:00:00',
          'referens': 'Tandläkare',
          'sistaAnsokningsdatum': '2019-05-31 23:59:59',
          'sistaPubliceringsdatum': '2019-05-31 23:59:59',
          'telefonnummer': '0733590030',
          'tillgangTillEgenBil': False,
          'updatedAt': 123456790,
          'varaktighetTyp': {'namn': '6 månader eller längre', 'varde': '2'},
          'version': '2.0',
          'yrkesroll': {'namn': 'Tandläkare', 'varde': '5724'}}




if __name__ == '__main__':
    pytest.main([os.path.realpath(__file__), '-svv', '-ra', '-m integration'])