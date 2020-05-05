import numpy as np
import csv
from crawler import bojcrawler
from multiprocessing import Pool, freeze_support

URL_RANK = "https://www.acmicpc.net/ranklist/"
URL_USER = "https://www.acmicpc.net/user/"
USER_AGENT = {
    "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/76.0.3809.132 Safari/537.36"
}


def get_accept_list_per_page(page):
    freeze_support()
    pool = Pool(processes=4)
    uid_list = bojcrawler.get_user_list_by_page(page)
    temp_list = pool.map(bojcrawler.get_accept_list_by_user, uid_list)
    pool.close()
    return temp_list


def set_problem_count(temp_list,testnp):
    for temp in temp_list:
        tp0 = temp
        if not temp:
            return False
        for t in tp0:
            for tp1 in temp:
                testnp[t - 1000, tp1 - 1000] = testnp[t - 1000, tp1 - 1000] + 1
    return True


def set_problem_count_until_empty():
    testnp = np.zeros((17000, 17000), dtype=np.int32)
    page_max = bojcrawler.get_rank_list_page_max(USER_AGENT)
    for i in range(1,page_max):
        temp_list = get_accept_list_per_page(i)
        if not set_problem_count(temp_list,testnp):
            break
    return testnp


def counting_to_csv(testnp):
    with open('count.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(testnp)
    return


if __name__ == '__main__':
    counting_to_csv(set_problem_count_until_empty())







