from datetime import date, timedelta
from time import sleep
import multiprocessing
import requests
import datetime
import time
start_time = time.time()

start = datetime.datetime.strptime("2020-08-1", "%Y-%m-%d")
end = datetime.datetime.strptime("2020-08-31", "%Y-%m-%d")
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days + 1)]

headers = {
    'authority': 'www.skyscanner.es',
    'x-skyscanner-devicedetection-istablet': 'false',
    'x-skyscanner-channelid': 'website',
    'x-skyscanner-utid': 'b9bd58b1-1fed-4c4c-9fe4-f5fa9a31ed1d',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'x-skyscanner-traveller-context': 'b9bd58b1-1fed-4c4c-9fe4-f5fa9a31ed1d',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'accept': 'application/json',
    'x-skyscanner-viewid': 'abb1e8c7-c8ba-4c1c-9df3-1c4d6fcbc0a9',
    'x-skyscanner-devicedetection-ismobile': 'false',
    'x-skyscanner-mixpanelid': '1694dbc0747975-0c547e5570983a-36667105-384000-1694dbc07489ef',
    'origin': 'https://www.skyscanner.es',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.skyscanner.es/transporte/vuelos/eas/mad/200731/',
    'accept-language': 'es-ES,es;q=0.9',
    'cookie':'gdpr=information:::true&adverts:::true&version:::2; _pxhd=e6a0700c9d9d1e3cece35d4232c2da2c2576a42693b69b12544424b379920aa4:8f136721-a076-11ea-b1dd-67a29f7690af; traveller_context=b9bd58b1-1fed-4c4c-9fe4-f5fa9a31ed1d; ssculture=locale:::es-ES&market:::ES&currency:::EUR; device_guid=ea05a7f5-8bc0-46ba-9acc-77ee94934bdb; scanner=currency:::EUR; _pxvid=8f136721-a076-11ea-b1dd-67a29f7690af; preferences=a54787f064d14e399d2344017662dc64; mp_2434748954c30ccc5017faa456fa3d38_mixpanel=%7B%22distinct_id%22%3A%20%221725c7cce1c1d2-0538c7c0be57ee-f7d1d38-1fa400-1725c7cce1d7d0%22%2C%22%24device_id%22%3A%20%221725c7cce1c1d2-0538c7c0be57ee-f7d1d38-1fa400-1725c7cce1d7d0%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22User%20Locale%22%3A%20%22ES-ES%22%2C%22User%20Market%22%3A%20%22ES%22%2C%22User%20Currency%22%3A%20%22EUR%22%2C%22New%20User%22%3A%20false%2C%22Internal%20User%22%3A%20%22%22%2C%22Mobile%22%3A%20%22FALSE%22%2C%22Tablet%22%3A%20%22FALSE%22%2C%22OS%20Version%22%3A%20%22NT%2010.0%22%2C%22Device%20Model%22%3A%20%22CHROME%20-%20WINDOWS%22%2C%22Browser%20Version%22%3A%20%2283.0.4103.61%22%2C%22Microsite%22%3A%20%22POKEMON%22%2C%22Skyscanner%20Is%20Authenticated%22%3A%20false%2C%22Skyscanner%20User%20Id%22%3A%20%22b9bd58b1-1fed-4c4c-9fe4-f5fa9a31ed1d%22%2C%22Skyscanner%20UTID%22%3A%20%22b9bd58b1-1fed-4c4c-9fe4-f5fa9a31ed1d%22%2C%22User%20GeoMarket%22%3A%20%22ES%22%2C%22Top%20Level%20Domain%22%3A%20%22www.skyscanner.es%22%2C%22Culture%20Cookie%20Present%22%3A%20true%7D; _px3=e0d09a81d7a7a440e2cdd3ffdcefc812e5151c1581e8bdc659b7fea8e14f4a5e:nIwgjIzcAAEDl2lJ2hv0MCtT7WSEky0A0FHrzVdDVB+NqvgWU80vcfg3LKOcJDbtJ3RR3LR73jGCFKGuG1hOHA==:1000:trjfXawzFhFIkoCiYmjNlI3NLn+8w63E7xhI80GLaCZdt+ROuwg8xPjYlBTQdsj/xz+0MjR0axgeEPaZLUVthdsGi5jiYbq6Pis7uJu0+AHMrZXh+372UTf6V/Pjxld1FEp1GJA/mffXjc+wpqrU4eFyE0wlzypdX2xMAxlyjXI=; ssaboverrides=; ssab=AAExperiment_V8:::b&BD_DV_Search_Bar_Expanded_V3:::b&BD_recommend_hotel_DV_V2:::a&CLABS_Web_New_Review_Page_V1:::b&Google_YOLO_Experiment_A_V7:::b&MR_HotelRelevance_ModelCohortExploration_V3:::a&New_SEO_Pages_Airport_V8:::a&Refund_Enable_QueryHistory_V1:::on&TerraEcoSortFilter_V10:::b&Terra_Artemis_multi_segment_load_test_V19:::a&Trex_DirectDays_Web_V21:::b&WOM_Mixpanel_Akamai_V5:::a&WOM_insp_shelves_return_link_V3:::b&bss_mirror_eu_central_1_V1:::a&bss_mirror_eu_west_1_V1:::a&bss_split_eu_central_1_V1:::a&bss_split_eu_west_1_V1:::a&change_optional_extra_title_V10:::a&conductor_fps_response_logs_V4:::a&dbook_finn_trafficcontrol_non_ru_web_V2:::a&dbook_mang_trafficcontrol_WEB_V2:::a&dbook_sune_trafficcontrol_web_V5:::a&fishmonger_split_ap_northeast_1_V7:::a&fishmonger_split_ap_southeast_1_V7:::a&fishmonger_split_eu_central_1_V6:::a&fishmonger_split_eu_west_1_V6:::a&flights_geo_mirror_ap_northeast_1_V2:::a&flights_geo_mirror_ap_southeast_1_V5:::a&flights_geo_mirror_eu_central_1_V2:::a&flights_geo_mirror_eu_west_1_V2:::a&fps_itc_filtering_enabled_web_V13:::true&fps_lus_quote_service_push_content_V7:::disabled&fps_mr_fqs_flights_pluto_V21:::c&fps_partner_data_if_V18:::c&fps_split_cell_apse_V9:::cell&fps_split_cell_web_apne_V5:::cell&fps_split_cell_web_euc_V15:::cell&fps_split_cell_web_euw_V47:::cell&fps_ttfr_skinny_phase_1_web_V7:::enabled&freeag_flights_price_alerts_V5:::b&hercules_card_detection_V6:::b&hercules_new_payment_form_V6:::b&kbconnector_mirror_ap_northeast_1_V3:::a&kbconnector_mirror_ap_southeast_1_V2:::a&kbconnector_mirror_eu_central_1_V2:::a&kbconnector_mirror_eu_west_1_V2:::a&mr_migration_proxy_test_always_on_V3:::a&mr_request_duplicator_test_01_V9:::a&pel_use_website_link_data_V10:::b&relevance_service_split_ap_northeast_1_V11:::a&relevance_service_split_ap_southeast_1_V9:::a&relevance_service_split_eu_central_1_V7:::a&relevance_service_split_eu_west_1_V14:::a&tempatron_rollout_V8:::a&terra_artemis_conductor_V28:::a&tps_proxy_traffic_V1:::a&unified_search_flights_enabled_V4:::a&unified_search_hotels_enabled_V2:::a&wom_hotel_search_price_alerts_V6:::b; experiment_allocation_id=e5e5004082fbb1069ee44a919ce9c396d0c48ceac385e3566ce470cb45c0108a; akacd_Acorn_Split_Traffic=1591447284~rv=10~id=421d247c9324aecb6665af713d9123ca',
#    'cookie':'_pxhd=10ff6a4b5b2c47e240c610b7492e6058e8a13e339a8475a38ba423e301d6a593:59ce4270-a2c8-11ea-8e00-6bc78b598546; ssaboverrides=; traveller_context=aef1f8a4-042d-4405-b4cd-10e319c083fc; ssab=AAExperiment_V8:::a&BD_DV_Search_Bar_Expanded_V3:::b&BD_recommend_hotel_DV_V2:::b&CLABS_Web_New_Review_Page_V1:::b&Google_YOLO_Experiment_A_V7:::b&MR_HotelRelevance_ModelCohortExploration_V3:::c&New_SEO_Pages_Airport_V8:::b&Refund_Enable_QueryHistory_V1:::on&TerraEcoSortFilter_V10:::b&Terra_Artemis_multi_segment_load_test_V19:::a&Trex_DirectDays_Web_V21:::b&WOM_Mixpanel_Akamai_V5:::a&WOM_insp_shelves_return_link_V3:::b&bss_split_ap_southeast_1_V1:::a&bss_split_eu_west_1_V1:::a&change_optional_extra_title_V10:::a&conductor_fps_response_logs_V4:::a&dbook_basi_trafficcontrol_web_V2:::a&dbook_finn_trafficcontrol_non_ru_web_V2:::a&dbook_mang_trafficcontrol_WEB_V2:::a&dbook_ssev_trafficcontrol_web_phase2_V7:::a&dbook_sune_trafficcontrol_web_V5:::a&fishmonger_split_ap_northeast_1_V7:::a&fishmonger_split_ap_southeast_1_V7:::a&fishmonger_split_eu_central_1_V6:::a&fishmonger_split_eu_west_1_V6:::a&flights_geo_mirror_ap_northeast_1_V2:::a&flights_geo_mirror_ap_southeast_1_V5:::a&flights_geo_mirror_eu_central_1_V2:::a&flights_geo_mirror_eu_west_1_V2:::a&fps_itc_filtering_enabled_web_V13:::false&fps_lus_quote_service_push_content_V7:::disabled&fps_mr_fqs_flights_pluto_V21:::c&fps_partner_data_if_V18:::c&fps_split_cell_apse_V9:::cell&fps_split_cell_web_apne_V5:::cell&fps_split_cell_web_euc_V15:::cell&fps_split_cell_web_euw_V47:::cell&fps_ttfr_skinny_phase_1_web_V7:::disabled&freeag_flights_price_alerts_V5:::b&hercules_card_detection_V6:::b&hercules_new_payment_form_V6:::b&inline_plus_format_campaign_V2:::a&kbconnector_mirror_ap_northeast_1_V3:::a&kbconnector_mirror_ap_southeast_1_V2:::a&kbconnector_mirror_eu_central_1_V2:::a&kbconnector_mirror_eu_west_1_V2:::a&mr_migration_proxy_test_always_75_percent_V1:::a&mr_migration_proxy_test_always_on_V3:::a&mr_request_duplicator_test_01_V9:::a&pel_use_website_link_data_V10:::b&relevance_service_split_ap_northeast_1_V11:::a&relevance_service_split_ap_southeast_1_V9:::a&relevance_service_split_eu_central_1_V7:::a&relevance_service_split_eu_west_1_V14:::a&taps_api_cells_traffic_mirroring_eu_west_1_V7:::a&tempatron_rollout_V8:::a&terra_artemis_conductor_V28:::a&tps_proxy_traffic_V1:::a&unified_search_flights_enabled_V4:::a&unified_search_hotels_enabled_V2:::a&wom_hotel_search_price_alerts_V6:::b; experiment_allocation_id=9cd9f75777135f4968161111e626a24857cc35fbe1f514677d7e995284f5bef9; ssculture=locale:::es-ES&market:::ES&currency:::EUR; scanner=currency:::EUR; device_guid=81e3a080-4661-4c05-995f-e305b6e5d0d4; akacd_Acorn_Split_Traffic=1591483997~rv=81~id=ba3882c72a93959122d4d0e3fb5fc436; preferences=aef1f8a4042d4405b4cd10e319c083fc; _ga=GA1.2.1380979952.1590879195; _gid=GA1.2.1543807894.1590879195; _gat=1; RT="z=1&dm=skyscanner.es&si=a696f963-e4e2-49cd-ad49-b6bbe43b5ad5&ss=kau8e43l&sl=1&tt=8p3&bcn=%2F%2F173e255a.akstat.io%2F&ld=8po"; _pxvid=59ce4270-a2c8-11ea-8e00-6bc78b598546; _px3=4499cccef52f6e55660d7b583db3fbfd0512a15a823881319e4beea30b1f1f97:jV1C9S0lRM6gxs0h9iq8oZCrbz2HD9XXRciJDNqTBxczQw4HuTtBWhNIIES1xv9aSJogNPiHfqe1JnA4i95cxw==:1000:8jrQ7Hmi5E2TORfkmTh7ZCwt42s+7mexBKORckjzmsyGNbYwBXYBIPenYYR9coHKWp356Vi0ABkE3hEGjJ3eBi0tTJDHJJI2OmmhHz/HBBu4Db+G3tl2i0L1985bHunVfMgfWNBvKwYdTP8RmBJYEOUeqF85OU2yaKZ0pNJJJ1k=; gdpr=information:::true&adverts:::true&version:::2; _uetsid=92e56000-d96a-0c8b-6ef2-28a58e443daf; _fbp=fb.1.1590879229308.30748059',
}

params = (
    ('geo_schema', 'skyscanner'),
    ('carrier_schema', 'skyscanner'),
    ('response_include', 'query;deeplink;segment;stats;fqs;pqs'),
)

with open('iata.json') as f:
    iatak = f.readlines()


def worker(iata,eguna):
    data = '{"adults":1,"cabinClass":"ECONOMY","options":{"include_unpriced_itineraries":true,"include_mixed_booking_options":true},"child_ages":[],"prefer_directs":false,"state":{},"alternativeOrigins":false,"alternativeDestinations":false,"market":"ES","locale":"es-ES","currency":"EUR","viewId":"abb1e8c7-c8ba-4c1c-9df3-1c4d6fcbc0a9","travellerContextId":"b9bd58b1-1fed-4c4c-9fe4-f5fa9a31ed1d","trusted_funnel_search_guid":"abb1e8c7-c8ba-4c1c-9df3-1c4d6fcbc0a9","legs":[{"origin":"MAD","destination":'+'"'+str(iata)+'"'+',"date":'+'"'+str(eguna)+'"'+',"add_alternative_origins":false,"add_alternative_destinations":false}]}'
    response = requests.post('https://www.skyscanner.es/g/conductor/v1/fps3/search/', headers=headers, params=params, data=data)
    print(response.status_code, len(response.content), str(iata), str(eguna))


counter=0
if __name__ == '__main__':
    jobs = []
    for i in iatak:
        for date in date_generated:
            eguna = date.strftime("%Y-%m-%d")
            i = i.replace('\n', '')
            p = multiprocessing.Process(target=worker, args=(i,eguna))
            jobs.append(p)
            p.start()
            counter = counter+1
            sleep(0.1)
sleep(2)
print(str(counter)+"requests in %s seconds " % (time.time() - start_time))
