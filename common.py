import json
from threading import Semaphore
import pymongo

sem = Semaphore()
con = pymongo.MongoClient()
coll = con.skyscanner.routes

def get_params():
    return (
        ('geo_schema', 'skyscanner'),
        ('carrier_schema', 'skyscanner'),
        ('response_include', 'query;deeplink;segment;stats;fqs;pqs'),
    )

def get_headers():
    return {
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
    'cookie':'_pxhd=cc5cbaa696ab0784a88948125c941a44af952322d6e7c9bd3b7603e6528a3c14:c281ace1-a39e-11ea-8f90-61e8f4161c5f; ssaboverrides=; traveller_context=a493311d-3678-4a26-8ea7-7ecbc84a3aca; ssab=AAExperiment_V8:::a&BD_DV_Search_Bar_Expanded_V3:::b&BD_recommend_hotel_DV_V2:::a&CLABS_Web_New_Review_Page_V1:::b&Google_YOLO_Experiment_A_V7:::b&MR_HotelRelevance_ModelCohortExploration_V3:::b&New_SEO_Pages_Airport_V8:::b&Refund_Enable_QueryHistory_V1:::on&TerraEcoSortFilter_V10:::b&Terra_Artemis_multi_segment_load_test_V19:::a&Trex_DirectDays_Web_V21:::b&WOM_Mixpanel_Akamai_V5:::b&WOM_insp_shelves_return_link_V3:::b&bss_mirror_ap_southeast_1_V1:::a&bss_mirror_eu_central_1_V1:::a&bss_mirror_eu_west_1_V1:::a&change_optional_extra_title_V10:::a&conductor_fps_response_logs_V4:::a&dbook_basi_trafficcontrol_web_V2:::a&dbook_finn_trafficcontrol_non_ru_web_V2:::a&dbook_mang_trafficcontrol_WEB_V2:::a&dbook_ssev_trafficcontrol_web_phase2_V7:::a&dbook_sune_trafficcontrol_web_V5:::a&dbook_uair_trafficcontrol_web_V2:::a&fishmonger_split_ap_northeast_1_V7:::a&fishmonger_split_ap_southeast_1_V7:::a&fishmonger_split_eu_central_1_V6:::a&fishmonger_split_eu_west_1_V6:::a&flights_geo_mirror_ap_northeast_1_V2:::a&flights_geo_mirror_ap_southeast_1_V5:::a&flights_geo_mirror_eu_central_1_V2:::a&flights_geo_mirror_eu_west_1_V2:::a&fps_bypass_bws_near_duplicate_filter_V3:::b&fps_itc_filtering_enabled_web_V13:::true&fps_lus_quote_service_push_content_V7:::enabled&fps_mr_fqs_flights_pluto_V21:::c&fps_partner_data_if_V18:::c&fps_split_cell_apse_V9:::cell&fps_split_cell_web_apne_V5:::cell&fps_split_cell_web_euc_V15:::cell&fps_split_cell_web_euw_V47:::cell&fps_ttfr_skinny_phase_1_web_V7:::enabled&freeag_flights_price_alerts_V5:::b&hercules_card_detection_V6:::b&hercules_new_payment_form_V6:::b&inline_plus_format_campaign_V2:::a&kbconnector_mirror_ap_northeast_1_V3:::a&kbconnector_mirror_ap_southeast_1_V2:::a&kbconnector_mirror_eu_central_1_V2:::a&kbconnector_mirror_eu_west_1_V2:::a&mr_migration_proxy_test_always_75_percent_V1:::a&mr_migration_proxy_test_always_on_V3:::a&mr_request_duplicator_test_01_V9:::a&pel_use_website_link_data_V10:::b&relevance_service_split_ap_northeast_1_V11:::a&relevance_service_split_ap_southeast_1_V9:::a&relevance_service_split_eu_central_1_V7:::a&relevance_service_split_eu_west_1_V14:::a&rts_magpie_soow_data_collection_V7:::budgetscheduled&taps_api_cells_traffic_mirroring_eu_west_1_V7:::a&tempatron_rollout_V8:::a&terra_artemis_conductor_V28:::a&tps_proxy_traffic_V1:::a&unified_search_flights_enabled_V4:::a&unified_search_hotels_enabled_V2:::a&wom_hotel_search_price_alerts_V6:::b; experiment_allocation_id=4c0c383086b519190d55099d4e5f8fb1ed0f2d2c99b121f5e883c619e721dc65; ssculture=locale:::es-ES&market:::ES&currency:::EUR; scanner=currency:::EUR; device_guid=cb385af8-2636-47ca-8818-d5efb24318c4; akacd_Acorn_Split_Traffic=1591576085~rv=81~id=693acfc946e4713606c73c2f432a36ac; preferences=a493311d36784a268ea77ecbc84a3aca; _ga=GA1.2.771405636.1590971287; _gid=GA1.2.739995992.1590971287; _gat=1; gdpr=information:::true&adverts:::true&version:::2; RT="sl=1&ss=kavr082w&tt=30j&bcn=%2F%2F686eb704.akstat.io%2F&z=1&dm=skyscanner.es&si=24000c59-1e45-4341-96a7-e0ce79cd717a&ld=7zfx"; _uetsid=b17142f4-9f8b-4c94-00da-aaf2c3137d1a; _pxvid=c281ace1-a39e-11ea-8f90-61e8f4161c5f; _px3=a2fc8df51a75315251a47a660cc8935358ef7a52d256cdcf8e33e6ff960bcf05:IioQEE7igxx42sZydef1wuq1UHNAJE27xIUw/38nKSf5kANWRn56dn4hadBz1x1k96Cdhv/HRMQ+3IHz1xnSjw==:1000:+AwkWinTc8OhPO0n8aXKTWwotAfQTSId+orPME8y2vtnV0YfROg6Xu7srFksqmFKxHzV7LjowvNcYAw8rUhxcActAM60TPhIpYZ6OHNnazHM6YDYlQvQb1PmGZR+OYTzT1+ilR5H5xpSRBi+m8VITiXfkU/AAJ4LpJS41wN93ik=',
}

def get_iatas():
    with open('iata.json') as f:
        iatas = f.readlines()
    return iatas

def get_request_data(day, iata):
    return '{"adults":1,"cabinClass":"ECONOMY","options":{"include_unpriced_itineraries":true,"include_mixed_booking_options":true},"child_ages":[],"prefer_directs":false,"state":{},"alternativeOrigins":false,"alternativeDestinations":false,"market":"US","locale":"en-US","currency":"EUR","viewId":"abb1e8c7-c8ba-4c1c-9df3-1c4d6fcbc0a9","travellerContextId":"b9bd58b1-1fed-4c4c-9fe4-f5fa9a31ed1d","trusted_funnel_search_guid":"abb1e8c7-c8ba-4c1c-9df3-1c4d6fcbc0a9","legs":[{"origin":"MAD","destination":'+'"'+str(iata)+'"'+',"date":'+'"'+str(day)+'"'+',"add_alternative_origins":false,"add_alternative_destinations":false}]}'

def process_data(data):
    raw = json.loads(data)
    routes = []
    for itinerary in raw["itineraries"]:
        for leg in raw["legs"]:
            if leg["id"] == itinerary["leg_ids"][0]:
                if len(leg["segment_ids"]) > 1:
                    scale = []
                    for place in raw["places"]:
                        if place["id"] == leg["origin_place_id"]:
                            origin_name = place["name"]
                        if place["id"] == leg["destination_place_id"]:
                            destination_name = place["name"]
                    new_route = {
                        "price": itinerary["pricing_options"][0]["price"]["amount"],
                        "origin_place_id": leg["origin_place_id"],
                        "destination_place_id": leg["destination_place_id"],
                        "arrival": leg["arrival"],
                        "departure": leg["departure"],
                        "duration": leg["duration"],
                        "scales": [],
                        "origin_name": origin_name,
                        "destination_name": destination_name,
                        "deep_link": itinerary["pricing_options"][0]["items"][0]["url"]                 }
                    for leg_segment in leg["segment_ids"]:
                        for segment in raw["segments"]:
                            if leg_segment == segment["id"]:
                                for place in raw["places"]:
                                    if place["id"] == segment["origin_place_id"]:
                                        origin_name = place["name"]
                                    if place["id"] == segment["destination_place_id"]:
                                        destination_name = place["name"]
                                for carrier in raw["carriers"]:
                                    if carrier["id"] == segment["operating_carrier_id"]:
                                        new_scale = {
                                            "origin_place_id": segment["origin_place_id"],
                                            "destination_place_id": segment["destination_place_id"],
                                            "arrival": segment["arrival"],
                                            "departure": segment["departure"],
                                            "duration": segment["duration"],
                                            "carrier": carrier["name"],
                                            "origin_name": origin_name,
                                            "destination_name": destination_name
                                        }
                                        break
                                break
                        new_route["scales"].append(new_scale)       
                else:
                    for segment in raw["segments"]:
                        if segment["id"] == leg["segment_ids"][0]:
                            for place in raw["places"]:
                                if place["id"] == segment["origin_place_id"]:
                                    origin_name = place["name"]
                                if place["id"] == segment["destination_place_id"]:
                                    destination_name = place["name"]
                            for carrier in raw["carriers"]:
                                if carrier["id"] == segment["operating_carrier_id"]:
                                    new_route = {
                                        "price": itinerary["pricing_options"][0]["price"]["amount"],
                                        "origin_place_id": segment["origin_place_id"],
                                        "destination_place_id": segment["destination_place_id"],
                                        "arrival": segment["arrival"],
                                        "departure": segment["departure"],
                                        "duration": segment["duration"],
                                        "carrier": carrier["name"],
                                        "origin_name": origin_name,
                                        "destination_name": destination_name,
                                        "deep_link": itinerary["pricing_options"][0]["items"][0]["url"] 
                                    }
                                    break
                            break               
        routes.append(new_route)
    return routes

    

