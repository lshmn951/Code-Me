from crawler import basecrawler


URL_BASE = "https://www.acmicpc.net"
URL_RANKLIST = URL_BASE + "/ranklist/"
URL_USER = URL_BASE + "/user/"


def get_rank_list_page_max(rheader=None):
    bs = basecrawler.get_bs_from_url(URL_RANKLIST + "1", rheader)
    return int(bs.select(".pagination a")[-1]["href"][10:])


def get_user_list_by_page(pagenum, rheader=None):
    bs = basecrawler.get_bs_from_url(URL_RANKLIST + str(pagenum), rheader)
    return [tr.select_one("a").text for tr in bs.select("#ranklist > tbody > tr")]


def get_accept_list_by_user(uid, rheader=None):
    bs = basecrawler.get_bs_from_url(URL_USER + uid, rheader)
    accept_list_html = bs.select_one(".panel-body").select(".problem_number")
    accept_list = [int(acc.text) for acc in accept_list_html]
    return accept_list

if __name__ == "__main__":
    prob_list = []
    get_accept_list_by_user("oogab")


