import json
from woocommerce import API

def _query_api(input_query):
      print("Starting to query API")
      wcapi = API(
        url="https://learn-league.com/",
        consumer_key="ck_a482ff0296b8b4a56b74ac4dc0cffbcd9a3d7ed7",
        consumer_secret="cs_f2e6b2f73ce68d50dd36bcd10b64d0eea2aa1c3f",
        wp_api=True,
        verify_ssl=True,
        version="wc/v3",
        query_string_auth=True,
      )

      lookup = wcapi.get(input_query,
                         params={
                           "per_page": 100,
                           "page": 1,
                           "role": "all",
                           "order_by": "id"
                         }).json()
      return lookup


def _query_api(input_query):
    print("Starting to query API")
    lookup = []
    lookup2 = []
    wcapi = API(
      url="https://learn-league.com/",
      consumer_key="ck_a482ff0296b8b4a56b74ac4dc0cffbcd9a3d7ed7",
      consumer_secret="cs_f2e6b2f73ce68d50dd36bcd10b64d0eea2aa1c3f",
      wp_api=True,
      verify_ssl=True,
      version="wc/v3",
      query_string_auth=True,
    )
    def _get_total_pages_from_headers():
      lookup_get_header = wcapi.get(input_query,params={
                         "per_page": 25,
                         "page": 1,
                         "role": "all",
                         "order_by": "id"
                       })
      totalpages = lookup_get_header.headers["X-WP-TotalPages"]
      print(totalpages)
      print(type(totalpages))
      return int(totalpages)
    def _lookup_per_page(pages):
      for page_no in range(pages):
        lookup_page = wcapi.get(input_query,
        params={
                         "per_page": 25,
                         "page": page_no + 1,
                         "role": "all",
                         "order_by": "id"
                       })
        lookup.append(lookup_page)
    _lookup_per_page(_get_total_pages_from_headers())
    print(lookup.json())
    for items in lookup:
        for item in items:
            lookup2.append(item)
    return lookup2
_query_api("customers")
