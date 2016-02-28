# -*- coding: UTF-8 -*-

import re
from pymongo import MongoClient

poem_id = ""
poem_title = ""
poem_author = ""
poem_content = ""


# 去掉所有的空格，换行，制表
def clear_string(s):
    p = re.compile('\s+')
    s = re.sub(p, '', s)
    return s


def insert_db(collection1):
    collection1.insert_one({"bh": poem_id, "pm": poem_title, "zz": poem_author, "zw": poem_content})


def set_poem(s):
    global poem_id
    global poem_author
    global poem_title
    s = clear_string(s)
    l1 = s.split("【")
    poem_id = l1[0]
    l2 = l1[1].split("】")
    poem_author = l2[1]
    poem_title = "【" + l2[0] + "】"


def set_poem(s):
    global poem_content
    s = clear_string(s)
    if ("," not in s) and ("。" not in s):
        return
    poem_content += s


def clear_poem():
    global poem_id
    global poem_author
    global poem_title
    global poem_content
    poem_id = ""
    poem_author = ""
    poem_title = ""
    poem_content = ""


def save_txt(f2):
    f2.write(poem_id)
    f2.write("\r\n")
    f2.write(poem_title)
    f2.write("\r\n")
    f2.write(poem_author)
    f2.write("\r\n")
    f2.write(poem_content)
    f2.write("\r\n")
    f2.write("\r\n")


if __name__ == "__main__":
    f = open('/Users/Richard/software/1.txt', 'r')
    f2 = open('/Users/Richard/software/tangshi-05.txt', 'w')
    client = MongoClient('localhost', 27017)
    db = client.ts_db
    collection = db.ts_collection
    line = f.readline().decode("gbk", "ignore")
    while line:
        if "【" in line:
            set_poem(line)
            while 1:
                line = f.readline().decode("gbk", "ignore")
                if "【" in line or line == '':
                    save_txt(f2)
                    insert_db(collection)
                    clear_poem()
                    break
                set_poem(line)
        else:
            line = f.readline().decode("gbk", "ignore")
    f.close()
    f2.close()
    client.close()
