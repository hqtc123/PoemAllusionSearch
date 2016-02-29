__author__ = 'Qing'
# -*- coding: UTF-8 -*-
from pymongo import MongoClient
import re
from datetime import *

if __name__ == "__main__":
    client = MongoClient("121.42.37.65", 27017)
    db = client.ts_db
    collection = db.myresults
    doc = collection.find_one({"_id": "一半"})
    print(str(doc["value"]["data"]["position"]) + "  sentence " + str(doc["value"]["data"]["sentence_index"]))
    poem = db.ts_co666.find_one({"_id":doc["value"]["data"]["poem_id"]})
    print(doc["value"]["data"]["poem_id"])
    print(poem["content"])
    print(poem["content_arr"])
