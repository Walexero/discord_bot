from woocommerce import API

def _query_api(input_query):
    #MULTIPLE QUERYS VARIABLE
    response_holder = []
    lookup = []

    wcapi = API(
        url="https://learn-league.com/",
        consumer_key= "ck_a482ff0296b8b4a56b74ac4dc0cffbcd9a3d7ed7",
        consumer_secret= "cs_f2e6b2f73ce68d50dd36bcd10b64d0eea2aa1c3f",
        wp_api=True,
        verify_ssl = True,
        version="wc/v3",
        query_string_auth = True,
    )

    def _get_total_pages_from_headers():
        lookup_get_header = wcapi.get(input_query,params={
                         "per_page": 50,
                         "page": 1,
                         "role": "all",
                         "order_by": "id"
                       })
        totalpages = lookup_get_header.headers["X-WP-TotalPages"]
        return int(totalpages)

    def _lookup_per_page(pages):
        for page_no in range(pages):
          lookup_page = wcapi.get(input_query,
          params={
                           "per_page": 50,
                           "page": page_no + 1,
                           "role": "all",
                           "order_by": "id"
                         }).json()
          response_holder.append(lookup_page)
        
    pages = _get_total_pages_from_headers()
    print(pages)

    def _query_resolver(pages,input_query):
        if pages > 1:
            _lookup_per_page(pages)
            return
        else:
            lookup_page = wcapi.get(input_query,
              params={
                               "per_page": 50,
                               "page": 1,
                               "role": "all",
                               "order_by": "id"
                             }).json()
            return lookup_page

    resolver = _query_resolver(pages,input_query)

    if resolver:
        print("Nice,Nice")
    else:
        for lookups in response_holder:
          for objects in lookups:
            lookup.append(objects)
        return lookup
