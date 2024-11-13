from pymongo import MongoClient

client = MongoClient("mongodb+srv://hono1030:Go1F3bz62ANxcQzW@cluster0.egdgc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client.message_db

collection_name = db["message_collection"]