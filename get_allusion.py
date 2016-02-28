__author__ = 'Qing'
# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup
import re
from pymongo import MongoClient


def html_tag_to_space(a_str):
    dr = re.compile(r'<[^>]+>', re.S)
    return dr.sub(' ', a_str)


def get_dm(div):
    span = div.find('span', class_='indentLabel', text='典故')
    dm_str = ''
    for sibling in span.next_siblings:
        for dm in html_tag_to_space(str(sibling)).split():
            dm_str += dm + '  '
    return dm_str


def get_dy_or_yl(div):
    content_str = ''
    for ele in div.contents:
        if ele == '\n':
            pass
        else:
            content = html_tag_to_space(str(ele))
            content_str += content
    return content_str


if __name__ == "__main__":
    dm_file = open("/home/hadoop/CloudClassHomework/dianmian-05.txt", 'w+', encoding='utf-8')
    dy_file = open("/home/hadoop/CloudClassHomework/dianyuan-05.txt", 'w+', encoding='utf-8')
    yl_file = open("/home/hadoop/CloudClassHomework/yongli-05.txt", 'w+', encoding='utf-8')
    client = MongoClient('localhost', 27017)
    db = client.dg_db
    collection = db.dg_collection
    for i in range(103):
        url = "http://sou-yun.com/AllusionsIndex.aspx?page=" + str(i)
        data = urllib.request.urlopen(url).read()
        page_html = data.decode('utf-8')
        soup = BeautifulSoup(page_html, "html.parser")
        for div_tag in soup.find_all('div', class_='allusion'):
            block_divs = div_tag.find_all("div", class_="allusionBlock")
            dm_content = get_dm(block_divs[0])
            dm_file.write(dm_content + "\n==============================\n")
            dy_content = get_dy_or_yl(block_divs[1])
            dy_file.write(dy_content + "\n================================\n")
            yl_content = get_dy_or_yl(block_divs[len(block_divs) - 1])
            yl_file.write(yl_content + "\n================================\n")
            collection.insert_one({"dm": dm_content, "dy": dy_content, "yl": yl_content})
    client.close()
    dm_file.close()
    dy_file.close()
    yl_file.close()
