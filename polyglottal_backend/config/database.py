from pymongo import MongoClient
import dns.resolver
import os

# DNS issues workaround
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)  # Disable default DNS resolver (server that responds to DNS requests)
dns.resolver.default_resolver.nameservers=['8.8.8.8']  # Use Google DNS instead
# end DNS issues workaround

client = MongoClient(os.getenv("MONGODB_CONN_STRING"))
db = client.message_db
collection_name = db["message_collection"]