async def _get_subscription_info(subscriber_email):
            print("Starting to query API")

            def _subscription_verifier(subscribers,subscriber_email):
                print("Finding Specific subscriber")
                for verify_subscriber_email in subscribers:
                    
                    if verify_subscriber_email["email"] == subscriber_email:
                        print(verify_subscriber_email)

            wcapi = API(
                url="https://learn-league.com/",
                consumer_key= os.getenv("PUB_KEY"),
                consumer_secret= os.getenv("PRIV_KEY"),
                wp_api=True,
                verify_ssl = True,
                version="wc/v3",
                query_string_auth = True,
            )

            lookup_subscribers = wcapi.get("customers").json()
            print("Finished querying API")
            return _subscription_verifier(lookup_subscribers, subscriber_email)