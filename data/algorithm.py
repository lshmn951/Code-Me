import requests
import csv
from bs4 import BeautifulSoup

URL_TAGS = "https://www.acmicpc.net/problem/tags"
URL_TAG_ALGORITHM = "https://www.acmicpc.net/problem/tag/"
USER_AGENT = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}

def get_tags_list():
    res = requests.get(URL_TAGS,headers=USER_AGENT)
    bs = BeautifulSoup(res.text,"lxml")
    table = bs.find("div","table-responsive")
    trlist = table.select("tbody > tr")
    taglist = []

    for tr in trlist:
        taglist.append(tr.select_one("a").text)

    return taglist

def get_algorithm_problem_list(tag):
    res = requests.get(URL_TAG_ALGORITHM+tag,headers=USER_AGENT)
    bs = BeautifulSoup(res.text,"lxml")
    page_list_html = bs.find("ul","pagination")
    pglist = page_list_html.select("li")
    page_list = []
    for pg in pglist:
        page_list.append(pg.select_one("a").text)
    pblist = []
    for page in page_list:
        res2 = requests.get(URL_TAG_ALGORITHM+tag+"/"+page,headers=USER_AGENT)
        bs2 = BeautifulSoup(res2.text,"lxml")
        prob_list_html = bs2.find("table",id="problemset")
        if prob_list_html is not None:
            prlist = prob_list_html.select("tbody > tr")

            for prob in prlist:
                pblist.append(int(prob.find("td").text))


    pblist.sort()
    prob_list=[]
    prob_list.append(tag)
    for pb in pblist:
        prob_list.append(pb)
    return prob_list

csv_list = []
tags_list = get_tags_list()

for tag in tags_list:
    temp_list = []
    temp_list = get_algorithm_problem_list(tag)
    csv_list.append(temp_list)

print(csv_list)

with open('algorithm_problems.csv','w',newline='') as f:
    writer = csv.writer(f)
    writer.writerows(csv_list)
