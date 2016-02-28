__author__ = 'Qing'
# -*- coding: UTF-8 -*-
from pymongo import MongoClient
import re
from datetime import *

if __name__ == "__main__":
    client = MongoClient("121.42.37.65", 27017)
    db = client.ts_db
    old_collection = db.ts_collection
    new_collection = db.ts_co666
    print(old_collection.count())
    print("start time " + str(datetime.today()))

    for doc in old_collection.find({"zz": "李世民"}):
        if doc["pm"] == "【句】":
            continue
        content = doc["zw"]
        poem_dict = {
            "title": doc["pm"][1:-1],
            "author": doc["zz"],
            "category": doc["bh"],
            "content_arr": re.split("，|。|\.|\*|？|！|；", content)[:-1],
            "content": content
        }
        new_collection.insert_one(poem_dict)
    print("end time " + str(datetime.today()))
